#!/usr/bin/env python
# coding: utf-8
#
#速度情報をずらし、速度を乱雑化させた新配置を生成する。
#

import sys
from re import *
import math
import string

spaces=compile(" +")

def spacesplit(line):
    line = string.rstrip(line," \t\r\n")
    columns=spaces.split(line)
    while columns[0] == "":
        columns.pop(0)
    return columns

import sys
shift = int(sys.argv[1])

tagWTG6=compile("^@WTG6")
tagATG5=compile("^@ATG5")
while True:
    line = sys.stdin.readline()
    if line == "":
        break
    result = tagATG5.search( line ) or tagWTG6.search( line ) 
    if result:
        print line,
        coordColumns = 12
        if tagATG5.search(line):
            coordColumns = 3
        line = sys.stdin.readline()
        print line,
        nmol = int(line)
        coord = []
        aug   = []
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = map(float, spacesplit(line))
            coord.append(columns[0:coordColumns])
            aug.append(columns[coordColumns:len(columns)])
        for i in range(nmol):
            for j in range(len(coord[i])):
                print coord[i][j],
            for j in range(len(aug[(i+shift)%nmol])):
                print aug[(i+shift)%nmol][j],
            print
    else:
        print line,
