#!/usr/bin/env python
# coding: utf-8

import sys
import rotation
import math
import itertools
import numpy
import numpy.linalg

def usage():
    print "usage: %s -y|-b" % sys.argv[0]
    print "  -y\tyaplot."
    print "  -b\tbond angles."
    sys.exit(1)


def rint(x):
    return math.floor(x+0.5)


<<<<<<< HEAD

def wrap(v,box):
    r = numpy.zeros(3)
    for i in range(len(v)):
        r[i] = v[i] - rint(v[i]/box[i])*box[i]
    return r



def output_yaplot(com,edges,box):
    print "y 2"
    print "@ 3"
    for edge in edges:
        i,j = edge
        d = com[j] - com[i]
        d = wrap(d,box)
=======
def output_yaplot(mols,edges,box):
    com = []
    print "y 1"
    print "@ 2"
    for i in range(len(mols)):
        sx = 0
        sy = 0
        sz = 0
        sm = 0
        for j in range(len(mols[i])):
            label,x,y,z,mass = mols[i][j]
            sx += x*mass
            sy += y*mass
            sz += z*mass
            sm += mass
        com.append((sx/sm,sy/sm,sz/sm))
        for j in range(len(mols[i])):
            label,x,y,z,mass = mols[i][j]
            if label in ("H","O"):
                for k in range(j):
                    labelk,xk,yk,zk,massk = mols[i][k]
                    if labelk in ("H","O"):
                        print "l",x,y,z,xk,yk,zk
    for edge in edges:
        if len(edge) == 3:
            i,j,dir = edge
        else:
            i,j = edge
            dir = "="
        dx = com[j][0] - com[i][0]
        dy = com[j][1] - com[i][1]
        dz = com[j][2] - com[i][2]
        dx -= rint( dx/box[0] )*box[0]
        dy -= rint( dy/box[1] )*box[1]
        dz -= rint( dz/box[2] )*box[2]
        if dir == "<":
            print "y 3"
            print "@ 4"
        elif dir == ">":
            print "y 4"
            print "@ 5"
        elif dir == "x":
            print "y 5"
            print "@ 6"
        else:
            print "y 2"
            print "@ 3"
>>>>>>> .
        print "l",com[i][0],com[i][1],com[i][2],com[i][0]+dx,com[i][1]+dy,com[i][2]+dz
    print




def output_bondangles(com,edges,box):
    nei = [set() for i in range(len(com))]
    for edge in edges:
        i,j = edge
        nei[i].add(j)
        nei[j].add(i)
    print "@VALU"
    print len(nei),4
    for i in range(len(nei)):
        for j,k in itertools.combinations(nei[i],2):
            v1 = com[j] - com[i]
            v1 = wrap(v1,box)
            v1 /= numpy.linalg.norm(v1)
            v2 = com[k] - com[i]
            v2 = wrap(v2,box)
            v2 /= numpy.linalg.norm(v2)
            print i,j,k,"%6.1f" % (math.acos(numpy.dot(v1,v2))*180./math.pi)
    print -1,-1,-1,0

mode = "-y"
if sys.argv[1] == "-b":
    mode = "-b"  # bond angle calculations

com = []
edges = []
while True:
    #read a line, anyway
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns) == 0:
        continue
    #look up tags
    tag = columns[0]
    if tag in ('@BOX3',):
        line = sys.stdin.readline()
        columns = line.split()
        box = numpy.array(map(float,columns[0:3]))
    elif tag in  ('@NGPH', ):
        #get the first line == number of molecules
        edges = []
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        while True:
            line = sys.stdin.readline()
            columns = line.split()
            x,y = map(int,columns[0:2])
            if x < 0:
                break
            edges.append((x,y))
<<<<<<< HEAD
    elif tag in  ('@AR3A', '@WTG6', '@WTG3', '@NX4A', '@NX3A'):
=======
    elif tag in  ('@DGPH', ):
        #get the first line == number of molecules
        edges = []
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        while True:
            line = sys.stdin.readline()
            columns = line.split()
            x,y = map(int,columns[0:2])
            if x < 0:
                break
            edges.append((x,y,columns[2]))
    elif tag in  ('@WTG6', '@WTG3', '@NX4A', '@NX3A'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])

        #read molecular info
        mols = []
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            cx,cy,cz = map(float,columns[0:3])
            cx -= rint(cx/box[0])*box[0]
            cy -= rint(cy/box[1])*box[1]
            cz -= rint(cz/box[2])*box[2]
            #last data, i-th molecule, 6 velocities
            if tag == '@WTG6':
                rotmat = map(float,columns[3:12])
            elif tag in ('@WTG3', '@NX4A'):
                quat = map(float,columns[3:7])
                rotmat = quat2rotmat(quat)
            elif tag in ('@NX3A'):
                euler = map(float,columns[3:7])
                quat = euler2quat(euler)
                rotmat = quat2rotmat(quat)
            if mode in ("-y", ):
                mol = defr[id08]
                intra = []
                for site in mol[0]:
                    x,y,z,mass,label = site
                    xx = cx + x*rotmat[0] + y*rotmat[1] + z*rotmat[2]
                    yy = cy + x*rotmat[3] + y*rotmat[4] + z*rotmat[5]
                    zz = cz + x*rotmat[6] + y*rotmat[7] + z*rotmat[8]
                    intra.append((label, xx,yy,zz,mass))
                mols.append(intra)
    elif tag in  ('@AR3A',):
>>>>>>> .
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        atoms = []
        #read molecular info
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            cx,cy,cz = map(float,columns[0:3])
            if mode in ("-y", "-b"):
                com.append(numpy.array((cx,cy,cz)))
    if len(com)>0 and len(edges)>0:
        if mode in ("-y", "-b"):
            if mode == "-y":
                output_yaplot(com,edges,box)
            elif mode == "-b":
                output_bondangles(com,edges,box)
