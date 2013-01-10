#!/usr/bin/env python

import sys

#1st line
line = sys.stdin.readline()
columns = line.split()
nmol = int(columns[0])
#2nd line
line = sys.stdin.readline()
box = map(float,line.split())
#3rd line
line = sys.stdin.readline()

#print headers
print "@BOX3"
print box[0],box[1],box[2]
print "@NX3A"
print nmol
#following lines

for i in range(nmol):
    line = sys.stdin.readline()
    xyz = map(float,line.split())
    line = sys.stdin.readline()
    euler = map(float,line.split())
    print xyz[0],xyz[1],xyz[2],euler[0],euler[1],euler[2]

    
    
