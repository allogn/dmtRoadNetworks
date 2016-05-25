from tkinter import *
import networkx as nx
from trip import Trip
from path import Path
from taxi_tsp_bruteforce import get_best_path


A = Trip((100, 300), (400, 100))
B = Trip((300, 100), (600, 200))
C = Trip((500, 100), (700, 400))
D = Trip((600, 350), (900, 200))
E = Trip((800, 150), (1000, 500))
F = Trip((900, 400), (1200, 300))
G = Trip((1050, 300), (1400, 500))


# trips = [A, B, C, D, E, F]
trips = [A, B, D, E, F, G]


canvas = Canvas(width=1500, height=700)
canvas.pack(expand=YES, fill=BOTH)

for t in trips:
    canvas.create_line(*t.src, *t.dst, width=2, arrow=LAST)


best_path = get_best_path(trips)
print(best_path.dist)
print(*best_path.points, sep='\n')

for i, p in enumerate(best_path.points[:-1]):
    canvas.create_line(*best_path.points[i], *best_path.points[i+1], width=4, arrow=LAST, fill='green')


mainloop()
