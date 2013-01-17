#!/usr/bin/env python
# coding: utf-8

import sys

vmrk = []
ngph = set()
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns)>0:
        if columns[0] == "@VMRK":
            line = sys.stdin.readline()
            nmol = int(line)
            for i in range(nmol):
                line = sys.stdin.readline()
                columns = map(int,line.split())
                vmrk.append(columns[0])
        elif columns[0] == "@NGPH":
            line = sys.stdin.readline()
            while True:
                line = sys.stdin.readline()
                columns = map(int,line.split())
                if columns[0] < 0:
                    break
                ngph.add((columns[0],columns[1]))
print "@BMRK"
print nmol
for i,j in ngph:
    print i,j,vmrk[i]+vmrk[j]
print -1,-1,0

                
                
            
            
