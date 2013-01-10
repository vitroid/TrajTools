#!/usr/bin/env python

import sys


oxygens = []
mins = [0] *3
maxs = [0] *3

for line in sys.stdin:
    columns = line.split()
    if columns[0] == 'HETATM':
        id = columns[2]
        if id[0] == 'O':
            #last 3 numbers
            #print columns
            xyz = map(float,columns[len(columns)-3:len(columns)])
            #print xyz
            for k in range(3):
                if xyz[k] < mins[k]:
                    mins[k] = xyz[k]
                if xyz[k] > maxs[k]:
                    maxs[k] = xyz[k]
            oxygens.append(xyz)

#initial guess
box = [maxs[0]-mins[0]+2.5,maxs[1]-mins[1]+2.5,maxs[2]-mins[2]+2.5]

import math
#list distances to four nearest neighbor molecules
def trial(oxygens,box):
    nearest = 100.0
    farthest = 0.0
    for i in oxygens:
        l = []
        cnt = 0
        for j in oxygens:
            d = 0
            for k in range(3):
                e = (i[k] - j[k])
                if e > box[k]/2:
                    e -= box[k]
                elif e < -box[k]/2:
                    e += box[k]
                d += e**2
            l.append(math.sqrt(d))
            cnt+=1
        l = sorted(l)
        #print l[1:5]
        #find the nearest distance to the nearest neighbors
        if l[1] < nearest:
            nearest = l[1]
        #find the farthest distance to the fourth farthest neighbor
        if l[4] > farthest:
            farthest = l[4]
    return nearest,farthest

import random

bestn,bestf = trial(oxygens, box)
width = bestf - bestn

rejects = 0
while True:
    newbox = list(box)
    newbox[0] += (random.random() - 0.7)
    newbox[1] += (random.random() - 0.7)
    newbox[2] += (random.random() - 0.7)
    n,f = trial(oxygens, newbox)
    #the narrower the better
    if f-n <= width:
        if f-n < width:
            rejects = 0
        width = f-n
        box = list(newbox)
    rejects += 1
    if rejects > 300:
        break
    print rejects,width,f-n,n,f,newbox
print box

    


        
