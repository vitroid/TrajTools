#!/usr/bin/env python

#pairlist module
import math
import itertools


def rint(x):
    return math.floor(x+0.5)



def ArrangeAddress(xyz,grid,box):
    #divide the simulation cell into grids
    nx,ny,nz = grid
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
    return residents


#return labels of the molecules near the given grid cell.
def neighbors(address,residents,grid):
    ix,iy,iz = address
    nx,ny,nz = grid
    #neighbor cells
    nei = []
    for jx in range(-1,2):
        kx = ix + jx
        kx %= nx
        for jy in range(-1,2):
            ky = iy + jy
            ky %=  ny
            for jz in range(-1,2):
                kz = iz + jz
                kz %= nz
                a2 = (kx,ky,kz)
                if residents.has_key(a2):
                    nei += residents[a2]
    return nei
    

def pairlist(xyz,rc,box):
    #residents in each grid cell
    nx = int(math.floor(box[0]/rc))
    ny = int(math.floor(box[1]/rc))
    nz = int(math.floor(box[2]/rc))
    grid = (nx,ny,nz)
    residents = ArrangeAddress(xyz,grid,box)
    
    pair = []
    #key-value pairs in the dictionary
    donecellpair = set()
    for address in residents:
        resident = residents[address]
        ix,iy,iz = address
        #neighbor cells
        for jx in range(-1,2):
            kx = ix + jx
            kx %= nx
            for jy in range(-1,2):
                ky = iy + jy
                ky %=  ny
                for jz in range(-1,2):
                    kz = iz + jz
                    kz %= nz
                    a2 = (kx,ky,kz)
                    if address == a2:
                        for a,b in itertools.combinations(resident,2):
                            pair.append((a,b))
                    else:
                        if residents.has_key(a2):
                            if not frozenset((address,a2)) in donecellpair:
                                donecellpair.add(frozenset((address,a2)))
                                for a in resident:
                                    for b in residents[a2]:
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
