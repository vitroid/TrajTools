#!/usr/bin/env python
#coding: utf-8
#input: coordinate of the nodes, the digraph obeying the ice rule.
#output: the digraph with zero net dipole.

import sys
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
            (x,y) = [int(v) for v in line.split()]
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


#v is an numpy.array
def box9wrap(v,box9):
    r = numpy.dot(box9.I, numpy.matrix(v).T)
    for k in range(3):
        r[k,0] -= math.floor(r[k,0]+0.5)
    a = numpy.dot(box9, r)
    return numpy.array((a[0,0],a[1,0],a[2,0]))


import numpy

if len(sys.argv)>1:
    random.seed(int(sys.argv[1]))
box=[]
coord = []
graph = MyDiGraph()
while True:
    line = sys.stdin.readline()
    if line == "":
        break
    columns = line.split()
    if len(columns) < 1:
        continue
    if columns[0] == "@BOX3":
        line = sys.stdin.readline()
        a,b,c = [float(x) for x in line.split()]
        a = numpy.array((a,0,0))
        b = numpy.array((0,b,0))
        c = numpy.array((0,0,c))
        box9 = numpy.matrix((a,b,c)).T
    elif columns[0] == "@BOX9":
        line = sys.stdin.readline()
        a = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        b = numpy.array([float(x) for x in line.split()])
        line = sys.stdin.readline()
        c = numpy.array([float(x) for x in line.split()])
        box9 = numpy.matrix((a,b,c)).T
    elif columns[0] == "@AR3A":
        line = sys.stdin.readline()
        nmol = int(line)
        for i in range(nmol):
            line = sys.stdin.readline()
            c = [float(x) for x in line.split()]
            coord.append(numpy.array(c[0:3]))
    elif columns[0] == "@AR3R":
        line = sys.stdin.readline()
        nmol = int(line)
        for i in range(nmol):
            line = sys.stdin.readline()
            c = [float(x) for x in line.split()]
            c = numpy.matrix(c).T
            c = numpy.dot(box9,c)
            coord.append(numpy.array((c[0,0],c[1,0],c[2,0])))
    elif columns[0] == "@NGPH":
        graph.loadNGPH(sys.stdin)
    if graph.number_of_nodes() > 0 and len(coord) > 0:
        dipole = numpy.zeros(3)
        for i,j,k in graph.edges_iter(data=True):
            #print coord[j],coord[i]
            vec = coord[j] - coord[i]
            vec = box9wrap(vec,box9)
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
