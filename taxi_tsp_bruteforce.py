"""
Find the best route for set of trips
 by brute-force

TODO:
 Brunch-n-bound for cutting tree
 Heuristic sub-optimal solver
"""

from itertools import permutations
from trip import Trip
from path import Path


def get_best_path(trips):

    paths = get_all_possible_paths(trips)
    best_path = find_best_path(paths, trips)

    return best_path


def find_best_path(paths, trips):
    min_dist = float('inf')
    for path in paths:
        p = make_path(path, trips)
        dist = total_distance(p)

        if dist < min_dist:
            min_dist = dist
            min_path = path
    best_path = Path(min_path, min_dist)
    return best_path


def make_path(path, trips):
    path_points = []
    passengers_in_car_from = dict.fromkeys(trips, 0)
    for i, path_point in enumerate(path[:-1]):
        path_points.append(path_point.src if passengers_in_car_from[path_point] == 0 else path_point.dst)
        passengers_in_car_from[path_point] ^= 1  # XOR
    return path_points


def get_all_possible_paths(trips):
    """
    >>> len(get_all_possible_paths(['A','B']))
    4
    >>> len(get_all_possible_paths(['A','B','C']))
    60
    >>> len(get_all_possible_paths(['A','B','C','D']))
    1776
    """
    points = trips + trips
    perm = permutations(points)
    path_set = set(perm)
    for path in path_set.copy():
        if is_path_is_not_valid(path, trips):
            path_set.remove(path)
            continue
    return path_set


def is_path_is_not_valid(path, trips):
    """
    Car should always has a passenger, otherwise trips are separate

    >>> is_path_is_not_valid(['A','A','B','C','B','C'],['A','B','C'])
    True
    """
    passengers_in_car_from = dict.fromkeys(trips, 0)
    for i, path_point in enumerate(path[:-1]):

        passengers_in_car_from[path_point] ^= 1  # XOR

        if sum(passengers_in_car_from.values()) == 0:
            return True

    return False


def distance(point1, point2):
    """
    Returns the Euclidean distance of two points in the Cartesian Plane.

    >>> distance([3,4],[0,0])
    5.0
    >>> distance([3,6],[10,6])
    7.0
    """
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5


def total_distance(points):
    """
    Returns the length of the path passing through
    all the points in the given order.

    >>> total_distance([[1,2],[4,6]])
    5.0
    >>> total_distance([[3,6],[7,6],[12,6]])
    9.0
    """
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    A = Trip((1, 5), (1, 10))
    B = Trip((2, 7), (4, 15))
    C = Trip((5, 8), (3, 17))
    D = Trip((3, 5), (5, 16))

    trips = [A, B, C, D]

    best_path = get_best_path(trips)
    print(best_path.dist)






