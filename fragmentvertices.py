#!/usr/bin/env python
# coding: utf-8

import sys

vertices = set()
rngs = []
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns)>0:
        if columns[0] == "@RNGS":
            line = sys.stdin.readline()
            nmol = int(line)
            while True:
                line = sys.stdin.readline()
                columns = map(int,line.split())
                if columns[0] == 0:
                    break
                del columns[0]
                rngs.append(set(columns))
        elif columns[0] == "@RSET":
            line = sys.stdin.readline()
            while True:
                line = sys.stdin.readline()
                columns = map(int,line.split())
                if columns[0] == 0:
                    break
                del columns[0]
                for i in columns:
                    vertices = vertices.union(rngs[i])
print "@VMRK"
print nmol
for i in range(nmol):
    if i in vertices:
        print 1
    else:
        print 0

                
                
                
            
            
