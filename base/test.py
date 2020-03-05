# from aabbtree import AABB, AABBTree
#
# tree = AABBTree()
# # (xmin, xmax), (ymin, ymax)
# aabb1 = AABB([(0,20), (0,20)])
# aabb2 = AABB([(5,20), (5,10)])
#
# tree.add(aabb1, 'envol')
#
# a = tree.does_overlap(aabb2)
#
# print(a)

#
# x1,y1 = -43.20318199999999, -22.81554220000002
# x2,y2 = transform(inProj,outProj,x1,y1)
# print ("Coordenate(", x2, ",", y2, ")")
#
# inProj = Proj(init='epsg:3857')
# outProj = Proj(init='epsg:4326') # It is equal to WSG
# x3,y3 = transform(inProj,outProj,x2,y2)
#
# x4,y4 = transform(inProj,outProj,x2+50,y2)
# x5,y5 = transform(inProj,outProj,x2-50,y2)
# x6,y6 = transform(inProj,outProj,x2,y2+50)
# x7,y7 = transform(inProj,outProj,x2,y2-50)

import pandas as pd
from pyproj import Proj, transform

outProj = Proj(init='epsg:3857')
inProj = Proj(init='epsg:4326') # It is equal to WSG
