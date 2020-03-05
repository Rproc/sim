import math
from scipy.spatial import distance
import copy

def neighborhood(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
yminAmortizado, espacamento, dict_cm, i, j, id_, neigh, escolas, saude, onibus):

    row = math.ceil( (xmaxAmortizado - xminAmortizado)/espacamento )
    col = math.ceil( (ymaxAmortizado - yminAmortizado)/espacamento )
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

    row = math.ceil( (xmaxAmortizado - xminAmortizado)/espacamento )
    col = math.ceil( (ymaxAmortizado - yminAmortizado)/espacamento )

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


def simulacao(neigh, dist, dict_cm, xmaxAmortizado, xminAmortizado, \
ymaxAmortizado, yminAmortizado, espacamento, escolas, saude, onibus):
    serie_historica = []
    fim = 1
    neigh = neigh
    dist = dist
    d0 = copy.deepcopy(dict_cm)
    serie_historica.append(d0)
    for key in dict_cm:
        if dict_cm[key]['area_parque_cm']:
            i = dict_cm[key]['i']
            j = dict_cm[key]['j']
            id_ = dict_cm[key]['id']
            ocupacao_per, escola_per, onibus_per, saude_per = neighborhood(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
            yminAmortizado, espacamento, dict_cm, i, j, id_, neigh, escolas, saude, onibus)
            distEscola, distOnibus, distSaude = dista(xmaxAmortizado, xminAmortizado, ymaxAmortizado, \
            yminAmortizado, espacamento, dict_cm, i, j, id_, dist)

            first_param = (ocupacao_per + escola_per + onibus_per + saude_per)/4
            second_param = (distEscola + distOnibus + distSaude) / 3

            print(first_param, second_param)

            if first_param + second_param > 0.6:
                if dict_cm[key]['area_lagoa_cm'] == 0:
                    dict_cm[key]['ocupado'] = 1


    return serie_historica, dict_cm







# End
