#!/usr/bin/env python
# coding: utf-8
# estimate simulation cell size from boxless unit cell.

import sys
import rdf
import math


def estimatebox(mols,maxs,dim):
    delta = 0.125
    box = list(maxs)
    box[dim] /= 2
    dist0 = rdf.calc(mols, maxs, binw=delta*2, cutoff=cutoff)
    #print dist0
    zeros = 0
    while dist0[zeros] == 0.0:
        zeros += 1
    maxs[dim] = box[dim] + zeros*delta*2
    #tune x
    while delta > 0.00001:
        dist0 = rdf.calc(mols, maxs, binw=delta*2, cutoff=cutoff)
        #print dist0
        best = 0
        bestsize = 0.0
        while box[dim] < maxs[dim]:
            dist = rdf.calc(mols, box, binw=delta*2, cutoff=cutoff)
            count = 0
            n = min(len(dist),len(dist0))
            for i in range(n):
                if (dist[i] ==0 and dist0[i] == 0):
                    count += 1
            if best < count:
                best = count
                bestsize = box[dim]
            #print best,bestsize,dist
            box[dim] += delta
        delta /= 2
        box[dim] = bestsize - delta*2
        maxs[dim] = bestsize + delta*4
    maxs[dim] = bestsize
    return bestsize

def usage():
    print "usage: %s cutoff" % sys.argv[0]
    sys.exit(1)


if len(sys.argv) == 1:
    cutoff = 6
else:
    cutoff = float(sys.argv[1])

while True:
    #read a line, anyway
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    #look up tags
    tag = columns[0]
    if tag in  ('@WTG6', '@WTG3', '@NX4A', '@NX3A'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        mols = []
        mins = [1e23] * 3
        maxs = [-1e23] * 3
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            xyz = map(float,columns[0:3])
            for dim in range(3):
                if xyz[dim] < mins[dim]:
                    mins[dim] = xyz[dim]
                if xyz[dim] > maxs[dim]:
                    maxs[dim] = xyz[dim]
            mols.append(xyz)
        for dim in range(3):
            maxs[dim] -= mins[dim]
            maxs[dim] *= 2
        for i in range(nmol):
            for dim in range(3):
                mols[i][dim] -= mins[dim]
        for dim in range(3):
            bestsize = estimatebox(mols,maxs,dim=dim)
        print "@BOX3"
        print maxs[0],maxs[1],maxs[2]
