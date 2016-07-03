from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx

from dmtRoadNetworks.path import calc_dist_sum_of_separate_trips
from dmtRoadNetworks.path_combinations import *
from dmtRoadNetworks.metrica import calc_metrics
from dmtRoadNetworks.trip import Trip

Graph = nx.Graph()
edges = []

#testcase
A = Trip((100, 300), (400, 100))
B = Trip((300, 100), (600, 200))
C = Trip((500, 100), (700, 400))
D = Trip((500, 350), (900, 200))
E = Trip((800, 150), (1000, 500))
F = Trip((900, 400), (1200, 300))
G = Trip((1050, 300), (1400, 500))
H = Trip((1300, 550), (1100, 200))

trips = [C, D]
# trips = [D, E]
# trips = [A, B, C, D, E, F, G, H]

#calculation
sum_of_separate_trips = calc_dist_sum_of_separate_trips(trips)
best_path = get_best_path(trips)
min_partition_set, min_sum = find_best_partitioning(trips)
edges = calc_metrics(trips, Graph)


#console output
print('\nTrips:')
for trip in trips:
    trip.display()

print('\nBEST PATH trough ALL trips\nWay-points:')
print(*best_path.points, sep='\n')
print('best_path dist = ', best_path.dist)
print('sum of separate trips = ', sum_of_separate_trips)
print('delta = ', sum_of_separate_trips - best_path.dist)

print('\nBEST SOLUTION\nmin partition set:',min_partition_set)
print('best dist = ', min_sum)

print('\nEdges:')
print(*(e[2] for e in edges), sep='\n')


#GUI
canvas = Canvas(width=1400, height=700)
canvas.configure(background='white')
canvas.pack(expand=YES, fill=BOTH)

for t in trips:
    canvas.create_line(*t.src, *t.dst, width=2, arrow=LAST)
for i, p in enumerate(best_path.points[:-1]):
    canvas.create_line(*best_path.points[i], *best_path.points[i+1], width=4, arrow=LAST, fill='green')
# TODO draw best partition path
# for i, p in enumerate(best_path.points[:-1]):

mainloop()

Graph.add_weighted_edges_from(edges)
pos = nx.random_layout(Graph)
nx.draw_networkx_nodes(Graph, pos)
nx.draw_networkx_edges(Graph, pos)

plt.axis('off')
plt.show()
