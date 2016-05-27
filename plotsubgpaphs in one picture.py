import matplotlib.pyplot as plt
import networkx as nx


G=nx.compose(subgraph1,subgraph2)

plt.figure(num=None, figsize=(20, 20), dpi=80)
plt.axis('off')
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edge_labels(G,pos)

plt.show()