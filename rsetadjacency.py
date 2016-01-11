#!/usr/bin/env python
# coding: utf-8
#
import sys
import math
import string
import fileloaders as fl




def AdjacencyGraph(nring, rsets, minsize=3):
    ringowners = [[] for i in range(nring)]
    for i in range(len(rsets)):
        rset = rsets[i]
        size = len(rset)
        #print columns
        if size >= minsize:
            for ring in rset:
                ringowners[ring].append(i)
    edges = set()
    for owners in ringowners:
        if len(owners)==2:
            edges.add(frozenset(owners))
    return edges



if __name__ == "__main__":
    minsize = 3
    cmd = sys.argv.pop(0)

    kinds = set()
    while 0 < len(sys.argv):
        item = sys.argv.pop(0)
        if item == "-v":
            #usage: -v vmrkfile members
            item = sys.argv.pop(0)
            file = open(item)
            while True:
                line = file.readline()
                if len(line) == 0:
                    break
                columns = line.split()
                if columns[0] == "@VMRK":
                    idlist = fl.LoadVMRK(file)
            item = sys.argv.pop(0)
            kinds = set([int(x) for x in item.split(",")])
            members = set()
            for i in range(len(idlist)):
                if idlist[i] in kinds:
                    members.add(i)
        else:
            minsize = int(item)
    print "KINDS:",kinds



    file = sys.stdin
    while True:
        line = file.readline()
        if line == "":
            break
        #process @RSET
        columns = [x for x in line.split()]
        if 0 < len(columns) and columns[0] == "@RSET":
            nring, rsets = fl.LoadRNGS(file)
            adjacencygraph = AdjacencyGraph(nring, rsets, minsize)
            print "@NGPH"
            print len(rsets)
            for edge in adjacencygraph:
                if 0 < len(kinds) and not edge.intersection(members) == edge:
                    continue
                for vertex in edge:
                    print vertex,
                print
            print -1,-1
