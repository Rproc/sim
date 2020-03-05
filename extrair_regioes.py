import fiona
from fiona.crs import from_epsg
from aabbtree import AABB, AABBTree


def extrair_chico_mendes():
    chico_mendes = fiona.open("Mapas_sim/shapes_sim_meters/area_chico_mendes.shp")
    # print (chico_mendes.schema)
    listaCoordenadas = chico_mendes[0]['geometry']['coordinates']
    # retirar ponto x máximo e ponto x mínimo, referente a projeção 3857
    # analogo para o ymin e ymax
    xmin = 999999999999999
    xmax = -99999999999999
    ymax = xmax
    ymin = xmin
    for elem in listaCoordenadas[0]:

        if elem[0] > xmax:
            xmax = elem[0]
        elif elem[0] < xmin:
            xmin = elem[0]

        if elem[1] > ymax:
            ymax = elem[1]
        elif elem[1] < ymin:
            ymin = elem[1]

    # print('X Max: ', xmax, '\nX Min: ', xmin)
    # print('YMax: ', ymax, '\nY Min: ', ymin)

    return xmax, xmin, ymax, ymin

def extrair_escolas_reg(tree):
    escolas = fiona.open("Mapas_sim/shapes_sim_meters/escola_metros.shp")
    # print (escolas.schema)
    listaEscolas = []

    for escola in escolas:
        x, y = escola['geometry']['coordinates']

        t = AABB([(x, x), (y, y)])

        if(tree.does_overlap(t)):
            listaEscolas.append(escola)


    return listaEscolas, escolas

def extrair_saude_reg(tree):
    saude = fiona.open("Mapas_sim/shapes_sim_meters/saude_metros.shp")
    # print (saude.schema)
    listaSaude = []

    for unidade in saude:
        x, y = unidade['geometry']['coordinates']

        t = AABB([(x, x), (y, y)])

        if(tree.does_overlap(t)):
            listaSaude.append(unidade)

    return listaSaude, saude

def extrair_onibus_reg(tree):
    onibus = fiona.open("Mapas_sim/shapes_sim_meters/ponto_onibus_metros.shp")
    # print (onibus.schema)

    listaOnibus = []
    for linha in onibus:
        for ponto in linha['geometry']['coordinates']:

            x, y = ponto
            t = AABB([(x, x), (y, y)])

            if(tree.does_overlap(t)):
                listaOnibus.append(linha)
                break

    return listaOnibus, onibus



# More?
