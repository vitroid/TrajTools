#!/usr/bin/env python


import sys

# 1cm-1 = 33ps
LEN = 330
vel = []
vacf = [0.0 for i in range(6)] * LEN
count = [0.0] * LEN
while True:
    #read a line, anyway
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    #look up tags
    tag = columns[0]
    if tag in  ('@WTG6', '@WTG3'):
        #get the first line == number of molecules
        line = sys.stdin.readline()
        columns = line.split()
        nmol = int(columns[0])
        #prepare room for new data
        vel.append([[] for j in range(nmol)])
        if len(vel) > LEN:
            vel.pop(0)
        #read molecular info
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            #last data, i-th molecule, 6 velocities
            if tag == '@WTG6':
                vel[-1][i] = map(float,columns[12:18])
            elif tag == '@WTG3':
                vel[-1][i] = map(float,columns[7:13])
            for j in range(len(vel)):
                for k in range(6):
                    vacf[len(vel)-j][k] += vel[-1][i][k] * vel[j][i][k]
                count[len(vel)-j] += 1

