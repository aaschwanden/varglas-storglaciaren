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
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(filename, 0)
    layer = data_source.GetLayer(0)
    srs=layer.GetSpatialRef()
    cnt = layer.GetFeatureCount()
    x = []
    y = []
    for pt in range(0, cnt):
        feature = layer.GetFeature(pt)
        geometry = feature.GetGeometryRef()
        points = geometry.GetPoints()
        for point in points:
            x.append(point[0])
            y.append(point[1])

    return np.asarray(y), np.asarray(x)


# Set up the option parser
description = '''A script to a shapefile into comma-separated value (csv) format.'''
parser = ArgumentParser()
parser.description = description
parser.add_argument("FILE", nargs=2)

options = parser.parse_args()
args = options.FILE

filename = args[0]
outfilename = args[1]

y, x = read_shapefile(filename)
data = np.vstack((y, x))
header = '# EPSG:3021\n# y (northing, m), x (easting, m)'
np.savetxt(outfilename, data.transpose(), delimiter=",", header=header)

