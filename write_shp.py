from pyproj import Proj, transform
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, Polygon

def write_escolas(listaEscolas, escolas):
    sink_schema = escolas.schema.copy()
    with fiona.open(
            'escola_estudo.shp', 'w',
            crs=from_epsg(3857),
            driver=escolas.driver,
            schema=sink_schema,
            ) as sink:

        for e in listaEscolas:
            sink.write(e)


def write_saude(listaSaude, saude):
    sink_schema = saude.schema.copy()
    with fiona.open(
            'saude_estudo.shp', 'w',
            crs=from_epsg(3857),
            driver=saude.driver,
            schema=sink_schema,
            ) as sink:

        for e in listaSaude:
            sink.write(e)


def write_onibus(listaOnibus, onibus):
    sink_schema = onibus.schema.copy()
    with fiona.open(
            'onibus_estudo.shp', 'w',
            crs=from_epsg(3857),
            driver=onibus.driver,
            schema=sink_schema,
            ) as sink:

        for e in listaOnibus:
            sink.write(e)


def write_ocupacao_por_tempo(serie, name, nextX, nextY):
    # Here's an example Shapely geometry
    # poly = Polygon(coordendas)

    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }
    i = 0

    for i in range(0, len(serie)):
        name_ = name + '_' + str(i) + '.shp'
        sink_list = []
        for key in serie[i]:
            if serie[i][key]['area_parque_cm']:
                if serie[i][key]['ocupado']:
                    sink_list.append(serie[i][key])
                    # Write a new Shapefile

        outpath = name_
        with fiona.open(outpath, 'w', crs=from_epsg(3857), driver='ESRI Shapefile', schema=schema) as c:

            for s in sink_list:
                x = s['local_x']
                y = s['local_y']

                p = [ (x, y), (x+nextX, y), (x+nextX, y + nextY), (x, y+nextY)]
                poly = Polygon(p)
                c.write({
                    'geometry': mapping(poly),
                    'properties': {'id': s['id']},
                })


# More comming

# def write_ocupacao_por_tempo(serie, name, nextX, nextY):
#     # Here's an example Shapely geometry
#     # poly = Polygon(coordendas)
#
#     # Define a polygon feature geometry with one attribute
#     schema = {
#         'geometry': 'Polygon',
#         'properties': {'id': 'int'},
#     }
#     i = 0
#     for i in range(0, len(serie)):
#         name = name + '_' + str(i) + '.shp'
#         sink_list = []
#         for key in serie[i]:
#             if serie[i][key]['area_parque_cm']:
#                 if serie[i][key]['ocupado']:
#                     sink_list.append(serie[i][key])
#                     # Write a new Shapefile
#         with fiona.open(name, 'w', crs=from_epsg(3857), driver='ESRI Shapefile', schema=schema) as c:
#
#             for s in sink_list:
#                 x = s['local_x']
#                 y = s['local_y']
#
#                 p = [ (x, y), (x+nextX, y), (x+nextX, y + nextY), (x, y+nextY)]
#                 poly = Polygon(p)
#                 c.write({
#                     'geometry': mapping(poly),
#                     'properties': {'id': s['id']},
#                 })
