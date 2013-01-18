#!/usr/bin/env python
# coding: utf-8

import sys

compo = int(sys.argv[1])
ncompo = 1
count = 0
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns)>0:
        if columns[0] == "@NCMP":
            line = sys.stdin.readline()
            ncompo = int(line)
        elif columns[0] in ("@NX4A","@AR3A"):
            if count == compo:
                print line,
            line = sys.stdin.readline()
            if count == compo:
                print line,
            nmol = int(line)
            for i in range(nmol):
                line = sys.stdin.readline()
                if count == compo:
                    print line,
            count = (count+1) % ncompo
        else:
            print line,
