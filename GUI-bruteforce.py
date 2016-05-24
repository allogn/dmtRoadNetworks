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


trips = [A, B, C, D, E]


canvas = Canvas(width=1330, height=700)
canvas.pack(expand=YES, fill=BOTH)

canvas.create_line(*A.src, *A.dst, width=2, arrow=LAST)
canvas.create_line(*B.src, *B.dst, width=2, arrow=LAST)
canvas.create_line(*C.src, *C.dst, width=2, arrow=LAST)
canvas.create_line(*D.src, *D.dst, width=2, arrow=LAST)
canvas.create_line(*E.src, *E.dst, width=2, arrow=LAST)


best_path = get_best_path(trips)
print(best_path.dist)
print(*best_path.points, sep='\n')

canvas.create_line(*best_path.points[0], *best_path.points[1], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[1], *best_path.points[2], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[2], *best_path.points[3], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[3], *best_path.points[4], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[4], *best_path.points[5], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[5], *best_path.points[6], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[6], *best_path.points[7], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[7], *best_path.points[8], width=4, arrow=LAST, fill='green')
canvas.create_line(*best_path.points[8], *best_path.points[9], width=4, arrow=LAST, fill='green')




mainloop()
