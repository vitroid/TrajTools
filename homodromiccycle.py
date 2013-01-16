#!/usr/bin/env python
#coding: utf-8

#rngsを読み込む
#ngphを読み込む
#それぞれのringがもしhomodromicなら、それを反転し、グラフを出力する。
#それにあわせて水分子を配置するのはwaterconfigにまかせる。


#input: coordinate of the nodes, the digraph obeying the ice rule.
#output: the digraph with zero net dipole.

import sys
from re import *
import math
import string

import networkx
import random



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

    def isHomodromic(self,ring):
        t = True
        for i in range(len(ring)):
            node = ring[i-1]
            if not ( ring[i] in self.neighbors(node) ):
                t = False
                break
        if t:
            return 1
        t = True
        for i in range(len(ring)-1, -1, -1):
            node = ring[i]
            if not ( ring[i-1] in self.neighbors(node) ):
                t = False
                break
        if t:
            return -1
        return 0


    def Invert(self,ring,rot):
        for i in range(len(ring)):
            x = ring[i-1]
            y = ring[i]
            if rot == +1:
                self.remove_edge(x,y)
                self.add_edge(y,x)
            else:
                self.remove_edge(y,x)
                self.add_edge(x,y)
            

    def homodromiccycle(self):
        marked = [False] * self.number_of_nodes()
        order = []
        node = random.randint(0,self.number_of_nodes()-1)
        return self._goahead(node,marked,order)


    #1. member nodes must have larger label than the initial node
    #2. cycle must close at the initial node. Other cycles should be ignored.
    def _scan(self,node,marked,order):
        if len(order) > 0:
            if order[0] == node:
                #rule 2
                #successfully closed cycle
                print order
                return
            elif order[0] > node:
                #rule 1
                return
        if marked[node]:
            #failed cycle
            return
        if len(order) > 10:
            return
        marked[node] = True
        order.append(node)
        nei = self.neighbors(node)
        if len(nei) != 2:
            print "ERROR",node,nei
            sys.exit(1)
        for next in nei:
            self._scan(next,marked,order)
        order.pop()
        marked[node] = False


    def allhomodromiccycles(self):
        marked = [False] * self.number_of_nodes()
        order = []
        for node in range(self.number_of_nodes()):
            self._scan(node,marked,order)


    def purgedefects(self, defects):
        d = defects[0]
        if self.in_degree(d) == 2 and self.out_degree(d) == 2:
            defects.pop(0)
            return
        #print d,len(defects)
        if self.in_degree(d) > 2:
            nodes = self.predecessors(d)
            i = random.randint(0,len(nodes)-1)
            node = nodes[i]
            self.remove_edge(node,d)
            self.add_edge(d,node)
            defects.append(node)
        if self.out_degree(d) > 2:
            nodes = self.successors(d)
            i = random.randint(0,len(nodes)-1)
            node = nodes[i]
            self.remove_edge(d,node)
            self.add_edge(node,d)
            defects.append(node)

    def defects(self):
        defects = []
        for i in range(self.number_of_nodes()):
            if self.in_degree(i) != 2 or self.out_degree(i) != 2:
                defects.append(i)
            if self.degree(i) != 4:
                print "ERROR",i,self.degree(i),self.successors(i),self.predecessors(i)
        return defects
        

    def saveNGPH(self):
        s = "@NGPH\n"
        s += "%d\n" % self.number_of_nodes()
        for i,j in self.edges_iter():
            s += "%d %d\n" % (i,j)
        s += "-1 -1\n"
        return s
            

rings = []  #by default, null list means all
ngphFile = open(sys.argv[1], "r")
if len(sys.argv) > 2:
    rings = sys.argv[2:]
rings = set(map(int,rings))
tagNGPH=compile("^@NGPH")
graph = MyDiGraph()
while True:
    line = ngphFile.readline()
    if line == "":
        break
    result = tagNGPH.search( line )
    if result:
        graph.loadNGPH(ngphFile)
right = 0
left = 0
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    count = 0
    ringid = 0
    inv = []
    if columns[0] == "@RNGS":
        nmol = sys.stdin.readline()
        while True:
            line = sys.stdin.readline()
            columns = line.split()
            columns = map(float,columns)
            if columns[0] == 0:
                break
            del columns[0]
            rot = graph.isHomodromic(columns)
            if rot:
                if len(rings) == 0:
                    g = MyDiGraph(graph)
                    g.Invert(columns,rot)
                    print g.saveNGPH()
                elif count in rings:
                    if rot == -1:
                        columns.reverse()
                    inv.append(columns)
                count += 1
if len(rings):
    for ring in inv:
        graph.Invert(ring,+1)
    print graph.saveNGPH()
