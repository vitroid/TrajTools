#!/usr/bin/env python

import numpy
import sys
import math

#remove warping rings

def LoadAR3A(file):
    coord = []
    line = file.readline()
    columns = line.split()
    nmol = int(columns[0])
    coord = []
    for i in range(nmol):
        line = file.readline()
        c = numpy.array([float(x) for x in line.split()][0:3])
        coord.append(c)
    return coord



def LoadBOX3(file):
    line = file.readline()
    a,b,c = [float(x) for x in line.split()]
    return (a,b,c)


#format is same as @RSET
def LoadRNGS(file,debug=0):
    line = file.readline()
    n = int(line)
    rings = []
    while True:
        line=file.readline()
        if len(line) == 0:
            break
        if debug: print "#",line,
        columns = [int(x) for x in line.split()]
        if debug: print "#",line,columns,n
        if columns[0] == 0:
            break
        nodes = columns[1:]
        rings.append(nodes)
    return n,rings





def rint(x):
    return math.floor(x+0.5)


coord = []
box = []
rings = []
rsets = []

while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if columns[0] in ("@AR3A","@NX4A"):
        coord = LoadAR3A(sys.stdin)
    elif columns[0] == "@BOX3":
        box = LoadBOX3(sys.stdin)
    elif columns[0] == "@RNGS":
        n,rings = LoadRNGS(sys.stdin)
    elif columns[0] == "@RSET":
        nr,rsets = LoadRNGS(sys.stdin)
    if len(coord)>0 and len(rings) > 0 and len(rsets) > 0:
        break


print "@BOX3"
print box[0],box[1],box[2]
print "@AR3A"
print len(rsets)
for rset in rsets:
    vertices = set()
    for r in rset:
        vertices |= set(rings[r])
    vertices = tuple(vertices)
    #first vertex is the origin
    com = numpy.zeros(3)
    for v in vertices:
        x = coord[v] - coord[vertices[0]]
        for dim in range(3):
            x[dim] -= rint(x[dim]/box[dim])*box[dim]
        com += x
    com /= len(vertices)
    com += coord[vertices[0]]
    print com[0],com[1],com[2]


