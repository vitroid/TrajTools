#!/usr/bin/env python
# coding: utf-8

import sys
from rotation import *
import math
import pairlist
import itertools
import numpy
import numpy.linalg

def usage():
    print "usage: %s -m|-3|-4" % sys.argv[0]
    print "  -m\tmdview."
    print "  -y\tyaplot. (no bonds)"
    print "  -3\tnx3a."
    print "  -4\tnx4a."
    print "  -n x\tngph with O-H threshold of x Å."
    sys.exit(1)


def rint(x):
    return math.floor(x+0.5)



def wrap(v,box):
    r = numpy.zeros(3)
    for i in range(len(v)):
        r[i] = v[i] - rint(v[i]/box[i])*box[i]
    return r



if len(sys.argv) >= 2:
    mode = sys.argv[1]
else:
    usage()
if mode == "-n":
    thres = float(sys.argv[2])


def output_mdview(atoms):
    print "-center 0 0 0"
    print "-fold"
    print len(atoms)
    for label,x,y,z in atoms:
        print label,x,y,z



def output_yaplot(mols,box):
    print "y 1"
    print "@ 2"
    print "r 0.1"
    for intra in mols:
        for a1,a2 in itertools.combinations(intra,2):
            if a1[0] == "O" and a2[0] == "H":
                d = a2[1] - a1[1]
                d = wrap(d,box) + a1[1]
                print "l",a1[1][0],a1[1][1],a1[1][2],d[0],d[1],d[2]
    print



ncmp = 1 #number of components
icmp = 0
defr = dict()
atoms = []
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
        if mode in ("-3","-4"):
            print "@ID08"
            print id08
    elif tag in ('@BOX3',):
        line = sys.stdin.readline()
        columns = line.split()
        box = numpy.array(map(float,columns[0:3]))
        if mode == "-m":
            print "-length '(%s, %s, %s)'" % (box[0],box[1],box[2])
        elif mode == "-y":
            pass
        else:
            print "@BOX3"
            print box[0],box[1],box[2]
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
    elif tag in  ('@WTG6', '@WTG3', '@NX4A', '@NX3A'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])

        if mode == "-3":
            print "@NX3A"
        elif mode == "-4":
            print "@NX4A"
        if mode in ("-3", "-4"):
            print nmol
        #read molecular info
        mols = []
        com = []
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            c = numpy.array(map(float,columns[0:3]))
            if mode == "-y":
                c = wrap(c,box)
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
            if mode in ("-m", "-n", "-y"):
                mol = defr[id08]
                intra = []
                sx = 0
                sy = 0
                sz = 0
                sm = 0
                for site in mol[0]:
                    x,y,z,mass,label = site
                    xx = c[0] + x*rotmat[0] + y*rotmat[1] + z*rotmat[2]
                    yy = c[1] + x*rotmat[3] + y*rotmat[4] + z*rotmat[5]
                    zz = c[2] + x*rotmat[6] + y*rotmat[7] + z*rotmat[8]
                    sx += xx*mass
                    sy += yy*mass
                    sz += zz*mass
                    sm +=    mass
                    atoms.append((label, xx,yy,zz))
                    intra.append((label, numpy.array((xx,yy,zz))))
                mols.append(intra)
                com.append((sx/sm,sy/sm,sz/sm))
            elif mode == "-3":
                euler = quat2euler(rotmat2quat(rotmat))
                print c[0],c[1],c[2],euler[0],euler[1],euler[2]
            elif mode == "-4":
                quat = rotmat2quat(rotmat)
                print c[0],c[1],c[2],quat[0],quat[1],quat[2],quat[3]
        if mode == "-m":
            icmp += 1
            if icmp == ncmp:
                output_mdview(atoms)
                icmp = 0
                atoms = []
        if mode == "-y":
            icmp += 1
            if icmp == ncmp:
                output_yaplot(mols,box)
                icmp = 0
                atoms = []
        if mode == "-n":
            print "@NGPH"
            print len(mols)
            for i,j in pairlist.pairlist(com,thres+1.1,box):
                    dmin = 999999.
                    dirmin  = 0
                    for si in mols[i]:
                        for sj in mols[j]:
                            if si[0][0] == "O" and sj[0][0] == "H":
                                dir = -1
                            if si[0][0] == "H" and sj[0][0] == "O":
                                dir = +1
                            if (si[0][0] == "O" and sj[0][0] == "H") or (si[0][0] == "H" and sj[0][0] == "O"):
                                d = si[1]-sj[1]
                                d = wrap(d,box)
                                d = numpy.linalg.norm(d)
                                if d < dmin:
                                    dmin = d
                                    dirmin = dir
                    if dmin < thres:
                        if dirmin > 0:
                            print i,j
                        else:
                            print j,i
            print -1,-1
    elif tag in  ('@AR3A',):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        #read molecular info
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            cx,cy,cz = map(float,columns[0:3])
            if mode in ("-m", "-n"):
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
                            
