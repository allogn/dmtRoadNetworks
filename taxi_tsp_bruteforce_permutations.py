"""
Sandbox for experiments with permutations
"""

from itertools import permutations


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

    trips = ['A', 'B', 'C', 'D']
    path_set = get_all_possible_paths(trips)

    print(*path_set, sep='\n')
    print(len(path_set))
