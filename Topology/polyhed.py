#!/usr/bin/env python
#
#This program may not work for liquid water.
#It is designed specifically for voronoi network where z is always 4 and the hull is convex.

import sys
import networkx as nx

i=1
debug = 0
MAXFRAGSIZE = 20
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == "-x":
        i+=1
        MAXRINGSIZE = int(sys.argv[i])
    elif arg == "-l":
        i += 1
        MAXFRAGSIZE = int(sys.argv[i])
    elif arg == "-d":
        debug = 1
    elif arg == "-n":
        NOCHECKCOMPO = 1
    i+=1

#my @PLACED;
#my @RINGSINTHEPOLY;
#my @NUMRINGSATTHENODE;
#my $NPOLY=0;
#my $NUMNODES;
#my %EDGES;
#my $ORIGINALCOMPO;
#
#When $RSET is non-zero, fragments are output in @RSET format.
#(@RSET is the format for set of rings.)
#
#my $RSET = 1;
#
#When $NGPH is non-zero, fragments are output in @NGPH format.
#
#my $NGPH = 0;

#
#list rings having the specified 3 successive nodes (center, left, and right)
#




#reorder the ring noders so as to start from the first node
def reorder(ring,first,second):
    s = ring.index(first)
    if ring[s-1] == second:
        r = [ring[i] for i in range(s,s-len(ring),-1)]
    else:
        r = [ring[i] for i in range(s-len(ring),s)]
    return r


#get two lists of nodes (rings) and make a large ring.
def MergeRings(ring1,ring2,first,second,debug=0):
    r1 = reorder(ring1,first,second)
    r2 = reorder(ring2,first,second)
    if debug: print("#",r1,"+",r2)
    #zipper motion
    head=0
    while r1[head-1] == r2[head-1]:
        head -= 1
        if head == -len(r1):
            return []
    tail=1
    while r1[tail+1-len(r1)] == r2[tail+1-len(r2)]:
        tail += 1
    #unshared nodes of the rings
    rest1 = set(r1) - set([r1[i] for i in range(head,tail+1)])
    rest2 = set(r2) - set([r2[i] for i in range(head,tail+1)])
    #if the remaining parts of the ring have common nodes,
    if len(rest1 & rest2) != 0:
        #not a simple ring
        return None
    ring = [r1[i] for i in range(tail-len(r1),head)]
    ring += [r2[i] for i in range(head,tail-len(r2),-1)]
    if debug:
        print("#",head,tail,ring,rest1,rest2,rest1 & rest2)
    return ring
    


def LoadRNGS(file,debug=0):
    line = file.readline()
    n = int(line)
    rings = []
    while True:
        line=file.readline()
        if len(line) == 0:
            break
        if debug: print("#",line, end=' ')
        columns = [int(x) for x in line.split()]
        if debug: print("#",line,columns,n)
        if columns[0] == 0:
            break
        nodes = columns[1:]
        rings.append(nodes)
    return n,rings
        


def Triplets(nodes):
    tri = []
    for i in range(len(nodes)):
        tri.append((nodes[i-2],nodes[i-1],nodes[i]))
    return tri




def Edges(nodes):
    ed = []
    for i in range(len(nodes)):
        ed.append((nodes[i-1],nodes[i]))
    return ed



            
        



#Look up all the polyhedral fragments (vitrites) in the given set of rings.
def Polyhed(_rings, debug=0):
    #Local functions

    def RegisterTriplets(nodes,ringid):
        for triplet in Triplets(nodes):
            if triplet not in _RingsAtATriplet:
                _RingsAtATriplet[triplet] = []
            _RingsAtATriplet[triplet].append(ringid)
            tr = tuple(reversed(triplet))
            if tr not in _RingsAtATriplet:
                _RingsAtATriplet[tr] = []
            _RingsAtATriplet[tr].append(ringid)

    def RegisterEdges(nodes,ringid):
        for edge in Edges(nodes):
            if edge not in _RingsAtAnEdge:
                _RingsAtAnEdge[edge] = []
            _RingsAtAnEdge[edge].append(ringid)
            ed = tuple(reversed(edge))
            if ed not in _RingsAtAnEdge:
                _RingsAtAnEdge[ed] = []
            _RingsAtAnEdge[ed].append(ringid)

    #Return True if the given fragment contains rings that are not the member of the fragment.
    def ContainsExtraRing(fragment):
        tris = set()
        allnodes = set()
        #A fragment is a set of ring IDs.
        for ringid in fragment:
            nodes = _rings[ringid]
            allnodes |= set(nodes)
            tris |= set(Triplets(nodes))
        for tri in tris:
            for ringid in _RingsAtATriplet[tri]:
                if ringid not in fragment:
                    #if all the nodes of a ring is included in the fragment,
                    nodes = _rings[ringid]
                    if len(set(nodes) - allnodes) == 0:
                        return True
                    #print(fragment,ringid)
        return False
    #Grow up a set of rings by adding new ring on the perimeter.
    #Return the list of polyhedron.
    #origin is the ring ID of the first face in the polyhedron
    def Progress(origin, peri, fragment, numRingsOnTheNode, debug=0):
        #Here we define a "face" as a ring belonging to the (growing) polyhedron.
        if debug:
            print("#",peri,fragment)
        if len(fragment) > MAXFRAGSIZE:
            #print("#LIMITTER")
            return False
        #if the perimeter closes,
        if peri == []:
            #If the polyhedron has internal vertices that are not a part of the polyhedron (i.e. if the polyhedron does not divide the total network into to components)
            if not IsDivided(fragment):
                #If the fragment does not contain any extra ring whose all vertices belong to the fragment but the ring is not a face,
                if not ContainsExtraRing(fragment):
                    #Add the fragment to the list.
                    #A fragment is a set of ring IDs of the faces
                    _vitrites.add(frozenset(fragment))
            #Search finished.
            return True
        #If the perimeter is still open,
        for i in range(len(peri)):
            #If any vertex on the perimeter is shared by more than two faces,
            if numRingsOnTheNode[peri[i]] > 2:
                if debug: print("#Failed(2)")
                return False
        for i in range(len(peri)):
            #Look up the node on the perimeter which is shared by two faces.
            if numRingsOnTheNode[peri[i]] == 2:
                #Reset the frag
                trynext = False
                #Three successive nodes around the node i
                center = peri[i]
                left   = peri[i-1]
                right  = peri[i+1-len(peri)] #Avoid to refer the out-of-list element
                #Reset the frag
                success = False
                if debug:
                    print("Next triplet:",left,center,right)
                if (left,center,right) in _RingsAtATriplet:
                    if debug:
                        print("Here rings are:", _RingsAtATriplet[(left,center,right)])
                    for ringid in _RingsAtATriplet[(left,center,right)]:
                        if debug:
                            print("#Next:", ringid)
                        #if the ring is new and its ID is larger than the origin,
                        if origin < ringid and not ringid in fragment:
                            nodes = _rings[ringid]
                            #Add the ring as a face and extend the perimeter
                            newperi = MergeRings(peri, nodes, center,right,debug=0)
                            if debug:
                                print("#Result:", newperi)
                            # result is not a simple ring
                            if newperi == None:
                                trynext = True
                                if debug:
                                    print("#Try next!")
                            else:
                                for node in nodes:
                                    numRingsOnTheNode[node] += 1
                                if debug:
                                    mult = [numRingsOnTheNode[i] for i in newperi]
                                    print("#",peri, nodes, edge, newperi,mult)
                                result = Progress(origin, newperi, fragment | set([ringid,]), numRingsOnTheNode, debug=debug)
                                for node in nodes:
                                    numRingsOnTheNode[node] -= 1
                                #if result == True:
                                #    return True
                #it might be too aggressive
                if not trynext:
                    break
        if debug: print("#Failed to expand perimeter",peri,fragment)
        return False


    #return the list of neighboring vertices for a given set of vertices
    def IsDivided(fragment):
        nodes = set()
        for ring in fragment:
            nodes |= set(_rings[ring])
        G2 = _G.copy()
        ebunch = []
        for i in nodes:
            for j in _G.neighbors(i):
                ebunch.append((i,j))
        #G2.remove_edges_from(ebunch)
        G2.remove_nodes_from(nodes)
        return nx.number_connected_components(G2) != _ncompo

    _RingsAtATriplet = dict()
    _RingsAtAnEdge = dict()
        
    for ringid in range(len(_rings)):
        RegisterTriplets(_rings[ringid],ringid)
        RegisterEdges(_rings[ringid],ringid)
    #For counting the number of components separated by a polyhedral fragment
    _G = nx.Graph()

    for ring in _rings:
        _G.add_cycle(ring)
    _ncompo = nx.number_connected_components(_G)

    _vitrites = set()
    #The first ring
    for ringid in range(len(_rings)):
        peri = _rings[ringid]
        fragment = set([ringid])
        edge = tuple(peri[0:2])
        numRingsOnTheNode = [0 for i in range(nnode)]
        #increment the number-of-rings-at-a-node counter
        #for each node on the first ring.
        for node in peri:
            numRingsOnTheNode[node] = 1
        if debug:
            print("#Candid:",ringid,_RingsAtAnEdge[edge])
        #The second ring, which is adjacent to the first one.
        for ringid2 in _RingsAtAnEdge[edge]:
            #The second one must have larger ring ID than the first one.
            if ringid < ringid2:
                nodes = _rings[ringid2]
                #Make the perimeter of two rings.
                newperi = MergeRings(peri, nodes, edge[0],edge[1],debug=0)
                if newperi != None:
                    #increment the number-of-rings-at-a-node counter
                    #for each node on the second ring.
                    for node in nodes:
                        numRingsOnTheNode[node] += 1
                    if debug:
                        mult = [numRingsOnTheNode[i] for i in newperi]
                        print(peri, nodes, edge, newperi,mult)
                    #Expand the perimeter by adding new faces to the polyhedron.
                    Progress(ringid, newperi, set([ringid,ringid2]), numRingsOnTheNode, debug)
                    #decrement the number-of-rings-at-a-node counter
                    #for each node on the second ring.
                    for node in nodes:
                        numRingsOnTheNode[node] -= 1
    return _vitrites


#file = open("q_400K_10GPa_v000.delaunay.tetra.adj.rngs")
#file = open("mux121.delaunay.tetra.adj.rngs")
file = sys.stdin
while True:
    line = file.readline()
    if len(line) == 0:
        break
    columns = line.split()
    if len(columns):
        if columns[0] == "@RNGS":
            nnode, Rings = LoadRNGS(file)
            break

vitrites = Polyhed(Rings)
        
print("@FSEP")
print("@RSET")
print(len(Rings))
for vitrite in vitrites:
    print(" ".join([str(i) for i in [len(vitrite)]+sorted(vitrite)]))
print(0) #terminator
