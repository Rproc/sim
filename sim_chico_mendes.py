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
import plots

# Parametros
name = 'parameters'
espacamento, n, neigh, dist, pesos, inercia, nome_serie, log, log_discrete = pp.load_param(name)

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

print('tree done')

escolas, saude, onibus, lagoa, chico_mendes = pp.load_shp()

dict_cm = pp.create_area(nextX, nextY, yminAmortizado, ymaxAmortizado,\
xmaxAmortizado, xminAmortizado, escolas, saude, onibus, lagoa, chico_mendes, \
espacamento, xmax, xmin, ymax, ymin)

pp.write_dict(dict_cm, 'teste')
# print(dict_cm[0])

# neigh = 'moore'
# dist = 'manhattan'
# # vizinhança, escola, pontos de onibus, saude, distancia
# pesos = [0.4, 0.3, 0.2, 0.1, 0.9]
# threshold = 0.10
# inercia = 0.65

print('pre process done')

serie, dict_cm, tempo, log, log_discrete = sim.simulacao(neigh, dist, dict_cm, xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
yminAmortizado, espacamento, escolas, saude, onibus, pesos, inercia )

print('end of simulation')
print(tempo)
# sink_list = []
# for key in dict_cm:
#     if dict_cm[key]['area_parque_cm']:
#         if dict_cm[key]['ocupado']:
#             sink_list.append(dict_cm[key])

# print(sink_list)

print('creating output')

write_shp.write_ocupacao_por_tempo(serie, 'ocupacao_cm', nextX, nextY)

pp.logging(log, 'log')
pp.logging(log_discrete, 'log_discrete')

print('plotting')
plots.plotOccBar(pp.log_processing(log_discrete))

plots.plot1(pp.log_processing(log), 100, 'Quantidade de células ocupadas por ano', 10, 20)


# End
