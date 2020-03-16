import extrair_regioes as exReg
import write_shp
from aabbtree import AABB, AABBTree
import fiona
from fiona.crs import from_epsg
import math
import csv

def pre_process(tree):

    listaEscolas, escolas = exReg.extrair_escolas_reg(tree)
    listaSaude, saude = exReg.extrair_saude_reg(tree)
    listaOnibus, onibus = exReg.extrair_onibus_reg(tree)

    write_shp.write_escolas(listaEscolas, escolas)
    write_shp.write_saude(listaSaude, saude)
    write_shp.write_onibus(listaOnibus, onibus)

    # return()


def load_shp():
    escolas = fiona.open("chico_mendes/escola_estudo.shp")
    saude = fiona.open("chico_mendes/saude_estudo.shp")
    onibus = fiona.open("chico_mendes/onibus_estudo.shp")
    lagoa = fiona.open("chico_mendes/lagoa_metros.shp")
    chico_mendes = fiona.open("chico_mendes/area_chico_mendes.shp")

    return escolas, saude, onibus, lagoa, chico_mendes


def create_area(nextX, nextY, yminAmortizado, ymaxAmortizado,\
xmaxAmortizado, xminAmortizado, escolas, saude, onibus, lagoa, chico_mendes, \
espacamento, xmax, xmin, ymax, ymin):
    listaL = lagoa[0]['geometry']['coordinates']
    listaCoordenadas = chico_mendes[0]['geometry']['coordinates']
    startX = xminAmortizado
    startY = ymaxAmortizado
    nowX = startX + nextX
    nowY = startY + nextY

    var = 0.000000001

    idString = 'id'
    xString = 'local_x'
    yString = 'local_y'
    escolaString = 'escola'
    onibusString = 'linha_onibus'
    saudeString = 'unidade_saude'
    chicoString = 'area_parque_cm'
    lagoaString = 'area_lagoa_cm'
    ocupaString = 'ocupado'

    listaL = lagoa[0]['geometry']['coordinates']

    xminL = 999999999999999
    xmaxL = -99999999999999
    ymaxL = -99999999999999
    yminL = 999999999999999
    for elem in listaL[0]:

        if elem[0] > xmaxL:
            xmaxL = elem[0]
        elif elem[0] < xminL:
            xminL = elem[0]

        if elem[1] > ymaxL:
            ymaxL = elem[1]
        elif elem[1] < yminL:
            yminL = elem[1]

    dict_cm = {}

    id_ = 0
    for i in range(0, math.ceil( (xmaxAmortizado - xminAmortizado)/espacamento )):
        for j in range(0, math.ceil( (ymaxAmortizado - yminAmortizado)/espacamento )):

            cm = 0
            l_cm = 0
            ocupa = 1
            listaOnibus = []
            listaEscolas = []
            listaSaude = []

            tree = AABBTree()

            # (xmin, xmax), (ymin, ymax)
            area_estudo = AABB([(startX, nowX), (nowY, startY)])
            tree.add(area_estudo, 'envol')

            #LAGOA
            t = AABB([(xminL, xmaxL), (yminL, ymaxL)])
            if(tree.does_overlap(t)):
                l_cm = 1
                ocupa = 0

            #PARQUE
            t = AABB([(xmin, xmax), (ymin, ymax)])
            if(tree.does_overlap(t)):
                cm = 1
                ocupa = 0

            for linha in onibus:
                for ponto in linha['geometry']['coordinates']:
                    x, y = ponto
                    t = AABB([(x, x), (y, y)])
                    if(tree.does_overlap(t)):
                        listaOnibus.append(linha)
                        ocupa = 1
                        break

            for unidade in saude:
                x, y = unidade['geometry']['coordinates']

                t = AABB([(x, x), (y, y)])

                if(tree.does_overlap(t)):
                    ocupa = 1
                    listaSaude.append(unidade)


            for escola in escolas:
                x, y = escola['geometry']['coordinates']

                t = AABB([(x, x), (y, y)])

                if(tree.does_overlap(t)):
                    listaEscolas.append(escola)
                    ocupa = 1


            dict_cm[id_] = {idString : id_, 'i': i, 'j': j, xString : startX, yString : startY, escolaString : listaEscolas, \
                         saudeString : listaSaude, onibusString : listaOnibus, chicoString : cm, lagoaString : l_cm, ocupaString : ocupa }


            id_ += 1
            startX = nowX + var
            nowX += nextX

        startX = xminAmortizado
        nowX = startX + nextX
        startY = nowY - var
        nowY += nextY

    return dict_cm


def write_dict(dict_cm, name):
    name = name + '.csv'
    w = csv.writer(open(name, "w"))
    for key, val in dict_cm.items():
        w.writerow([key, val])


def logging(log, name):
    name = name + '.txt'

    with open(name, 'w') as f:
        for elem in log:
            for item in elem:
                f.write(str(item))


# End
