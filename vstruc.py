#!/usr/bin/env python

#should be integrated to trajConverter.py

import rotation_numpy
import math
import numpy
import sys

def rint(x):
    return math.floor(x+0.5)


def wrap(v,box):
    r = numpy.zeros(3)
    for i in range(len(v)):
        r[i] = v[i] - rint(v[i]/box[i])*box[i]
    return r

def die(msg):
    sys.stderr.writeline(msg)
    sys.exit(1)

width = int(sys.argv[1])

vcom = None
vori = None
deltastack = []
stack = []
frame = 0
ncompo = 1
compo = 0
ids = dict()
tags = dict()
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns) > 0:
        if columns[0] == "@BOX3":
            line = sys.stdin.readline()
            box = map(float,line.split())
        elif columns[0] == "@ID08":
            line = sys.stdin.readline()
            id08 = line[0:8]
            ids[compo] = id08
        elif columns[0] == "@NCMP":
            line = sys.stdin.readline()
            ncompo = int(line)
            compo = 0
        elif columns[0] == "@NX4A":
            if id08 != ids[compo]:
                die("ID unmatches.")
            if tags.has_key(compo) and columns[0] != tags[compo]:
                die("Tag unmatches.")
            tags[compo] = columns[0]
            line = sys.stdin.readline()
            nmol = int(line)
            mols = []
            for i in range(nmol):
                line = sys.stdin.readline()
                columns = map(float,line.split())
                com = numpy.array(columns[0:3])
                ori = numpy.array(columns[3:7])
                mols.append((com,ori))
            if compo == 0:
                stack.append([])
            stack[-1].append(mols)
            if len(stack) > 1:
                delta = []
                for i in range(nmol):
                    com = stack[len(stack)-1][compo][i][0]
                    ori = stack[len(stack)-1][compo][i][1]
                    lastcom = stack[len(stack)-2][compo][i][0]
                    lastori = stack[len(stack)-2][compo][i][1]
                    dcom = wrap(com - lastcom, box)
                    #negative rotation
                    n = - lastori
                    n[0] = - n[0]
                    dori = rotation_numpy.qadd(ori, n)
                    #print dori
                    dcom /= width
                    dori = rotation_numpy.qmul(dori,1.0/width)
                    delta.append((dcom,dori))
                if compo == 0:
                    deltastack.append([])
                deltastack[-1].append(delta)
            compo += 1
        elif columns[0] == "@AR3A":
            if id08 != ids[compo]:
                die("ID unmatches.")
            if tags.has_key(compo) and columns[0] != tags[compo]:
                die("Tag unmatches.")
            tags[compo] = columns[0]
            line = sys.stdin.readline()
            nmol = int(line)
            mols = []
            for i in range(nmol):
                line = sys.stdin.readline()
                columns = map(float,line.split())
                com = numpy.array(columns[0:3])
                mols.append(com)
            if compo == 0:
                stack.append([])
            stack[-1].append(mols)
            if len(stack) > 1:
                delta = []
                for i in range(nmol):
                    com = stack[len(stack)-1][compo][i]
                    lastcom = stack[len(stack)-2][compo][i]
                    dcom = wrap(com - lastcom, box)
                    dcom /= width
                    delta.append(dcom)
                if compo == 0:
                    deltastack.append([])
                deltastack[-1].append(delta)
            compo += 1
            #deltastack: 4-d array of time, compo, molecule, and (com or ori)
            #stack:      4-d array of time, compo, molecule and (com or ori)
        if compo == ncompo:
            #print stack
            if len(stack) == width:
                #if frame >= 100:
                #    break
                frame += 1
                print "@NCMP"
                print ncompo
                print "@BOX3"
                print box[0],box[1],box[2]
                for compo in range(ncompo):
                    print "@ID08"
                    print ids[compo]
                    print tags[compo]
                    nmol = len(stack[0][compo])
                    print nmol
                    if tags[compo] == "@NX4A":
                        for i in range(nmol):
                            #print stack[0][i]
                            c = stack[0][compo][i][0]
                            o = stack[0][compo][i][1]
                            for j in range(len(deltastack)):
                                #print i,deltastack[j][i],o
                                weight = len(deltastack)-j
                                #print weight
                                c += deltastack[j][compo][i][0]*weight
                                q = rotation_numpy.qmul(deltastack[j][compo][i][1], weight)
                                o = rotation_numpy.qadd(o, q)
                            print c[0],c[1],c[2],o[0],o[1],o[2],o[3]
                    elif tags[compo] == "@AR3A":
                        for i in range(nmol):
                            #print stack[0][i]
                            c = stack[0][compo][i]
                            for j in range(len(deltastack)):
                                #print i,deltastack[j][i],o
                                weight = len(deltastack)-j
                                #print weight
                                c += deltastack[j][compo][i]*weight
                            print c[0],c[1],c[2]
                del stack[0]
                if len(deltastack) > 0:
                    del deltastack[0]
            compo = 0
