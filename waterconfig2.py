#!/usr/bin/env python

from math import *
import sys
from random import *
from rotation import *


#calculate quaternions from two O-to-H vectors
def rotmx2(p,q):
    p = normalize(p)
    q = normalize(q)
    k = normalize((p[0]+q[0],p[1]+q[1],p[2]+q[2]))
    j = normalize((q[0]-p[0],q[1]-p[1],q[2]-p[2]))
    i = normalize((j[1]*k[2]-j[2]*k[1],j[2]*k[0]-j[0]*k[2],j[0]*k[1]-j[1]*k[0]))
    return rotmat2quat( (i[0], j[0], k[0], i[1], j[1], k[1], i[2], j[2], k[2]) )


def orientation(i,xyz,hb,box):
    a = [0.0] * 3
    b = [0.0] * 3
    for k in range(3):
        a[k] = xyz[hb[i][0]][k] - xyz[i][k]
        a[k] -= floor(a[k]/box[k]+0.5)*box[k]
        
        b[k] = xyz[hb[i][1]][k] - xyz[i][k]
        b[k] -= floor(b[k]/box[k]+0.5)*box[k]
    return rotmx2(a,b)


    
tag = '@NX4A'
hb = None
xyz = None
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns) == 0:
        continue
    if columns[0] in ('@BOX3'):
        line = sys.stdin.readline()
        columns = line.split()
        box = map(float,columns)
        print "@BOX3"
        print box[0],box[1],box[2]
    if columns[0] in ('@NX4A', '@NX3A', '@AR3A'):
        line = sys.stdin.readline()
        columns = line.split()
	n=int(columns[0])
        xyz = []
	for i in range(n):
            line = sys.stdin.readline()
            columns = line.split()
            x,y,z = map(float,columns[0:3])
	    x+=(random()-0.5)*0.00001
	    y+=(random()-0.5)*0.00001
	    z+=(random()-0.5)*0.00001
	    xyz.append((x,y,z))
    elif columns[0] in ('@NGPH'):
        line = sys.stdin.readline()
        columns = line.split()
	n=int(columns[0])
        hb = [ [] for i in range(n) ]
	while True:
            line = sys.stdin.readline()
            columns = line.split()
            frm,to = map(int, columns[0:2])
            if frm < 0:
                break
            hb[frm].append(to)
    if hb and xyz:
        if tag[0] == '@':
            print tag
            print n
        for i in range(n):
            q = orientation(i,xyz,hb,box)
            if tag == '@NX4A':
                print xyz[i][0],xyz[i][1],xyz[i][2],q[0],q[1],q[2],q[3]
        hb = None
        xyz = None
