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

dy = 1
dx = math.sqrt(3.)/2
dz = math.sqrt(2./3.)

grid[0]*=2
box = dx*grid[0],dy*grid[1],dz*grid[2]
nmol = grid[0]*grid[1]*grid[2]

#molecular positions
#HB direction vectors
diry = numpy.arange(grid[0]*grid[2]).reshape(grid[0],grid[2])
dirz = numpy.arange(grid[0]*grid[1]).reshape(grid[0],grid[1])
for iz in range(grid[2]):
    for ix in range(grid[0]):
        diry[ix,iz] = random.randint(0,1)
for iy in range(grid[1]):
    for ix in range(grid[0]):
        dirz[ix,iy] = random.randint(0,1)

print "@BOX3"
print box[0],box[1],box[2]
print "@AR3A"
print nmol
count = 0
residents = dict()
for iz in range(grid[2]):
    for iy in range(grid[1]):
        for ix in range(grid[0]):
            print ix*dx+(iz%2)*dx*2/3,iy*dy+ix*dy/2,iz*dz
            residents[(ix,iy,iz)] = count
            count += 1
print "@NGPH"
print nmol
for iz in range(grid[2]):
    for iy in range(grid[1]):
        for ix in range(grid[0]):
            me = residents[(ix,iy,iz)]
            if diry[ix,iz]:
                n1 = residents[(ix,(iy+1)%grid[1],iz)]
            else:
                n1 = residents[(ix,(iy-1+grid[1])%grid[1],iz)]
            if dirz[ix,iy]:
                n2 = residents[(ix,iy,(iz+1)%grid[2])]
            else:
                n2 = residents[(ix,iy,(iz-1+grid[2])%grid[2])]
            print me,n1
            print me,n2
print -1,-1
