#!/usr/bin/env python
###############################################################################
#
# Project: svxdem.py
# Purpose: svxdem.py (SURVEX-DEM) creates svx files from raster DEMs exported from 
# GRASS-GIS as ASCII files
# This program is licenced under the MIT License
#          
# Author:   Carlos H. Grohmann, carlos.grohmann@gmail.com
#
###############################################################################
# Copyright (c) 2009-2019, Carlos H. Grohmann
# 
###############################################################################


# import modules
import os, sys, math

# =============================================================================
def Usage():
    print ('------------------------------------------------------------------')
    print ('svxdem.py (SURVEX-DEM) creates svx files from raster DEMs exported') 
    print ('from GRASS-GIS as ASCII files')
    print ('')
    print ('like this:')
    print ('r.out.ascii input=topo output=.ascii')
    print ('')
    print ('Usage: svxdem.py -i infile -o outfile -p UTM22S')
    print ('------------------------------------------------------------------')
    sys.exit(1)

# =============================================================================
# Parse command line arguments.
# =============================================================================
import optparse

p = optparse.OptionParser()
p.add_option('--indem', '-i', default=None)
p.add_option('--outdem', '-o', default=None)
p.add_option('--proj', '-p', default=None)
options, arguments = p.parse_args()
# if no input, call Usage()
if options.indem is None:
	Usage()
# if no output, default to the same filename as input, but with svx extension
if options.outdem is None:
    options.outdem = options.indem.split('.')[0]+'.svx'

outbasename = options.outdem.split('.')[0]

print ('------------------------------------------------------------------')
print ('< svxdem.py - (c) 2009-2019, Carlos H. Grohmann >')
print ('------------------------------------------------------------------')

# =============================================================================
# open input file 
# infile = open(options.indem, 'rU')

# GRASS' ASCII file has a standard structure, so we read values for
# variables first, then iterate through the rest of the file 
# to get the cell values
with open(options.indem) as dem_ascii:
    north = float(dem_ascii.readline().split(': ')[1])
    south = float(dem_ascii.readline().split(': ')[1])
    east = float(dem_ascii.readline().split(': ')[1])
    west = float(dem_ascii.readline().split(': ')[1])
    nrows = int(dem_ascii.readline().split(': ')[1])
    ncols = int(dem_ascii.readline().split(': ')[1])
    cells = dem_ascii.readlines()

# print(north, south, east, west, rows, cols)
# print(cells)

# calculate grid spacing 
grid_ns=(north-south)/nrows
grid_ew=(east-west)/ncols

print ('')
print ('')
print ('Dataset limits:')
print ('north: {:07.3f}'.format(north))
print ('south: {:07.3f}'.format(south))
print ('east: {:06.3f}'.format(east))
print ('west: {:06.3f}'.format(west))
print ('rows: {:d}'.format(nrows))
print ('cols: {:d}'.format(ncols))
print ('')
print ('grid_ns: {:03.2f}'.format(grid_ns))
print ('grid_ew: {:03.2f}'.format(grid_ew))
print ('')

# output file
with open(options.outdem, 'w') as dem_svx:
    # create header 
    dem_svx.write(';********************   SURVEX-DEM   ********************\n')
    dem_svx.write(';Survex terrain data created by SURVEX-DEM (svxdem.py)\n')
    dem_svx.write(';based on a DEM exported from GRASS-GIS as an ASCII file\n') 
    dem_svx.write('\n')
    dem_svx.write(';SURVEX-DEM (c) 2009-2019, Carlos H. Grohmann. IEE-USP - Brazil\n')
    dem_svx.write(';https://github.com/CarlosGrohmann\n')
    dem_svx.write(';This program is licensed under LGPL 2.0 or later\n')
    dem_svx.write('\n')
    dem_svx.write('\n')
    dem_svx.write('\n')
    dem_svx.write(';Surface data for Survex\n')
    dem_svx.write('\n')

    if options.proj:
        dem_svx.write('*cs {}\n'.format(options.proj))
        dem_svx.write('*cs out {}\n'.format(options.proj))

    dem_svx.write('\n')
    dem_svx.write('*begin {}\n'.format(outbasename))

# ------------------------
    # create fixed stations
    rrow = range(nrows)
    rcol = range(ncols)

    n = north
    for row in rrow:
        w = west
        for col in rcol:
            w = w + grid_ew
            elev = float(cells[row].strip().split(' ')[col])
            # print (row, col, w, n, elev)
            dem_svx.write('*fix N{:d}E{:d} {:06.1f} {:07.1f} {:05.2f}\n'.format(row, col, w, n, elev))
        n = n - grid_ns

    ## option using enumerate()
    # n = north
    # for row in enumerate(cells):
    #     w = west
    #     for col, elev in enumerate(row[1].strip().split(' ')):
    #         w = w + grid_ew
    #         # print (row[0], col, w, n, elev)
    #         dem_svx.write('*fix N{:d}E{:d} {:06.1f} {:07.1f} {:05.2f}\n'.format(row[0], col, w, n, float(elev)))
    #     n = n - grid_ns

# ------------------------
    # create nosurvey shots
    dem_svx.write('\n')
    dem_svx.write('*data nosurvey station\n')
    dem_svx.write('*flags surface\n')

    dem_svx.write(';by row (row/col)\n')
    for row in rrow:
        for col in rcol:
            dem_svx.write('N{:d}E{:d}\n'.format(row, col))
        dem_svx.write('\n')

    dem_svx.write(';by col (col/row)\n')
    for col in rcol:
        for row in rrow:
            dem_svx.write('N{:d}E{:d}\n'.format(row, col))
        dem_svx.write('\n')

# ------------------------
    dem_svx.write('*end {}\n'.format(outbasename))


print ('')
print ('Done! ')


