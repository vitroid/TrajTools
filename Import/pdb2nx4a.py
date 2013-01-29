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
    #i$B<4$r(Bx$B<4$K0\$92sE>$N<4$O!"(Bi$B$H(Bx$B$N(B2$BJ,LL$H$J$k!#(B
    #j$B<4$r(By$B<4$K0\$92sE>$N<4$O!"(Bj$B$H(By$B$N(B2$BJ,LL$H$J$k!#(B
    #$B$=$7$F!"$=$l$i$rF1;~$K$_$?$92sE>$N<4$O!"$=$l$i$N8r@~$H$J$k!#(B
    #$B8r@~$O!"(B2$B$D$NLL$NK!@~$N$$$:$l$H$bD>8r$9$k(B=$B30@Q$G$"$k!#(B
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

atoms = dict()
nei = dict()

for line in sys.stdin:
    columns = line.split()
    if columns[0] == 'HETATM':
        label = columns[1]
        #last 3 numbers are coordinates
        xyz = numpy.array(map(float,columns[len(columns)-3:len(columns)]))
        atoms[label] = xyz
    elif columns[0] == "CONECT":
        i = columns[1]
        for j in columns[2:len(columns)]:
            if not nei.has_key(i):
                nei[i] = []
            nei[i].append(j)

print "@NX4A"
print len(atoms)/3
for n in nei:
    if len(nei[n]) == 2: #oxygen
        i,j,k = n, nei[n][0], nei[n][1]
        oh1 = atoms[j] - atoms[i]
        oh2 = atoms[k] - atoms[i]
        k = oh1+oh2
        k /= norm(k)
        j = oh2-oh1
        j /= norm(j)
        i = numpy.cross(j,k)
        mat = numpy.matrix((i,j,k)).T
        quat = ohvectors2quat(atoms[j] - atoms[i], atoms[k] - atoms[i])
        quat2 = rotation.rotmat2quat_numpy(mat)
        print quat,quat2
        #print atoms[j] - atoms[i], atoms[k] - atoms[i], quat
        for i in atoms[i]:
            print i,
        for i in quat:
            print i,
        print
