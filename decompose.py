#!/usr/bin/env python
# coding: utf-8

import sys
vmrk = []
component = []
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
                while columns[0] >= len(component):
                    component.append([])
        elif columns[0] in ("@NX4A","@AR3A"):
            tag = columns[0]
            line = sys.stdin.readline()
            for i in range(nmol):
                line = sys.stdin.readline()
                xyz = map(float, line.split())
                component[vmrk[i]].append(xyz)
        else:
            print line,
print "@NCMP"
print len(component)
for i in range(len(component)):
    compo = component[i]
    print tag
    print len(compo)
    for xyz in compo:
        for i in xyz:
            print i,
        print

                
                
            
            
