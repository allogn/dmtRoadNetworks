from itertools import permutations
from trip import Trip
from path import Path


def get_best_path(trips):

    points = trips + trips
    perm = permutations(points)
    path_set = set(perm)

    for path in path_set.copy():

        if is_path_is_not_valid(path):
            path_set.remove(path)
            continue

    path_points = []
    passengers_in_car_from = dict.fromkeys(trips, 0)

    for i, path_point in enumerate(path[:-1]):

        path_points.append(path_point.src if passengers_in_car_from[path_point]==0 else path_point.dst)
        passengers_in_car_from[path_point] ^= 1  # XOR

    best_path = Path(path_points)

    return best_path


def is_path_is_not_valid(path):
    passengers_in_car_from = dict.fromkeys(trips, 0)
    for i, path_point in enumerate(path[:-1]):

        passengers_in_car_from[path_point] ^= 1  # XOR

        if sum(passengers_in_car_from.values()) == 0:
            return True

    return False


A = Trip((1, 5), (1, 10))
B = Trip((2, 7), (4, 15))
C = Trip((5, 8), (3, 17))
D = Trip((3, 5), (5, 16))

trips = [A, B, C, D]

best_path = get_best_path(trips)
print(best_path.dst)






