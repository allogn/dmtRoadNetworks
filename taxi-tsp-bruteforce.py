from itertools import permutations
from trip import Trip


def get_best_path(path_set):
    for path in path_set.copy():

        if is_path_is_not_valid(path):
            path_set.remove(path)
            continue


    return best_path


def is_path_is_not_valid(path):
    passengers_in_car = dict.fromkeys(trips, 0)
    for i, path_point in enumerate(path[:-1]):

        is_car_is_empty = True if sum(passengers_in_car.values()) == 0 else False
        passengers_in_car[path_point] ^= 1  # XOR

        if is_car_is_empty and i > 0:
            return True

    return False


# A = Trip((1, 5), (1, 10))
# B = Trip((1, 5), (1, 10))
# C = Trip((1, 5), (1, 10))
# D = Trip((1, 5), (1, 10))

A = Trip('A', 'a')
B = Trip('B', 'b')
C = Trip('C', 'c')
D = Trip('D', 'd')


# trips = ['A', 'B', 'C', 'D']
trips = [A, B, C, D]

points = trips + trips
perm = permutations(points)
path_set = set(perm)

get_best_path(path_set)




# passengers_in_car = dict.fromkeys(trips, 0)
# print(passengers_in_car)
# passengers_in_car[path_point] ^= 1  # XOR

print(*path_set, sep='\n')
print(len(path_set))



