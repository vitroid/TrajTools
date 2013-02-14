#!/usr/bin/env python

#exchange axes from xyz to yzx.
#trivial with quaternion.

import sys
import rotation
import math
#xyz->yzx
#revolve 120 degree around (1,1,1) axis
thh = math.pi / 3
e   = 1. / math.sqrt(3)
co  = math.cos(thh)
si  = math.sin(thh)
rot = (co, -e*si, e*si, -e*si)
 

while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns)==0:
        continue
    if columns[0] =="@BOX3":
        print columns[0]
        line = sys.stdin.readline()
        columns = line.split()
        bx,by,bz = map(float,columns[0:3])
        print by,bz,bx
    elif columns[0] =="@NX4A":
        print columns[0]
        line = sys.stdin.readline()
        nmol = int(line)
        print nmol
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            x,y,z,a,b,c,d = map(float,columns[0:7])
            a,b,c,d = rotation.qadd((a,b,c,d),rot)
            print y,z,x,a,b,c,d
    elif columns[0] =="@AR3A":
        print columns[0]
        line = sys.stdin.readline()
        nmol = int(line)
        print nmol
        for i in range(nmol):
            line = sys.stdin.readline()
            columns = line.split()
            x,y,z = map(float,columns[0:3])
            print y,z,x
    else:
        print line,
