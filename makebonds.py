#!/usr/bin/env python

#make bonds acoording to com-com distances

import sys
import math


thres = float(sys.argv[1])

while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if columns[0] == '@BOX3':
        line = sys.stdin.readline()
        box = map(float, line.split())
    if columns[0] in ("@AR3A", "@NX3A", "@NX4A", "@WTG3", "@WTG6"):
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        coord = []
        for i in range(nmol):
            line = sys.stdin.readline()
            coord.append(map(float,line.split()))
        print "@NGPH"
        print nmol
        for i in range(nmol):
            for j in range(i+1,nmol):
                d = 0.0
                for k in range(3):
                    d0 = coord[i][k] - coord[j][k]
                    d0 -= math.floor(d0/box[k]+0.5)*box[k]
                    d += d0**2
                if d < thres**2:
                    print i,j
        print -1,-1


            
            
