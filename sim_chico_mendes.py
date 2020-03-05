import pandas as pd
from pyproj import Proj, transform
import fiona
from fiona.crs import from_epsg
import logging
import sys
from aabbtree import AABB, AABBTree
import math
from scipy.spatial import distance
import copy
from shapely.geometry import mapping, Polygon
import pre_process as pp
import extrair_regioes as exReg
import simulacao as sim
import write_shp
# Parametros
espacamento = 50
n = 20 # multiplicador da area de amortização
nextX = espacamento
nextY = -espacamento


xmax, xmin, ymax, ymin = exReg.extrair_chico_mendes()

# print(xmax, xmin, ymax, ymin)
yminAmortizado = ymin + (-n*espacamento)
ymaxAmortizado = ymax + (n*espacamento)
xminAmortizado = xmin + (-n*espacamento)
xmaxAmortizado = xmax + (n*espacamento)

tree = AABBTree()
treeEstudo = AABBTree()
# (xmin, xmax), (ymin, ymax)
area_estudo = AABB([(xmin, xmax), (ymin, ymax)])
area_amortizada = AABB([(xminAmortizado, xmaxAmortizado), (yminAmortizado, ymaxAmortizado)])

tree.add(area_amortizada, 'envol')
treeEstudo.add(area_estudo)

pp.pre_process(tree)

escolas, saude, onibus, lagoa, chico_mendes = pp.load_shp()

dict_cm = pp.create_area(nextX, nextY, yminAmortizado, ymaxAmortizado,\
xmaxAmortizado, xminAmortizado, escolas, saude, onibus, lagoa, chico_mendes, \
espacamento)

pp.write_dict(dict_cm, 'teste')
# print(dict_cm[0])

neigh = 'moore'
dist = 'manhattan'

serie, dict_cm = sim.simulacao(neigh, dist, dict_cm, xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
yminAmortizado, espacamento, escolas, saude, onibus)


# sink_list = []
# for key in dict_cm:
#     if dict_cm[key]['area_parque_cm']:
#         if dict_cm[key]['ocupado']:
#             sink_list.append(dict_cm[key])

# print(sink_list)



write_shp.write_ocupacao_por_tempo(dict_cm, 'oc_test_py', nextX, nextY)







# End
