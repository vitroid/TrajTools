#!/usr/bin/env python

#make bonds acoording to com-com distances

import sys
import math
import numpy

thres = float(sys.argv[1])

coord = []
box   = []
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if columns[0] == '@BOX3':
        line = sys.stdin.readline()
        a,b,c = map(float, line.split())
        a = numpy.array((a,0,0))
        b = numpy.array((0,b,0))
        c = numpy.array((0,0,c))
        box = numpy.matrix((a,b,c)).T
        boxi = box.I
    elif columns[0] == '@BOX9':
        line = sys.stdin.readline()
        a = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        b = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        c = numpy.array([float(x) for x in line.split()])
        box = numpy.matrix((a,b,c)).T
        boxi = box.I
    elif columns[0] in ("@AR3A", "@NX3A", "@NX4A", "@WTG3", "@WTG6"):
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        coord = []
        for i in range(nmol):
            line = sys.stdin.readline()
            coord.append(numpy.array([float(x) for x in line.split()]))
    elif columns[0] in ("@AR3R",):
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        coord = []
        for i in range(nmol):
            line = sys.stdin.readline()
            c = numpy.array([float(x) for x in line.split()])
            c = numpy.dot(box,c)
            coord.append(numpy.array((c[0,0],c[0,1],c[0,2])))
    if len(coord) > 0 and len(box) > 0:
        print "@NGPH"
        print nmol
        for i in range(nmol):
            for j in range(i+1,nmol):
                d = numpy.matrix(coord[i] - coord[j]).T
                rd = numpy.dot(boxi,d)
                for k in range(3):
                    rd[k,0] -= math.floor(rd[k,0] + 0.5) #rint()
                d = numpy.dot(box,rd)
                l = numpy.linalg.norm(d)
                #print rd,d,l
                if l < thres:
                    print i,j
        print -1,-1
        coord = []

            
            
