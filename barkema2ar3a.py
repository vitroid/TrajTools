#!/usr/bin/env python

import sys
ngph = 0
ar3a = 0
if sys.argv[1] == "-n":
    ngph = 1
if sys.argv[1] == "-a":
    ar3a = 1

line=sys.stdin.readline()
nmol=int(line[2:])
line=sys.stdin.readline()
box=float(line[4:])
if ar3a:
    print "@BOX3"
    print box*2,box*2,box*2
    print "@AR3A"
    print nmol
for i in range(nmol):
    line=sys.stdin.readline()
    i,x,y,z = map(float,line.split())
    if ar3a:
        print x+box,y+box,z+box
if ngph:
    print "@NGPH"
    print nmol
for i in range(nmol):
    line=sys.stdin.readline()
    i,a,b,c,d = map(int, line.split())
    if ngph:
        print i,a
        print i,b
        print i,c
        print i,d
if ngph:
    print -1,-1
