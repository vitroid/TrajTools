#hcp triple ice

from math import *
NX = 3
NY = 2
NZ = 2
hy = sqrt(3)/2.
hz = sqrt(3.0/2.0)*2./3.
box = (NX*1.0, NY*2*hy, NZ*hz*2)
coord = []
for ix in range(NX):
    for iy in range(NY):
        for iz in range(NZ):
            coord.append((1.0 * ix, hy*2*iy, hz*iz*2))
            coord.append((1.0 * ix + 0.5, hy* (2*iy+1), hz*iz*2))
            coord.append((1.0 * ix + 0.5, hy* (2*iy+1./3.), hz*(iz*2+1)))
            coord.append((1.0 * ix, hy* (2*iy+4./3), hz*(iz*2+1)))

def dist(coord,i,j):
    sum = 0.0
    for k in range(3):
        d = coord[i][k] - coord[j][k]
        d -= floor(d/box[k]+0.5)*box[k]
        sum += d**2
    return sum


nei = [set() for i in range(len(coord))]

for i in range(len(coord)):
    for j in range(len(coord)):
        if j != i:
            if dist(coord,i,j) < 1.1:
                nei[i].add(j)

tri = dict()
quartet = []
for i in range(len(coord)):
    for j1 in nei[i]:
        for j2 in nei[i]:
            if j1 != j2:
                sum = 0.0
                for k in range(3):
                    d1 = coord[j1][k] - coord[i][k]
                    d1 -= floor(d1/box[k]+0.5)*box[k]
                    d2 = coord[j2][k] - coord[i][k]
                    d2 -= floor(d2/box[k]+0.5)*box[k]
                    sum += d1 * d2
                tri[(i,j1,j2)] = (sum + 1./3.)**2
                fourth = nei[j1] & nei[j2]
                for k in fourth:
                    quartet.append((i,j1,j2,k))


net = dict()
for i in range(len(coord)):
    for j in range(len(coord)):
        d = [0.0] * 3
        for k in range(3):
            d[k] = coord[i][k] - coord[j][k]
            d[k] -= floor(d[k]/box[k]+0.5)*box[k]
        if 0.45 < d[0] < 0.55 and hy-0.05 < d[1] < hy+0.05 and -0.05 < d[2] < 0.05:
            if not net.has_key(i):
                net[i] = set()
            net[i].add(j)
            if not net.has_key(j):
                net[j] = set()
            net[j].add(i)
        if 0.95 < d[0] < 1.05 and -0.05 < d[1] < +0.05 and -0.05 < d[2] < 0.05:
            if not net.has_key(i):
                net[i] = set()
            net[i].add(j)
            if not net.has_key(j):
                net[j] = set()
            net[j].add(i)

    
def totalenergy(net, tri):
    ep = 0.0
    for i in net:
        for j1 in net[i]:
            for j2 in net[i]:
                if j1 < j2:
                    ep += tri[i,j1,j2]
    return ep

ep = totalenergy(net,tri)
print ep
print len(quartet)

def trial(ep, net, tri, quartet,beta):
    #lookup parallel bonds and exchange them
    while True:
        i,j1,j2,k = quartet[random(0,len(quartet)-1)]
        if j1 in net[i] and j2 in net[k] and not j1 in net[k] and not j2 in net[i]:
            break
    # i -- j1, k--j2
    delta = 0.0
    for x in net[i]:
        if x != j1:
            delta -= tri[i,j1,x]
            delta += tri[i,j2,x]
    for x in net[k]:
        if x != j2:
            delta -= tri[k,j2,x]
            delta += tri[k,j1,x]
    for x in net[j1]:
        if x != i:
            delta -= tri[j1,i,x]
            delta += tri[j1,k,x]
    for x in net[j2]:
        if x != k:
            delta -= tri[j2,k,x]
            delta += tri[j2,i,x]
    if delta < 0 or random() < exp(-beta*delta):
        net[i].add(j2)
        net[k].add(j1)
        net[i].remove(j1)
        net[k].remove(j2)
        net[j2].add(i)
        net[j1].add(k)
        net[j1].remove(i)
        net[j2].remove(k)
        ep += delta
        print FRAME, ep, delta
    return ep


def line3d(c,d):
    line(c[0]*30+c[1]*3,c[1]*8+c[2]*83,
                 (c[0]+d[0])*30+(c[1]+d[1])*3,(c[1]+d[1])*8+(c[2]+d[2])*83)


def snapshot(net,nei,coord):
    translate(30,10)
    strokewidth(0.5)
    stroke(0,0,0,0.2)
    for i in range(len(net)):
        for j in nei[i]:
            d = [0.] * 3
            for k in range(3):
                d[k] = coord[j][k] - coord[i][k]
                d[k] -= floor(d[k]/box[k]+0.5)*box[k]
            line3d(coord[i],d)
    
    stroke(0)
    for i in range(len(net)):
        for j in net[i]:
            d = [0.] * 3
            for k in range(3):
                d[k] = coord[j][k] - coord[i][k]
                d[k] -= floor(d[k]/box[k]+0.5)*box[k]
            line3d(coord[i],d)
                
            

size(300,300)
speed(30)
def draw():
    global ep
    beta = (FRAME % 300)*0.1 + 1
    for i in range(10):
        ep = trial(ep,net,tri,quartet,beta)
    snapshot(net,nei,coord)

