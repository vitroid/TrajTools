#!/usr/bin/env python
# coding: utf-8

#anneal the network structure.


import sys
import math



def force(mols,ngph,box):
    forces = []
    boxforce = [0.0] * 3
    for i in range(len(mols)):
        forces.append([0.0]*3)
    for i,j in ngph:
        d = [0.0] * 3
        s = 0.0
        for dim in range(3):
            d[dim] = mols[j][dim] - mols[i][dim]
            d[dim] -= math.floor(d[dim] / box[dim] + 0.5)*box[dim]
            s += d[dim] **2
        s = math.sqrt(s)
        for dim in range(3):
            forces[i][dim] +=  (s - 1.0) * d[dim] / s
            forces[j][dim] -=  (s - 1.0) * d[dim] / s
            boxforce[dim]  -=  (s - 1.0) * abs(d[dim]) / s
        #if i == 0 and j == 1:
        #    print i,j,s,d
    return forces,boxforce


k = 0.01
boxk = 0.0001

def iterate(mols,ngph,box=None):
    #calcforce
    for loop in range(1000):
        forces,boxforce = force(mols,ngph,box)
        for i in range(len(mols)):
            for dim in range(3):
                mols[i][dim] += forces[i][dim] * k
        newbox = [0.0] * 3
        for dim in range(3):
            newbox[dim] = box[dim] + boxforce[dim] * boxk
        for i in range(len(mols)):
            for dim in range(3):
                mols[i][dim] *= newbox[dim] / box[dim]
        box = newbox
    return box,mols





def usage():
    print "usage: %s " % sys.argv[0]
    sys.exit(1)


#if len(sys.argv) == 1:
#    cutoff = 6
#else:
#    cutoff = float(sys.argv[1])

ngph = []
mols = []
while True:
    #read a line, anyway
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    #look up tags
    tag = columns[0]
    if tag in  ('@NGPH', ):
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        while True:
            line = sys.stdin.readline()
            columns = line.split()
            columns = tuple(map(int, columns[0:2]))
            if columns[0] < 0:
                break
            ngph.append(columns)
    if tag in  ('@BOX3', ):
        line = sys.stdin.readline()
        columns = line.split()
        box = map(float, columns[0:3])
    elif tag in  ('@AR3A', '@WTG6', '@WTG3', '@NX4A', '@NX3A'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            xyz = map(float,columns[0:3])
            for dim in range(3):
                xyz[dim] -= math.floor(xyz[dim] / box[dim])*box[dim]
            mols.append(xyz)
    if len(mols) and len(ngph):
        box,mols = iterate(mols,ngph,box)
        print "@BOX3"
        print box[0],box[1],box[2]
        print "@AR3A"
        print len(mols)
        for x,y,z in mols:
            print x,y,z
        
