#!/usr/bin/env python
#Determine whether the network obeys Bernal's ice rule or not.

import sys

undir = False
if len(sys.argv)>1:
    if sys.argv[1] == "-u":
        undir = True

while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns)==0:
        continue
    if columns[0] =="@NGPH":
        line = sys.stdin.readline()
        nmol = int(line)
        nin =  [set() for i in range(nmol)]
        nout = [set() for i in range(nmol)]
        while True:
            line = sys.stdin.readline()
            i,j = map(int,line.split())
            if i < 0:
                break
            nin[j].add(i)
            nout[i].add(j)
        defect = 0
        for i in range(nmol):
            if undir:
                if len(nin[i]|nout[i]) != 4:
                    defect += 1
                    print i,nin[i],nout[i]
            else:
                if len(nin[i]) != 2 or len(nout[i]) != 2:
                    defect += 1
                    print i,nin[i],nout[i]
        if defect > 0:
            print "Defective network."
            sys.exit(1)

            
            
