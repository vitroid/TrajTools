#!/usr/bin/env python
#coding: utf-8
#input: coordinate of the nodes, the digraph obeying the ice rule.
#output: the digraph with zero net dipole.

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
            (x,y) = map(int, spacesplit(line))
            if x < 0:
                break
            self.add_edge(x,y)
    def _goahead(self,node,marked,order):
        while not marked[node]:
            marked[node] = True
            order.append(node)
            #print order
            nei = self.neighbors(node)
            next = random.randint(0,1)
            if len(nei) != 2:
                print "ERROR",node,nei
            node = nei[next]
        #a cyclic path is found.
        #trim the uncyclic part
        while order[0] != node:
            order.pop(0)
        #add the node at the last again
        order.append(node)
        delta = numpy.zeros(3)
        for i in range(len(order)-1):
            delta += self.get_edge_data(order[i],order[i+1])["vector"]
        return order, delta

    def homodromiccycle(self):
        marked = [False] * self.number_of_nodes()
        order = []
        node = random.randint(0,self.number_of_nodes()-1)
        return self._goahead(node,marked,order)


    def purgedefects(self, defects):
        d = defects[0]
        if self.in_degree(d) == 2 and self.out_degree(d) == 2:
            defects.pop(0)
            return
        print d,len(defects)
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
            


if len(sys.argv)>1:
    random.seed(int(sys.argv[1]))
tagNGPH=compile("^@NGPH")
graph = MyDiGraph()
while True:
    line = sys.stdin.readline()
    if line == "":
        break
    result = tagNGPH.search( line )
    if result:
        graph.loadNGPH(sys.stdin)
        defects = graph.defects()
        while len(defects)>0:
            graph.purgedefects(defects)
        #verify
        defects = graph.defects()
        if len(defects) > 0:
            print "ERROR ", defects
        print graph.saveNGPH()
        graph.clear()
