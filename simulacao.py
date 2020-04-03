import math
from scipy.spatial import distance
import copy
import random

def neighborhood(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
yminAmortizado, espacamento, dict_cm, i, j, id_, neigh, escolas, saude, onibus):

    col = math.ceil( (xmaxAmortizado - xminAmortizado)/espacamento )
    row = math.ceil( (ymaxAmortizado - yminAmortizado)/espacamento )
    cell = []

    if neigh == 'moore':

        ocupado = 0
        num_escolas = 0
        linhasOnibus = 0
        postoSaude = 0
        cell.append((i-1)*row+j) # vizinho de cima
        cell.append((i-1)*row+(j+1)) # viz diagonal superior direito
        cell.append(id_ + 1) # vizinho da direita
        cell.append((i+1)*row + (j+1)) # viz diagonal inferior direito
        cell.append((i+1)*row + j) # viz embaixo
        cell.append((i+1)*row + (j+1)) # viz diagonal inferior esquerdo
        cell.append(id_ - 1) # viz esquerdo
        cell.append((i-1)*row + (j-1)) # viz diagonal superior esquerdo

        for c in cell:
            if dict_cm[c]['ocupado']:
                ocupado += dict_cm[c]['ocupado']
            num_escolas += len(dict_cm[c]['escola'])
            linhasOnibus += len(dict_cm[c]['linha_onibus'])
            postoSaude += len(dict_cm[c]['unidade_saude'])

        ocupado = ocupado/len(cell)
        num_escolas = num_escolas/len(escolas)
        linhasOnibus = linhasOnibus/len(onibus)
        postoSaude = postoSaude/len(saude)

        return ocupado, num_escolas,linhasOnibus, postoSaude

def dista(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
yminAmortizado, espacamento, dict_cm, i, j, id_, dist):

    col = math.ceil( (xmaxAmortizado - xminAmortizado)/espacamento )
    row = math.ceil( (ymaxAmortizado - yminAmortizado)/espacamento )

    listaEsc = []
    listaOni = []
    listaSau = []
    for key in dict_cm:
        if len(dict_cm[key]['escola']) > 0:
            listaEsc.append(key)
        if len(dict_cm[key]['linha_onibus']) > 0:
            listaOni.append(key)
        if len(dict_cm[key]['unidade_saude']) > 0:
            listaSau.append(key)


    le = []
    lo = []
    ls = []
    if dist == 'manhattan':

        for e in listaEsc:
            x = int(e/row)
            y = e % row
            d = distance.cityblock([i, j], [x, y])
            le.append(d)

        for o in listaOni:
            x = int(o/row)
            y = o % row
            d = distance.cityblock([i, j], [x, y])
            lo.append(d)

        for s in listaSau:
            x = int(s/row)
            y = s % row
            d = distance.cityblock([i, j], [x, y])
            ls.append(d)

        distE = [l / max(le) for l in le]
        distO = [l / max(lo) for l in lo]
        distS = [l / max(ls) for l in ls]

        return min(distE), min(distO), min(distS)


def simulacao(neigh, dist, dict_temp, xmaxAmortizado, xminAmortizado, \
ymaxAmortizado, yminAmortizado, espacamento, escolas, saude, onibus, pesos, inercia):
    serie_historica = []
    fim = 1
    neigh = neigh
    dist = dist
    d0 = copy.deepcopy(dict_temp)
    serie_historica.append(d0)

    space_to_occup = 0
    occupied = 0
    lag = 0
    parq = 0

    for key in d0:
        if (d0[key]['area_parque_cm'] == 1) and (d0[key]['area_lagoa_cm'] == 0):
            space_to_occup += 1
        if d0[key]['area_lagoa_cm']:
            lag += 1
        if d0[key]['area_parque_cm']:
            parq += 1

    print('to: ', space_to_occup)

    log = []
    log_disc = []
    t = 0
    while ((occupied < (space_to_occup-2)) and (t < 100)):
        occ_now = 0
        for key in dict_temp:
            if (dict_temp[key]['area_parque_cm']):
                i = dict_temp[key]['i']
                j = dict_temp[key]['j']
                id_ = dict_temp[key]['id']
                ocupacao_per, escola_per, onibus_per, saude_per = neighborhood(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
                yminAmortizado, espacamento, dict_temp, i, j, id_, neigh, escolas, saude, onibus)
                distEscola, distOnibus, distSaude = dista(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
                yminAmortizado, espacamento, dict_temp, i, j, id_, dist)

                N = ocupacao_per*pesos[0]
                S = (escola_per*pesos[1] + onibus_per*pesos[2] + saude_per*pesos[3])/3
                D = (((1 - distEscola) + (1 - distOnibus) + (1 - distSaude)) / 3)*pesos[4]
                I = inercia
                P = 1
                E = 1

                if dict_temp[key]['area_lagoa_cm']:
                    P = 0

                funct = ((N + S + D - I))*P*E
                if funct < 0.0:
                    funct = 0.0

                f = random.random()
                if funct > f:
                    if dict_temp[key]['ocupado'] == 0:
                        dict_temp[key]['ocupado'] = 1
                        occupied += 1
                        occ_now += 1

        serie_historica.append(copy.deepcopy(dict_temp))
        log.append(['iteracao: ', t, ', ' 'space occ: ', occupied, '\n'])
        log_disc.append(['iteracao: ', t, ', ' 'space occ now: ', occ_now, '\n'])


        t+=1
        print('iteracao: ', t, 'space occ: ', occupied)


    print('final: ',occupied)

    return serie_historica, dict_temp, t, log, log_disc



# End


# def simulacao(neigh, dist, dict_cm, xmaxAmortizado, xminAmortizado, \
# ymaxAmortizado, yminAmortizado, espacamento, escolas, saude, onibus):
#     serie_historica = []
#     fim = 1
#     neigh = neigh
#     dist = dist
#     d0 = copy.deepcopy(dict_cm)
#     serie_historica.append(d0)
#
#     space_to_occup = 0
#     ocupped = 0
#
#     for key in d0:
#         if (d0[key]['area_parque_cm']) and (d0[key]['area_lagoa_cm'] == 0):
#             space_to_occup += 1
#
#     while occuped < space_to_occup:
#
#         for key in dict_cm:
#             if dict_cm[key]['area_parque_cm']:
#                 i = dict_cm[key]['i']
#                 j = dict_cm[key]['j']
#                 id_ = dict_cm[key]['id']
#                 ocupacao_per, escola_per, onibus_per, saude_per = neighborhood(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
#                 yminAmortizado, espacamento, dict_cm, i, j, id_, neigh, escolas, saude, onibus)
#                 distEscola, distOnibus, distSaude = dista(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
#                 yminAmortizado, espacamento, dict_cm, i, j, id_, dist)
#
#                 first_param = (ocupacao_per + escola_per + onibus_per + saude_per)/4
#                 second_param = (distEscola + distOnibus + distSaude) / 3
#
#                 print(first_param, second_param)
#
#                 if first_param + second_param > 0.6:
#                     if dict_cm[key]['area_lagoa_cm'] == 0:
#                         dict_cm[key]['ocupado'] = 1
#                         ocupped = space_to_occup
#
#     serie_historica.append(dict_cm)
#
#
#     return serie_historica, dict_cm
