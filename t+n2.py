#!/usr/bin/env python
# coding: utf-8

import sys
from rotation import *
import math

def usage():
    print "usage: %s -m|-3|-4" % sys.argv[0]
    print "  -y\tyaplot."
    sys.exit(1)


def rint(x):
    return math.floor(x+0.5)


def output_yaplot(mols,edges,box):
    com = []
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
    print "@ 3"
    for edge in edges:
        i,j = edge
        dx = com[j][0] - com[i][0]
        dy = com[j][1] - com[i][1]
        dz = com[j][2] - com[i][2]
        dx -= rint( dx/box[0] )*box[0]
        dy -= rint( dy/box[1] )*box[1]
        dz -= rint( dz/box[2] )*box[2]
        print "l",com[i][0],com[i][1],com[i][2],com[i][0]+dx,com[i][1]+dy,com[i][2]+dz
    print


mode = "-y"

ncmp = 1 #number of components
icmp = 0
defr = dict()
mols = []
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
    if tag in  ('@NCMP',):
        line = sys.stdin.readline()
        ncmp = int(line)
        atoms = []
        icmp = 0
    if tag in  ('@ID08',):
        line = sys.stdin.readline()
        id08 = line[0:8]
    elif tag in ('@BOX3',):
        line = sys.stdin.readline()
        columns = line.split()
        box = map(float,columns[0:3])
    elif tag in  ('@DEFR',):
        line = sys.stdin.readline()
        id = line[0:8]
        line = sys.stdin.readline()
        nsite = int(line)
        sites = []
        intr  = []
        for site in range(nsite):
            line = sys.stdin.readline()
            columns = line.split()  # x,y,z,mass,label
            columns[0:4] = map(float,columns[0:4])
            sites.append(columns)
        for site in range(nsite):
            line = sys.stdin.readline()
            columns = line.split() #eps, sig, charge
            columns = map(float,columns[0:3])
            intr.append(columns)
        defr[id] = (sites,intr)
    elif tag in  ('@DEFP',):
        line = sys.stdin.readline()
        id = line[0:8]
        line = sys.stdin.readline()
        nsite = int(line)
        sites = []
        intr  = []
        for site in range(nsite):
            line = sys.stdin.readline()
            columns = line.split()  # mass,label
            columns = [0.0, 0.0, 0.0, float(columns[0]), columns[1]]
            sites.append(columns)
        for site in range(nsite):
            line = sys.stdin.readline()
            columns = line.split() #eps, sig, charge
            columns = map(float,columns[0:3])
            intr.append(columns)
        defr[id] = (sites,intr)
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
            if mode in ("-y", ):
                mol = defr[id08]
                intra = []
                for site in mol[0]:
                    x,y,z,mass,label = site
                    atoms.append((label, cx,cy,cz))
        if mode == "-m":
            icmp += 1
            if icmp == ncmp:
                output_mdview(atoms)
                icmp = 0
                atoms = []
    if mode == "-y" and len(mols)>0 and len(edges)>0:
        icmp += 1
        if icmp == ncmp:
            output_yaplot(mols,edges,box)
            icmp = 0
                            
