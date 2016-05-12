import sys
from copy import deepcopy
import heapq as hp


def singleSourseDijkstra(G, start, target):

    intree = deepcopy(G.node)
    distance = deepcopy(G.node)
    parent = deepcopy(G.node)
    #intree = [False]*len(G.node)
    #distance[:] = sys.maxint   #How to make it without loops&
    #parent[:] = None   #How to make it without loops&

    for i in distance:
        intree[i] = False
        distance[i] = sys.maxint
        parent[i] = None

    distance[distance.keys()[0]] = 0
    v = start
    h = []
    while (intree[v] == False):
        intree[v] = True
        p = G.edge[v]
        for j in p:
            weight = p[j]['weight']
            if distance[j] > (distance[v] + weight):
                distance[j] = distance[v] + weight
                parent[j] = v
                hp.heappush(h, (distance[j], j))
        if len(h)>0:
            v = hp.heappop(h)[1]

    u = target
    path = []
    while True:
        path += u
        if u == start: break
        u = parent[u]

    path.reverse()
    return path

import networkx as nx

G = nx.Graph()
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 12)]
G.add_weighted_edges_from(e)

print singleSourseDijkstra(G, 'a', 'd'), ' - my implementation'
print nx.dijkstra_path(G,'a','d'), ' - networkxnx implementation'

G1=nx.Graph()
e1=[('a','b',16),('a','d',35),('a','c',9),('b','d',12),
    ('b','e',25),('c','d',15),('c','f',22),('d','e',14),
    ('d','f',17),('d','g',19),('e','g',8), ('f','g',14)]
G1.add_weighted_edges_from(e1)
print singleSourseDijkstra(G1, 'a', 'g'), ' - my implementation'
print nx.dijkstra_path(G1, 'a', 'g'), ' - networkxnx implementation'
print singleSourseDijkstra(G1, 'a', 'f'), ' - my implementation'
print nx.dijkstra_path(G1, 'a', 'f'), ' - networkxnx implementation'