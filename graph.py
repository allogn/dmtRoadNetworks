
# coding: utf-8

# In[120]:

import numpy as np
import networkx as nx
# import xml.sax not now
import copy
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

# N - number of nodes
# nodeEdges[i] - list of neighbour nodes of node i with weight (neighbour node,weight)
# nodeGPS - longitute and latitude of the node (lon,lat)
# nG - networkx DiGraph (the same as all the above if you can work only with networkx)
# ok?

def createFakeGraph(x,y):# x - width of our graph or number of nodes per string, y - height of our graph or number of strings
#     returns all the information about the graph
    N=x*y
    nodeEdges=[]
    nodeGPS=N*[(0,0)]
    for j in range(y):
        for i in range(x):
            nodeGPS[i+j*x]=(i+np.random.rand()/3,j+np.random.rand()/3)
            nodeEdges.append([])
            for dx in range(-1,2):
                if (i+dx>=0) and (i+dx<x):
                    for dy in range(-1,2):
                        if (j+dy>=0) and (j+dy<y):
                            if abs(dx)+abs(dy)==1:
                                nodeEdges[i+j*x].append((((dx+i)+(dy+j)*x),1))
    nG=nx.DiGraph()
    for n in range(N):
        nG.add_node(n)
        for e in range(len(nodeEdges[n])):
            nG.add_edge(n,nodeEdges[n][0],{'w':nodeEdges[n][1]})
    nx.graph.Graph.add_node
    return (N,nodeGPS,nodeEdges,nx)



def drawGraphAndPaths(N,nodeGPS,nodeEdges,paths=[[]],linecolor='k',linewidth=2):#N - number of nodes, nodeGPS - GPS coordinates of nodes
#     paths - a list of paths, where path is a list of nodes of some path, linecolor - a color of the lines for plot, linewidth - width for the plot
# it just draws the graph (with paths if you need them)
    plt.figure(figsize=(5,5))
    plt.plot([nodeGPS[n][0] for n in range(N)], [nodeGPS[n][1] for n in range(N)], 'ro')
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    for n in range(N):
        for e in range(len(nodeEdges[n])):
            x1.append(nodeGPS[n][0])
            y1.append(nodeGPS[n][1])
            x2.append(nodeGPS[nodeEdges[n][e][0]][0])
            y2.append(nodeGPS[nodeEdges[n][e][0]][1])
    plt.plot([x1,x2],[y1,y2], color='k', linestyle='-', linewidth=1)
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    for p in range(len(paths)):
        if (len(paths[p])==0):
            continue
        x1.append(nodeGPS[paths[p][0]][0])
        y1.append(nodeGPS[paths[p][0]][1])
        for n in range(len(paths[p])-1):
            x2.append(nodeGPS[paths[p][n+1]][0])
            y2.append(nodeGPS[paths[p][n+1]][1])
            x1.append(nodeGPS[paths[p][n+1]][0])
            y1.append(nodeGPS[paths[p][n+1]][1])
        if (len(x1)>0):
            x1.pop()
            y1.pop()
    plt.plot([x1,x2],[y1,y2], color=linecolor, linestyle='-', linewidth=7)

def generateOrders(N,howMuch):#N - number of nodes, howMuch - how much orders we want
#     returns a list of orders - a start node, a finish node and a number minutes from 0:00 of the start time (s,f,m)
    res=[]
    for i in range(howMuch):
        res.append((np.random.randint(N),np.random.randint(N),np.random.randint(24*60)))
    return res
    
#  Example of usage   
(N,nodeGPS,nodeEdges,nx)=createFakeGraph(10,20)
drawGraphAndPaths(N,nodeGPS,nodeEdges)
drawGraphAndPaths(N,nodeGPS,nodeEdges,[[0,1,2,12,22,32,42,43,53,54,64],[67,68,58,48,49],[199,198,197,196,195,185,175,165]],'g',2)
print generateOrders(N,20)


# In[ ]:



