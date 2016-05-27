from itertools import permutations
from client import Client
from path import *


def find_best_partitioning(trips):

    all_partitions_set = list(get_partitions(set(range(len(trips)))))
    min_partition_set = ()
    min_sum = float('inf')

    for partition_set in all_partitions_set:
        sum_dist = 0
        # if max(len(partition) for partition in partition_set) > 4:
        #     # print('\nSkipped partition set', partition_set)
        #     continue
        for partition_index in partition_set:
            t = [trips[i] for i in partition_index]
            best_path = get_best_path(t)
            sum_dist += best_path.dist
        # print(partition_set)
        # print(sum_dist)
        if sum_dist < min_sum:
            min_sum = sum_dist
            min_partition_set = partition_set

    return min_partition_set, min_sum


def get_partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i & 1].add(item)
            i >>= 1
        for b in get_partitions(parts[1]):
            yield [parts[0]] + b


def get_best_path(trips):
    """
    >>> A = Client((100, 300), (400, 100))
    >>> B = Client((300, 100), (600, 200))
    >>> C = Client((500, 100), (700, 400))
    >>> D = Client((600, 350), (900, 200))
    >>> trips = [A, B, C, D]
    >>> best_path = get_best_path(trips)
    >>> print(best_path.dist)
    1168.9101800615372
    """
    paths = get_all_possible_paths(trips)
    best_path = find_min_path(paths)

    return best_path


def find_min_path(paths):
    min_dist = float('inf')
    for p in paths:
        pth = Path(p)
        if pth.dist < min_dist:
            min_dist = pth.dist
            min_path = pth
    return min_path


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
