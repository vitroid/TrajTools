#!/usr/bin/env python
# coding: utf-8

#generate pseudo-disordered HCP ice
import sys
import random
import math
import numpy

#normal stacking layer (AB layers) is on Z axis.
#Zigzag layer of Nakata's ice is on X axis.
if len(sys.argv) >= 4:
    grid = map(int,sys.argv[1:4])
    if len(sys.argv) == 5:
        random.seed(int(sys.argv[4]))

dx = 1.
dy = 1.
dz = math.sqrt(2)/2

grid[2] *= 2
box = dx*grid[0],dy*grid[1],dz*grid[2]
nmol = grid[0]*grid[1]*grid[2]

#molecular positions
#HB direction vectors
dirx = numpy.arange(grid[1]*grid[2]).reshape(grid[1],grid[2])
diry = numpy.arange(grid[0]*grid[2]).reshape(grid[0],grid[2])
for iz in range(grid[2]):
    for ix in range(grid[0]):
        diry[ix,iz] = random.randint(0,1)
for iz in range(grid[2]):
    for iy in range(grid[1]):
        dirx[iy,iz] = random.randint(0,1)

print "@BOX3"
print box[0],box[1],box[2]
print "@AR3A"
print nmol
count = 0
residents = dict()
for iz in range(grid[2]):
    for iy in range(grid[1]):
        for ix in range(grid[0]):
            print ix*dx+(iz%2)*dx/2.,iy*dy+(iz%2)*dy/2.,iz*dz
            residents[(ix,iy,iz)] = count
            count += 1
print "@NGPH"
print nmol
for iz in range(grid[2]):
    for iy in range(grid[1]):
        for ix in range(grid[0]):
            me = residents[(ix,iy,iz)]
            if dirx[iy,iz]:
                n1 = residents[((ix+1)%grid[0],iy,iz)]
            else:
                n1 = residents[((ix-1+grid[0])%grid[0],iy,iz)]
            if diry[ix,iz]:
                n2 = residents[(ix,(iy+1)%grid[1],iz)]
            else:
                n2 = residents[(ix,(iy-1+grid[1])%grid[1],iz)]
            print me,n1
            print me,n2
print -1,-1
