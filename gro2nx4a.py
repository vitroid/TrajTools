#!/usr/bin/env python
# coding: utf-8

import math
import sys
import numpy
import rotation



############################################################### Periodic boundary utility
#relative position vector at the periodic boundary condition
def Wrap( vector, box ):
  for dim in range(len(vector)):
    vector[dim] -= math.floor( vector[dim] / box[dim] + 0.5 ) * box[dim]
  return vector




def Configure_gro(file):
    line = file.readline()
    line = file.readline()
    nsite = int(line)
    waters = []
    water = []
    for i in range(nsite):
        line = file.readline()
        molnum = line[0:5]
        molname = line[5:10]
        elemname = line[10:15]
        sitenum = line[15:20]
        x = float(line[20:28])*10
        y = float(line[28:36])*10
        z = float(line[36:44])*10
        xyz = numpy.array([x,y,z])
        if elemname == "   OW":
            water.append(xyz)
        elif elemname == "  HW1":
            water.append(xyz)
        elif elemname == "  HW2":
            water.append(xyz)
            waters.append(water)
            water = []
    line = file.readline()
    box = line.split()
    box[0] = float(box[0])*10
    box[1] = float(box[1])*10
    box[2] = float(box[2])*10
    box = numpy.array(box)
    #convert hydrogen positions from absolute to relative
    for water in waters:
        com = water[0]
        h1  = water[1]
        h2  = water[2]
        water[1] = Wrap(h1-com,box)
        water[2] = Wrap(h2-com,box)
        water[0] = com + (water[1]+water[2])/18
    return waters, box
            

def saveBOX3(box):
  print "@BOX3"
  print box[0],box[1],box[2]
  

def saveNX4A(waters):
  print "@NX4A"
  print len(waters)
  for water in waters:
    com = water[0]
    q = water[1]
    print com[0],com[1],com[2],q[0],q[1],q[2],q[3]


def atomic2rigid(water):
  com = water[0]
  h1  = water[1]
  h2  = water[2]
  y   = h2-h1
  z   = h1+h2
  y /= numpy.linalg.norm(y)
  z /= numpy.linalg.norm(z)
  x   = numpy.cross(y,z)
  mat = [x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]]
  #mat = [x[0],x[1],x[2],y[0],y[1],y[2],z[0],z[1],z[2]]
  q = rotation.rotmat2quat(mat)
  return (com,q)

def main(debug=False):
  #stage 1: load the structure
  waters,box = Configure_gro(sys.stdin)
  rigid = []
  for water in waters:
    rigid.append(atomic2rigid(water))
  saveBOX3(box)
  saveNX4A(rigid)

main()
