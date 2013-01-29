#!/usr/bin/env python
# conding: utf-8

import sys
#compare two NGPHs and show difference in @DGPH format

def loadNGPH(filehandle):
    while True:
        line = filehandle.readline()
        if len(line) == 0:
            break
        columns = line.split()
        if len(columns) == 0:
            continue
        if columns[0] == "@NGPH":
            line = filehandle.readline()
            nmol = int(line)
            edges = set()
            while True:
                line = filehandle.readline()
                (x,y) = map(int, line.split())
                if x < 0:
                    break
                edges.add((x,y))
    return nmol,edges

n1,e1 = loadNGPH(open(sys.argv[1],"r"))
n2,e2 = loadNGPH(open(sys.argv[2],"r"))
if  n1 != n2:
    print "different size",n1,n2
    sys.exit(1)
print "@DGPH"
print n1
for edge in e1&e2:
    x,y = edge
    print x,y,"="
for edge in e1 - e2:
    x,y = edge
    if (y,x) in e2:
        print x,y,"x"
    else:
        print x,y,"<"
for edge in e2 - e1:
    x,y = edge
    if not (y,x) in e1:
        print x,y,">"
print -1,-1,0
