#!/usr/bin/env python

#pairlist module
import math
import itertools


def rint(x):
    return math.floor(x+0.5)

def pairlist(xyz,rc,box):
    #divide the simulation cell into grids
    nx = math.floor(box[0]/rc)
    ny = math.floor(box[1]/rc)
    nz = math.floor(box[2]/rc)
    #residents in each grid cell
    residents = dict()
    for i in range(len(xyz)):
        mol = xyz[i]
        x,y,z = mol[0:3]
        x -= rint( x / box[0] ) * box[0]
        y -= rint( y / box[1] ) * box[1] 
        z -= rint( z / box[2] ) * box[2]
        ix = x / box[0] * nx
        iy = y / box[1] * ny
        iz = z / box[2] * nz
        if ix<0:
            ix += nx
        if iy<0:
            iy += ny
        if iz<0:
            iz += nz
        ix = int(ix)
        iy = int(iy)
        iz = int(iz)
        address = (ix,iy,iz)
        if not residents.has_key(address):
            residents[address] = []
        residents[address].append(i)
    pair = []
    #key-value pairs in the dictionary
    for address in residents:
        resident = residents[address]
        ix,iy,iz = address
        #neighbor cells
        for jx in range(-1,2):
            kx = ix + jx
            if kx < 0:
                kx += nx
            for jy in range(-1,2):
                ky = iy + jy
                if ky < 0:
                    ky += ny
                for jz in range(-1,2):
                    kz = iz + jz
                    if kz < 0:
                        kz += nz
                    if ( jx==0 and jy==0 and jz==0 ):
                        for a,b in itertools.combinations(resident,2):
                            pair.append((a,b))
                    else:
                        print kx,ky,kz
                        if residents.has_key((kx,ky,kz)):
                            for a in resident:
                                for b in residents[(kx,ky,kz)]:
                                    pair.append((a,b))
    return pair

def test():
    xyz = []
    for x in range(4):
        for y in range(4):
            for z in range(4):
                xyz.append((x,y,z))
    box = (4,4,4)
    rc = 1.0
    print pairlist(xyz,rc,box)

#test()
