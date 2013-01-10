#!/usr/bin/env python
# coding: utf-8
#sample implementation; only com-com RDF

import sys
import rdf
import math
def usage():
    print "usage: %s cutoff" % sys.argv[0]
    sys.exit(1)


cutoff = float(sys.argv[1])

while True:
    #read a line, anyway
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    #look up tags
    tag = columns[0]
    if tag in ('@BOX3',):
        line = sys.stdin.readline()
        columns = line.split()
        box = map(float,columns[0:3])
    elif tag in  ('@WTG6', '@WTG3', '@NX4A', '@NX3A'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        mols = []
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            xyz = map(float,columns[0:3])
            for dim in range(3):
                xyz[dim] -= math.floor(xyz[dim] / box[dim]) * box[dim]
            mols.append(xyz)
        dist = rdf.calc(mols, box, binw=0.5, cutoff=cutoff)
        print dist
