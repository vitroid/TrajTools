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
	print "l",com[i][0],com[i][1],com[i][2],com[i][0]+d[0],com[i][1]+d[1],com[i][2]+d[2]
    print




def output_bondangles(com,edges,box):
    nei = [set() for i in range(len(com))]
    dir = dict()
    for edge in edges:
        i,j = edge
        dir[(i,j)] = +1
        dir[(j,i)] = -1
        nei[i].add(j)
        nei[j].add(i)
    print "@VALU"
    print len(nei),6
    for i in range(len(nei)):
        for j,k in itertools.combinations(nei[i],2):
            v1 = com[j] - com[i]
            v1 = wrap(v1,box)
            v1 /= numpy.linalg.norm(v1)
            v2 = com[k] - com[i]
            v2 = wrap(v2,box)
            v2 /= numpy.linalg.norm(v2)
            print i,j,k,"%6.1f" % (math.acos(numpy.dot(v1,v2))*180./math.pi),dir[(i,j)],dir[(i,k)]
    print -1,-1,-1,0,0,0

mode = "-y"
if len(sys.argv)> 1 and sys.argv[1] == "-b":
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
    elif tag in  ('@AR3A', '@WTG6', '@WTG3', '@NX4A', '@NX3A'):
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
