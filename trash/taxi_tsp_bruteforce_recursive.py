"""
Sandbox for experiments with recursion
not working yet
"""
import math

from itertools import permutations
from trip import Trip



trips = [Trip('A', 'a'), Trip('B', 'b'), Trip('C', 'c')]
[trip.display() for trip in trips]


def foo(paths, path, dst, waiting, in_car):
    if len(waiting) == 0:
        perm = permutations(in_car)
        # print([p for p in perm])
        paths.append(path.append([p for p in perm]))
        return paths
    # if len(in_car) == 1:
    #     return waiting * foo(trips, waiting - 1, in_car + 1)
    # return waiting * foo(trips, waiting - 1, in_car + 1) \
    #     + in_car * foo(trips, waiting, in_car - 1)
    return paths



# xpaths = foo(paths, path, (), (), ('a','b','c'))
paths = []
path = []
perm = permutations(('a', 'b', 'c'))
[paths.append(p) for p in perm]
# paths.append([path.append(p) for p in perm])
# for p in perm:

# print(*p) for p in perm], sep='\n')
print('-----')
print(*paths, sep='\n')




def getPaths(trips):

    xpaths=foo(len(trips) - 2, 2)
    # print(*xpaths)
    paths = []
    for i in trips:
        for j in trips:
            if j == i: continue
            path = []
            path.append(i.src)
            path.append(j.src)
            # path.append(*xpaths)
            paths.append(path)
    return paths



# pths = getPaths(trips)
# print(*pths, sep='\n')
# print(len(pths))
