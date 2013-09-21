#!/usr/bin/env python
# Copyright (C) 2013 Andy Aschwanden
#

from argparse import ArgumentParser
import numpy as np


def read_shapefile(filename):
    '''
    Reads lat / lon from a ESRI shape file.

    Paramters
    ----------
    filename: filename of ESRI shape file.

    Returns
    -------
    lat, lon: array_like coordinates
    
    '''
    import ogr
    import osr
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(filename, 0)
    layer = data_source.GetLayer(0)
    srs=layer.GetSpatialRef()
    cnt = layer.GetFeatureCount()
    x = []
    y = []
    names = []
    for pt in range(0, cnt):
        feature = layer.GetFeature(pt)
        try:
            name = feature.name
        except:
            name = str(pt)
        geometry = feature.GetGeometryRef()
        x.append(geometry.GetX())
        y.append(geometry.GetY())
        names.append(name)

    return np.asarray(y), np.asarray(x), np.array(names, 'O')


# Set up the option parser
description = '''A script to convert a shapefile into gmsh geo format.'''
parser = ArgumentParser()
parser.description = description
parser.add_argument("FILE", nargs=2)

options = parser.parse_args()
args = options.FILE

filename = args[0]
outfilename = args[1]

y, x, name = read_shapefile(filename)
data = np.vstack((y, x))

f = open(outfilename, 'w')
print >> f, 'Mesh.Algorithm=5; \n'
for k in range(0,len(y)):
    out = 'Point(%g)={%14.7e,%14.7e,0.0,%g};' % (k+1 ,y[k], x[k], 18.0)
    print >> f, out


s = str(range(0, len(y))).split('[')[1].split(']')[0]
out = 'Spline(1)={%s};' % s
print >> f, out
    
f.close()
