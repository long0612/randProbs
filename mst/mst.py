# Minimum spanning tree (MST) algorithms
#
# Long Le
# University of Illinois
#

import numpy as np
import matplotlib.pyplot as plt
from pqdict import minpq

class Node:
    def __init__(self,x):
        self.val = x

class Edge:
    def __init__(self,n0,n1,w):
        self.ePts = set([n0,n1]) # end points
        self.w = w # weight

# union-find set
class UnionFindSet:
    def __init__(self,iterable):
        self.memMap = {} # membership map
        self.id = 0 # membership ID
        for item in iterable:
            self.memMap[item] = self.id
            self.id += 1

    def find(self,a):
        return self.memMap.get(a,None)

    def union(self,a,b):
        aId = self.memMap[a]
        bId = self.memMap[b]
        for key,val in self.memMap.items():
            if val == aId or val == bId:
                self.memMap[key] = self.id # new id
        self.id += 1

def Prim(nodes,edges):
    # https://en.wikipedia.org/wiki/Prim's_algorithm

    C = minpq() # cheapest cost of a connection to a node
    E = {} # the edge providing that cheapest connection
    for node in nodes:
        C[node] = np.infty
        E[node] = None
    # forest
    edgesF = set()

    while len(C) > 0:
        node = C.pop()

        if E[node] != None:
            edgesF.add(E[node])

        for edge in edges:
            u,v = edge.ePts
            if u == node:  
                ngb = v
            elif v == node:
                ngb = u
            else:
                continue

            if ngb in C:
                if edge.w < C[ngb]:
                    C[ngb] = edge.w
                    E[ngb] = edge

    return edgesF

def Kruskal(nodes,edges):
    # https://en.wikipedia.org/wiki/Kruskal's_algorithm

    # sort all edges in non-decreasing order of weights
    edgesSort = minpq()
    for edge in edges:
        edgesSort[edge] = edge.w
    edgesF = set()

    ufset = UnionFindSet(nodes)

    for edge in edgesSort.popkeys():
        if len(edgesF) == len(nodes)-1:
            break
        u,v = edge.ePts
        if ufset.find(u) != ufset.find(v):
            edgesF.add(edge)
            ufset.union(u,v)

    return edgesF

def visualize(nodes,edges,locMap):
    plt.figure(figsize=(10,10))
    for node in nodes:
        loc = locMap[node]
        plt.scatter(loc[0],loc[1],lw=32)
        plt.annotate(str(node.val),xy=loc,xytext=(loc[0]+.1,loc[1]+.1),fontsize=15)
    for edge in edges:
        u,v =  edge.ePts
        locU = locMap[u]
        locV = locMap[v]
        #print('loc = %s' % loc)
        add_label(plt.plot([locU[0],locV[0]],[locU[1],locV[1]])[0],'%.2f' % edge.w)

    axes = plt.axes()
    axes.axison=False
    plt.show()
    return

def add_label(line,label,size=20,color=None):
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()
    xStart = np.percentile(xdata,55)
    xEnd = np.percentile(xdata,45)
    yStart = np.percentile(ydata,55)
    yEnd = np.percentile(ydata,45)

    line.axes.annotate(label,
            xy=((xEnd+xStart)/2,(yEnd+yStart)/2),size=18)
