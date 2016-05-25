# """
# Find the best route for set of trips
#  by brute-force
#
# TODO:
#  Brunch-n-bound for cutting tree
#  Heuristic sub-optimal solver
# """
#
#
# from itertools import permutations
# from trip import Trip
# from path import *
#
#
# def get_best_path(trips):
#     """
#     >>> A = Trip((100, 300), (400, 100))
#     >>> B = Trip((300, 100), (600, 200))
#     >>> C = Trip((500, 100), (700, 400))
#     >>> D = Trip((600, 350), (900, 200))
#     >>> trips = [A, B, C, D]
#     >>> best_path = get_best_path(trips)
#     >>> print(best_path.dist)
#     1168.9101800615372
#     """
#     paths = get_all_possible_paths(trips)
#     best_path = find_min_path(paths, trips)
#
#     return best_path
#
#
# def find_min_path(paths, trips):
#     min_dist = float('inf')
#     for path in paths:
#         p = make_path(path, trips)
#         dist = total_distance(p)
#
#         if dist < min_dist:
#             min_dist = dist
#             min_path = p
#     min_path = Path(min_path, min_dist)
#     return min_path
#
#
# def make_path(path, trips):
#     path_points = []
#     passengers_in_car_from = dict.fromkeys(trips, 0)
#     for path_point in path:
#         path_points.append(path_point.src if passengers_in_car_from[path_point] == 0 else path_point.dst)
#         passengers_in_car_from[path_point] ^= 1  # XOR
#     return path_points
#
#
# def get_all_possible_paths(trips):
#     """
#     >>> len(get_all_possible_paths(['A','B']))
#     4
#     >>> len(get_all_possible_paths(['A','B','C']))
#     60
#     >>> len(get_all_possible_paths(['A','B','C','D']))
#     1776
#     """
#     points = trips + trips
#     perm = permutations(points)
#     path_set = set(perm)
#     for path in path_set.copy():
#         if is_path_is_not_valid(path, trips):
#             path_set.remove(path)
#             continue
#     return path_set
#
#
# def is_path_is_not_valid(path, trips):
#     """
#     Car should always has a passenger, otherwise trips are separate
#
#     >>> is_path_is_not_valid(['A','A','B','C','B','C'],['A','B','C'])
#     True
#     """
#     passengers_in_car_from = dict.fromkeys(trips, 0)
#     for i, path_point in enumerate(path[:-1]):
#
#         passengers_in_car_from[path_point] ^= 1  # XOR
#
#         if sum(passengers_in_car_from.values()) == 0:
#             return True
#
#     return False
#
#
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
#
#     A = Trip((100, 300), (400, 100))
#     B = Trip((300, 100), (600, 200))
#     C = Trip((500, 100), (700, 400))
#     D = Trip((600, 350), (900, 200))
#
#     trips = [A, B, C, D]
#
#     best_path = get_best_path(trips)
#     print(best_path.dist)
#     print(*best_path.points, sep='\n')
