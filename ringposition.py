import numpy as np
import wrap as wr

def RingPosition(ring,coord,box):
    c = np.zeros(3)
    center = wr.wrap(coord[ring[0]],box)
    for node in ring:
        d = coord[node] - center
        d = wr.wrap(d,box)
        c += d
    return center + c / len(ring)



def RingPositions(rings, coord,box):
    pos = []
    for ring in rings:
        pos.append(RingPosition(ring,coord,box))
    return pos



#it also works as a command
if __name__ == "__main__":
    import fileloaders as fl
    import sys
    file = sys.stdin
    while True:
        line = file.readline()
        if line == "":
            break
        #process @RSET
        columns = [x for x in line.split()]
        if 0 < len(columns):
            if columns[0] == "@RSET":
                nring_,ringsets = fl.LoadRNGS(file)
            elif columns[0] == "@RNGS":
                nnode_,rings = fl.LoadRNGS(file)
            elif columns[0] == "@BOX3":
                box = fl.LoadBOX3(file)
            elif columns[0] in ("@AR3A", "@NX3A", "@NX4A"):
                coord = fl.LoadAR3A(file)
    ringpositions    = RingPositions(rings, coord, box)
    ringsetpositions = RingPositions(ringsets, ringpositions, box)
    print "@BOX3"
    for x in box:
        print x,
    print
    print "@AR3A"
    print len(ringsets)
    for i in range(len(ringsets)):
        pos = ringsetpositions[i]
        for x in pos:
            print x,
        print

        
