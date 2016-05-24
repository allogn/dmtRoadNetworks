from itertools import permutations


def filter_paths(path_set):
    for path in path_set.copy():

        if is_path_is_not_valid(path):
            path_set.remove(path)
            continue

    return path_set


def is_path_is_not_valid(path):
    passengers_in_car = dict.fromkeys(trips, 0)
    for i, path_point in enumerate(path[:-1]):

        is_car_is_empty = True if sum(passengers_in_car.values()) == 0 else False
        passengers_in_car[path_point] ^= 1  # XOR

        if i > 0 and is_car_is_empty :
            return True

    return False


trips = ['A', 'B', 'C', 'D']
points = trips + trips
perm = permutations(points)
path_set = set(perm)
filter_paths(path_set)


print(*path_set, sep='\n')
print(len(path_set))



