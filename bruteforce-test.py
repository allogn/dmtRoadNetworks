from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx

from graph_separation import graph_separation
from path import *
from path_combinations import *
from metrica import trips_2_graph


# test-case
A = Client((100, 300), (400, 100), 'A')
B = Client((300, 100), (600, 200), 'B')
C = Client((500, 100), (700, 400), 'C')
D = Client((500, 350), (900, 200), 'D')
E = Client((800, 150), (1000, 500), 'E')
F = Client((900, 400), (1200, 300), 'F')
G = Client((1050, 300), (1400, 500), 'G')
H = Client((1300, 550), (1100, 200), 'H')


#BEST PATH DEMOP
clients = [A, B, C, D, E]
best_path = get_best_path(clients)
best_path.display()
# GUI of Best Path
canvas = Canvas(width=1400, height=700)
canvas.pack(expand=YES, fill=BOTH)
for t in clients:
    canvas.create_line(*t.src, *t.dst, width=2, arrow=LAST)
for i, p in enumerate(best_path.path_points[:-1]):
    canvas.create_line(*best_path.path_points[i], *best_path.path_points[i+1], width=4, arrow=LAST, fill='green')
# TODO draw best partition path
# for i, p in enumerate(best_path.points[:-1]):
mainloop()


#GRAPH SEGMENTATION
clients = [A, B, C, D, E, F, G, H]
edges = trips_2_graph(clients)
edges_named = []
for i, e in enumerate(edges):
    print('Edge from:', *e[0].name, 'To:', *e[1].name, 'Weight:', e[2])
    edges_named.append((e[0].name, e[1].name, e[2]))

Graph = nx.Graph()
Graph_names = nx.Graph()
Graph.add_weighted_edges_from(edges)
Graph_names.add_weighted_edges_from(edges_named)

# Here we separate it to non-connected sub-graphs
subgraphs = list(nx.connected_component_subgraphs(Graph))
subgraphs_names = list(nx.connected_component_subgraphs(Graph_names))
print('sub graphs', *[sub.nodes() for sub in subgraphs])

divided_sub_graphs = []
divided_sub_graphs_names = []
threshold = 4

# For each sub-graph we make a cuts until the size of each sub-graph will not exceed threshold
for i in range(len(subgraphs)):
    graph_separation(subgraphs[i], threshold, divided_sub_graphs)

for i in range(len(subgraphs_names)):
    graph_separation(subgraphs_names[i], threshold, divided_sub_graphs_names)

# As output we receive a list of sub-graphs which length doesn't exceed threshold.
print('divided sub graphs', *[sub.nodes() for sub in divided_sub_graphs])

composed_sub_graphs_names = nx.compose_all(divided_sub_graphs_names)

pos = nx.circular_layout(composed_sub_graphs_names)
plt.figure(num=None, figsize=(20, 20), dpi=80)
plt.axis('off')
nx.draw_networkx_nodes(composed_sub_graphs_names, pos, node_size=1200)
nx.draw_networkx_edges(composed_sub_graphs_names, pos)
nx.draw_networkx_labels(composed_sub_graphs_names, pos, font_size=32)
nx.draw_networkx_edge_labels(composed_sub_graphs_names, pos, font_size=18)
plt.show()


#BEST SOLUTION bruteforce
clients = [A, B, C, D, E]
best_path = get_best_path(clients)
sum_of_separate_trips = calc_dist_sum_of_separate_trips(clients)
# console output
print('\nClients:')
for c in clients:
    c.display()
min_partition_set, min_sum = find_best_partitioning(clients)
print('\nBEST SOLUTION\nmin partition set:', min_partition_set)
print('\nsum of separate trips = ', sum_of_separate_trips)
print('best dist = ', min_sum)
print('delta = ', sum_of_separate_trips - best_path.dist)


