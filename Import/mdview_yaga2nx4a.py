#!/usr/bin/env python

import numpy
from numpy.linalg import *
from math import *
import rotation_numpy

def mycross(a,b):
    if norm(a) < 0.01 or norm(b) < 0.01:
        return None
    c = numpy.cross(a,b)
    if norm(c) < 0.01:
        return None
    return c

#oh1, oh2: intermolecular OH vectors
def ohvectors2quat(oh1,oh2):
    k = oh1+oh2
    k /= norm(k)
    j = oh2-oh1
    j /= norm(j)
    i = numpy.cross(j,k)
    #i軸をx軸に移す回転の軸は、iとxの2分面となる。
    #j軸をy軸に移す回転の軸は、jとyの2分面となる。
    #そして、それらを同時にみたす回転の軸は、それらの交線となる。
    #交線は、2つの面の法線のいずれとも直交する=外積である。
    ex = numpy.array((1,0,0))
    ey = numpy.array((0,1,0))
    ez = numpy.array((0,0,1))

    axis = mycross(i-ex,j-ey)
    if axis is None:
        axis = mycross(i-ex,k-ez)
        if axis is None:
            axis = mycross(k-ez,j-ey)
            if axis is None:
                #no rotation
                return 1.0, 0.0, 0.0, 0.0
    axis /= norm(axis)
    
    x0 = list(ex)
    i0 = i - axis[0]*axis
    x0 -= axis[0]*axis
    if norm(i0) < 0.1:
        x0 = list(ey)
        i0 = j - axis[1]*axis
        x0 -= axis[1]*axis

    i0 /= norm(i0)
    x0 /= norm(x0)
    cosine = numpy.dot(i0,x0)
    if cosine < -1.0 or cosine > 1.0:
        cosh = 0.0
        sinh = 1.0
    else:
        cosh = sqrt((1.0+cosine)*0.5)
        sinh = sqrt(1.0 - cosh**2)
    o = numpy.cross(i0,x0)
    if numpy.dot(o,axis)<0.0:
        sinh = -sinh
    return numpy.array((cosh, -sinh*axis[0], sinh*axis[1],-sinh*axis[2]))





import sys

mols = []
mol = []

for line in sys.stdin:
    columns = line.split()
    if len(columns) == 4:
        name = columns[0]
        #last 3 numbers are coordinates
        xyz = numpy.array(map(float,columns[len(columns)-3:len(columns)]))
        mol.append(xyz)
        if len(mol) == 3:
            mols.append(mol)
            mol = []

print "@NX4A"
print len(mols)
for mol in mols:
    o,h1,h2 = mol[0], mol[1], mol[2]
    com = (16*o+h1+h2)/18
    oh1 = h1 - o
    oh2 = h2 - o
    k = oh1+oh2
    k /= norm(k)
    j = oh2-oh1
    j /= norm(j)
    i = numpy.cross(j,k)
    quat2 = rotation_numpy.rotmat2quat(i,j,k)
    #print atoms[j] - atoms[i], atoms[k] - atoms[i], quat
    for i in com:
        print i,
    for i in quat2:
        print i,
    print
