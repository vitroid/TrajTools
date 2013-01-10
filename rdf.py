#!/usr/bin/env python
#Fast RDF

import math

def gridpairs(mols, cutoff, box):
    directory = dict()
    gridsize = [cutoff] * 3
    ngrid = [0] * 3
    for dim in range(3):
        ngrid[dim] = int(box[dim] / cutoff)
        gridsize[dim] = box[dim] / ngrid[dim]
    for i in range(len(mols)):
        a = [0]*3
        for dim in range(3):
            a[dim] = int(mols[i][dim]/gridsize[dim])
        a = tuple(a)
        if not directory.has_key(a):
            directory[a] = []
        directory[a].append(i)
    done = dict()
    pairs = []
    #pairs in the same grid
    for cell in directory:
        done[(cell,cell)] = 1
        memb = directory[cell]
        for i in memb:
            for j in memb:
                if i<j:
                    s = 0.0
                    for k in range(3):
                        d = mols[i][k] - mols[j][k]
                        s += d**2
                    r = math.sqrt(s)
                    pairs.append(r)
    #different cell pairs
    #nc = 0
    for x in range(ngrid[0]):
        for y in range(ngrid[1]):
            for z in range(ngrid[2]):
                cell1 = (x,y,z)
                for dx in range(-1,+2):
                    for dy in range(-1,+2):
                        for dz in range(-1,2):
                            nx = x + dx
                            ny = y + dy
                            nz = z + dz
                            nx = (nx+ngrid[0]) % ngrid[0]
                            ny = (ny+ngrid[1]) % ngrid[1]
                            nz = (nz+ngrid[2]) % ngrid[2]
                            cell2 = (nx,ny,nz)
                            if not done.has_key((cell1,cell2)):
                                #nc += 1
                                done[(cell1,cell2)] = 1
                                done[(cell2,cell1)] = 1
                                if directory.has_key(cell1) and directory.has_key(cell2):
                                    for i in directory[cell1]:
                                        for j in directory[cell2]:
                                            s = 0.0
                                            for k in range(3):
                                                d = mols[i][k] - mols[j][k]
                                                d -= math.floor( d / box[k] + 0.5 ) * box[k]
                                                s += d**2
                                            r = math.sqrt(s)
                                            pairs.append(r)
    #print nc,ngrid
    return pairs
                
    


def simplepairs(mols,box):
    pairdistance = []
    for i in range(len(mols)):
        for j in range(i+1,len(mols)):
            s = 0.0
            for k in range(3):
                d = mols[i][k] - mols[j][k]
                d -= math.floor( d / box[k] + 0.5 ) * box[k]
                s += d**2
            r = math.sqrt(s)
            pairdistance.append(r)
    return pairdistance
    

def calc(mols, box, binw=1.0, cutoff=0):
    if cutoff:
        pairs = gridpairs(mols, cutoff, box)
    else:
        pairs = simplepairs(mols,box)
    distrib = []
    for r in pairs:
        ir = int(r / binw +0.5)
        if cutoff == 0 or r < cutoff:
            if len(distrib) <= ir:
                #extend dist
                distrib.extend([0.0]*(ir+1-len(distrib)))
            distrib[ir] += 1
    return distrib
