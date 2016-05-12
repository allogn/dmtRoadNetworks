from tkinter import *
import Trip
import itertools
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
trace = 0
trips = []
edges = []


class CanvasEventsDemo:
    def __init__(self, parent=None):
        canvas = Canvas(width=800, height=600, bg='white')
        canvas.pack()
        canvas.bind('<ButtonPress-1>', self.onStart)
        canvas.bind('<B1-Motion>', self.onDrug)
        canvas.bind('<ButtonRelease-1>', self.onRelease)
        # canvas.bind('<Double-1>',      self.onClear)
        canvas.bind('<ButtonPress-3>', self.onB2Click)
        self.canvas = canvas
        self.drawn = None

    def onStart(self, event):
        self.start = event
        self.drawn = None

    def onDrug(self, event):
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = canvas.create_line(self.start.x, self.start.y, event.x, event.y, width=1, arrow=LAST)
        if trace: print(objectId)
        self.drawn = objectId

    def onRelease(self, event):
        self.end = event
        trip = Trip((self.start.x, self.start.y), (self.end.x, self.end.y))
        trips.append(trip)
        trip.display()

    def onB2Click(self, event):
        calcMetrics()


class Trip:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.dist = distance.euclidean(src, dst)

    def display(self):
        print("Src: ", self.src, ", Dst: ", self.dst, ", Dist: ", self.dist)


def getBestDist(A, B):
    return (distance.euclidean(A.src, B.src) +
            min(distance.euclidean(A.src, B.dst), distance.euclidean(A.dst, B.src), A.dist, B.dist) +
            distance.euclidean(A.dst, B.dst))


def calcMetrics():
    print('\nTrips:')
    for trip in trips:
        trip.display()
    print('\nPairs:')
    for a, b in itertools.combinations(trips, 2):
        # if isTimeTestFail(): continue
        bestDist = getBestDist(a, b)
        sumDist = a.dist + b.dist
        if bestDist > sumDist: continue
        minDist = min(a.dist, b.dist)
        maxDist = max(a.dist, b.dist)
        delta = sumDist - bestDist
        coPathCoeff = maxDist / bestDist
        effect = delta / bestDist
        weight = effect * coPathCoeff
        G.add_edge(a, b, weight=weight)
        print('edge is added', weight)

    pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, width=weight,)
    plt.axis('off')
    plt.savefig("weighted_graph.png")  # save as png
    plt.show()  # display

CanvasEventsDemo()
mainloop()
