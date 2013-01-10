#!/usr/bin/env python
#coding: utf-8
#input: coordinate of the nodes, the digraph obeying the ice rule.
#output: the digraph with zero net dipole.

import sys
import math
import string

import networkx

class MyDiGraph(networkx.DiGraph):
    def loadNGPH(self,filehandle):
        self.clear()
        line = filehandle.readline()
        nmol = int(line)
        for i in range(nmol):
            self.add_node(i)
        while True:
            line = filehandle.readline()
            (x,y) = map(int, line.split())
            if x < 0:
                break
            self.add_edge(x,y)



files = sys.argv[1:]
g = dict()
for filename in files:
    f = open(filename)
    while True:
        line = f.readline()
        if line == "":
            break
        columns = line.split()
        if columns[0] == "@NGPH":
            g[filename] = MyDiGraph()
            g[filename].loadNGPH(f)

unique = []
count = dict()
for f in files:
    isUnique = True
    for u in unique:
        if networkx.is_isomorphic(g[f],g[u]):
            isUnique = False
            print f,"==",u
            count[u] += 1
            break
    if isUnique:
        unique.append(f)
        count[f] = 1
        
for filename in unique:
    print filename, count[filename]


