from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx
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

clients = [A, B, C, D, E]
edges = trips_2_graph(clients)
print('\nEdges:', *(e[2] for e in edges), sep='\n')

# clients = [A, B]
# clients = [A, B, C, D, E, F, G, H]

# calculation
# sum_of_separate_trips = calc_dist_sum_of_separate_trips(clients)
# best_path = get_best_path(clients)
# div = calc_diviation(best_path)

#console output
# print('\nClients:')
# for c in clients:
#     c.display()

# print('\nBEST PATH trough ALL trips\nWay-points:')
# print(*best_path.path_points, sep='\n')
# print('best_path dist = ', best_path.dist)
# print('sum of separate trips = ', sum_of_separate_trips)
# print('delta = ', sum_of_separate_trips - best_path.dist)
#
# min_partition_set, min_sum = find_best_partitioning(clients)
# print('\nBEST SOLUTION\nmin partition set:',min_partition_set)
# print('best dist = ', min_sum)
#
#

#
# path = get_best_path(clients)
# path.display()
#
#
# # GUI
# canvas = Canvas(width=1400, height=700)
# canvas.pack(expand=YES, fill=BOTH)
#
# for t in clients:
#     canvas.create_line(*t.src, *t.dst, width=2, arrow=LAST)
# for i, p in enumerate(best_path.path_points[:-1]):
#     canvas.create_line(*best_path.path_points[i], *best_path.path_points[i+1], width=4, arrow=LAST, fill='green')
# # TODO draw best partition path
# # for i, p in enumerate(best_path.points[:-1]):
#
# mainloop()
#
# Graph = nx.Graph()
# Graph.add_weighted_edges_from(edges)
# pos = nx.random_layout(Graph)
# nx.draw_networkx_nodes(Graph, pos)
# nx.draw_networkx_edges(Graph, pos)
#
# plt.axis('off')
# plt.show()
