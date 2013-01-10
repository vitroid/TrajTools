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
    def saveNGPH(self):
        s = "@NGPH\n"
        s += "%d\n" % self.number_of_nodes()
        for i,j in self.edges_iter():
            s += "%d %d\n" % (i,j)
        s += "-1 -1\n"
        return s
            


import numpy
       
if len(sys.argv)>1:
    random.seed(int(sys.argv[1]))
tagBOX3=compile("^@BOX3")
tagAR3A=compile("^@(AR3A|NX4A)")
tagNGPH=compile("^@NGPH")
box=[]
coord = []
graph = MyDiGraph()
while True:
    line = sys.stdin.readline()
    if line == "":
        break
    result = tagBOX3.search( line )
    if result:
        line = sys.stdin.readline()
        box = map(float, spacesplit(line))
    result = tagAR3A.search( line )
    if result:
        line = sys.stdin.readline()
        nmol = int(line)
        for i in range(nmol):
            line = sys.stdin.readline()
            c = map(float, spacesplit(line))
            coord.append(c[0:3])
    result = tagNGPH.search( line )
    if result:
        graph.loadNGPH(sys.stdin)
    if graph.number_of_nodes() > 0 and len(coord) > 0:
        dipole = numpy.zeros(3)
        for i,j,k in graph.edges_iter(data=True):
            vec = numpy.zeros(3)
            for dim in range(0,3):
                vec[dim] = coord[j][dim] - coord[i][dim]
                vec[dim] -= math.floor(vec[dim]/box[dim] + 0.5) * box[dim]
            dipole += vec
            #add the direction vector as an attribute of the edge
            k["vector"] = vec
        #test
        #for i,j,k in graph.edges_iter(data=True):
        #    print i,j,k
        s0 = numpy.linalg.norm(dipole)
        #In the following calculations, there must be error allowances.
        while s0 > 1.0:
            path,pathdipole = graph.homodromiccycle()
            s1 = numpy.linalg.norm(dipole - 2.0 * pathdipole)
            if s1 - s0 < 15.0:
                print s0,s1,dipole,pathdipole
                #accept the inversion
                for i in range(len(path)-1):
                    f = path[i]
                    t = path[i+1]
                    v = graph.get_edge_data(f,t)["vector"]
                    graph.remove_edge(f,t)
                    graph.add_edge(t,f,vector=-v)
                s0 = s1
                dipole -= 2.0 * pathdipole
        print graph.saveNGPH()
        graph.clear()
        coord = []
