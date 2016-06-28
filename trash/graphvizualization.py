import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
e = [('a', 'b', 3), ('b', 'c', 9), ('a', 'c', 5), ('c', 'd', 2),('d','e',7),('e', 'k', 5),('d','k',6),('c','e',2)]
G.add_weighted_edges_from(e)


plt.figure(num=None, figsize=(20, 20), dpi=80)
plt.axis('off')
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos, node_size=1200)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos, font_size=32)
nx.draw_networkx_edge_labels(G,pos,font_size=18)
plt.show()