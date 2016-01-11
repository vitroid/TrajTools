#!/usr/bin/env python
# coding: utf-8

import sys
import math
import numpy

rep = [int(x) for x in sys.argv[1:4]]

while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns) == 0:
        continue
    #monoclinic box
    if columns[0] == "@BOX4":
        print columns[0]
        line = sys.stdin.readline()
        a,b,c0,theta = [float(x) for x in line.split()]
        th = theta*math.pi / 180.
        print a*rep[0],b*rep[1],c0*rep[2],theta
        a = numpy.array((a,0,0))
        b = numpy.array((0,b,0))
        c = numpy.array((c0*math.cos(th),0,c0*math.sin(th)))
    elif columns[0] == "@BOX3":
        print columns[0]
        line = sys.stdin.readline()
        a,b,c = [float(x) for x in line.split()]
        print a*rep[0],b*rep[1],c*rep[2]
        a = numpy.array((a,0,0))
        b = numpy.array((0,b,0))
        c = numpy.array((0,0,c))
    elif columns[0] == "@BOX9":
        print columns[0]
        line = sys.stdin.readline()
        a = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        b = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        c = numpy.array([float(x) for x in line.split()])
        print a[0]*rep[0],a[1]*rep[0],a[2]*rep[0]
        print b[0]*rep[1],b[1]*rep[1],b[2]*rep[1]
        print c[0]*rep[2],c[1]*rep[2],c[2]*rep[2]
    #relative coord
    elif columns[0] == "@AR3R":
        print columns[0]
        line = sys.stdin.readline()
        nmol = int(line)
        print nmol*rep[0]*rep[1]*rep[2]
        for i in range(nmol):
            line = sys.stdin.readline()
            pos = [float(x) for x in line.split()[0:3]]
            for x in range(rep[0]):
                for y in range(rep[1]):
                    for z in range(rep[2]):
                        print (pos[0]+x)/rep[0],(pos[1]+y)/rep[1],(pos[2]+z)/rep[2]
    elif columns[0] in ("@NX4A", "@AR3A"):
        print columns[0]
        line = sys.stdin.readline()
        nmol = int(line)
        print nmol*rep[0]*rep[1]*rep[2]
        for i in range(nmol):
            line = sys.stdin.readline()
            pos = [float(x) for x in line.split()]
            xyz = numpy.array(pos[0:3])
            for x in range(rep[0]):
                for y in range(rep[1]):
                    for z in range(rep[2]):
                        p = xyz + x*a + y*b + z*c
                        print p[0],p[1],p[2],
                        for j in pos[3:]:
                            print j,
                        print

            

                
