from itertools import permutations


def filter_paths(path_set):
    for path in path_set.copy():
        passengers = dict.fromkeys(trips, 0)

        for i, point in enumerate(path[:-1]):

            is_car_is_empty = True if sum(passengers.values()) == 0 else False
            passengers[point] ^= 1  # XOR

            if is_car_is_empty and i > 0:
                path_set.remove(path)
                break

    return path_set

trips = ['A', 'B', 'C', 'D']
points = trips + trips
perm = permutations(points)
path_set = set(perm)
filter_paths(path_set)

# print(len(paths))
print(len(path_set))
