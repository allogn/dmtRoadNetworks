import networkx as nx

#Here we determine our graph
G = nx.Graph()
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 12),('e','f',4)]
G.add_weighted_edges_from(e)

#Here we separate it to nonconnected subgraphs

graphs=list(nx.connected_component_subgraphs(G))

#Here we output obtained result

print graphs[0].nodes()