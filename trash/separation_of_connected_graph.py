import networkx as nx

#Here we determine our graph
G = nx.Graph()
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 2),('d','e',7),('e', 'k', 5),('d','k',6),('c','e',2)]
G.add_weighted_edges_from(e)


#Here we separate it to nonconnected subgraphs

subgraphs=list(nx.connected_component_subgraphs(G))

#Here we make minimal weighted cut by using stoer_wagner algorythm
cut_value, xer = nx.stoer_wagner(subgraphs[0])

#Here we form subgraph from cutted edges of our subgraph

H1=subgraphs[0].subgraph(xer[0])
H2=subgraphs[0].subgraph(xer[1])

#Here we print obtained cutted subgraphs
print H1.edges()
print H2.edges()