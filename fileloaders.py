#!/usr/bin/env python

import numpy as np

def LoadVMRK(file):
    n = int(file.readline())
    v = []
    for i in range(n):
        x = int(file.readline())
        v.append(x)
    return v



def LoadBOX3(file):
    line = file.readline()
    return np.array([float(x) for x in line.split()])



def LoadAR3A(file):
    xyz = []
    line = file.readline()
    nmol = int(line)
    for i in range(nmol):
        line = file.readline()
        columns = np.array([float(x) for x in line.split()[0:3]])
        xyz.append(columns)
    return xyz



#format is same as @RSET
def LoadRNGS(file,debug=0):
    line = file.readline()
    n = int(line)
    rings = []
    while True:
        line=file.readline()
        if len(line) == 0:
            break
        if debug: print "#",line,
        columns = [int(x) for x in line.split()]
        if debug: print "#",line,columns,n
        if columns[0] == 0:
            break
        nodes = columns[1:]
        rings.append(nodes)
    return n,rings
