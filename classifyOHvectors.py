#!/usr/bin/env python
# coding: utf-8
#秩序氷IIの座標を読みこみ、O-Hベクトルの向きとc軸との内積をとって、その大きさでベクトルを分類する。
#垂直ならpiller
#環の水素結合は水平に近いはず(椅子と平面も識別する)
#らせんのベクトルはもっとc軸に沿っているはず。
#これらを4種類に分類して、@BMRK形式で出力する。


import sys
import numpy
import rotation_numpy
import pairlist
import numpy.linalg
import math

def rint(x):
    return math.floor(x+0.5)



def wrap(v,box):
    r = numpy.zeros(len(v))
    for i in range(len(v)):
        r[i] = v[i] - rint(v[i]/box[i])*box[i]
    return r



#TIP4P intramolecular coordinates
O = numpy.array([0,0,                       -6.50980307353661025e-02])
H1 = numpy.array([0,  7.56950327263661182e-01,  5.20784245882928820e-01])
H2 = numpy.array([0, -7.56950327263661182e-01, 5.20784245882928820e-01])
OH1 = H1 - O
OH2 = H2 - O
#unit vector of c-axis
Caxis = numpy.array([0,0,1])
#classification of inner products
# 144 0.06 flat ring
# 144 0.23 chair ring
# 144 0.50 spiral
# 144 0.96 pillar
category = dict()
category[6] = 1
category[23] = 2
category[50] = 3
category[96] = 4
category[-6] = -1
category[-23] = -2
category[-50] = -3
category[-96] = -4



while True:
    #read a line from stdin
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns) > 0:
        #first element of the line
        tag = columns[0]
        if tag in ("@BOX3",):
            #cell size
            line = sys.stdin.readline()
            box = numpy.array(map(float, line.split()))
        if tag in ("@NX3A", "@NX4A"):
            #rigid water molecules
            line = sys.stdin.readline()
            #next line is number of molecules
            nmol = int(line)
            coms = []
            rotmats = []
            for i in range(nmol):
                #read x,y,z, and orientation (NX3A:euler, NX4A:quat)
                line = sys.stdin.readline()
                r = map(float, line.split())
                if tag == "@NX3A":
                    #xyz+euler angles
                    euler = numpy.array(r[3:6])
                    q = rotation_numpy.euler2quat(euler)
                else:
                    #xyz + quaternion
                    q = r[3:7]
                #store the rotation matrix and coordinate in arrays.
                rotmats.append(rotation_numpy.quat2rotmat(q))
                coms.append(numpy.array(r[0:3]))

#Fast pairlist maker
rc = 3.0
pairs = pairlist.pairlist(coms,rc,box)
# lookup HB pairs
print "@BMRK"
print nmol
for i,j in pairs:
    d = wrap( coms[j] - coms[i], box )
    ih1 = numpy.dot(rotmats[i], H1)
    ih2 = numpy.dot(rotmats[i], H2)
    di1 = numpy.linalg.norm( d - ih1 )
    di2 = numpy.linalg.norm( d - ih2 )
    di = min(di1,di2)
    jh1 = numpy.dot(rotmats[j], H1)
    jh2 = numpy.dot(rotmats[j], H2)
    dj1 = numpy.linalg.norm( d + jh1 )
    dj2 = numpy.linalg.norm( d + jh2 )
    dj = min(dj1,dj2)
    if di < dj and di < 2.45:
        #i's H is pointing to j
        #relative vector
        d = wrap( coms[j] - coms[i], box )
        d /= numpy.linalg.norm(d)
        ip = numpy.dot(d,Caxis)
        ip = int(rint(ip*100))
        print i,j,category[ip]
    elif dj < di and dj < 2.45:
        d = wrap( coms[i] - coms[j], box )
        d /= numpy.linalg.norm(d)
        ip = numpy.dot(d,Caxis)
        ip = int(rint(ip*100))
        print j,i,category[ip]
print -1,-1,-1
# 144 -0.059 flat ring
# 144 -0.234 chair ring
# 144 -0.501 spiral
# 144 -0.961 pillar
# 144 0.059 flat ring
# 144 0.234 chair ring
# 144 0.501 spiral
# 144 0.961 pillar

