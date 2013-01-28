#!/usr/bin/env python
# coding: utf-8

import sys
import pairlist
import numpy
import math
import numpy.linalg
def rint(x):
    return math.floor(x+0.5)



def wrap(v,box):
    r = numpy.zeros(3)
    for i in range(len(v)):
        r[i] = v[i] - rint(v[i]/box[i])*box[i]
    return r


def loadNX4A(file):
    xyz = []
    while True:
        line = file.readline()
        if len(line) == 0:
            break
        columns = line.split()
        if len(columns)>0:
            if columns[0] in ("@NX4A","@AR3A"):
                line = file.readline()
                nmol = int(line)
                for i in range(nmol):
                    line = file.readline()
                    columns = numpy.array(map(float,line.split()))
                    xyz.append(columns)
            elif columns[0] == "@BOX3":
                line = file.readline()
                box = numpy.array(map(float,line.split()))
    return box,xyz

def usage():
    print "usage: %s [-r distance] lattice.nx4a < dislocated.nx4a" % sys.argv[0]
    sys.exit(1)

argc = len(sys.argv)
basebox,basexyz = loadNX4A(open(sys.argv[argc-1],"r"))
rc = 1.0
if argc > 2:
    if sys.argv[1] == "-r":
        rc = float(sys.argv[2])
    else:
        usage()

nx = int(math.floor(basebox[0]/rc))
ny = int(math.floor(basebox[1]/rc))
nz = int(math.floor(basebox[2]/rc))
grid = (nx,ny,nz)
baseresidents = pairlist.ArrangeAddress(basexyz,grid,basebox)
box,xyz = loadNX4A(sys.stdin)
residents = pairlist.ArrangeAddress(xyz,grid,box)
vmrk = dict()
for addr in residents:
    mols = residents[addr]
    natives = pairlist.neighbors(addr,baseresidents,grid)
    for m in mols:
        xm = xyz[m]
        vmrk[m] = 0
        for n in natives:
            xn = basexyz[n]
            d = xm[0:3] - xn[0:3]
            d = wrap(d,box)
            if numpy.linalg.norm(d) < rc:
                vmrk[m] = 1
        
print "@VMRK"
print len(xyz)
for i in range(len(xyz)):
    print vmrk[i]

                
                
            
            
