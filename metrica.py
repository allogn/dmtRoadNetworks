import itertools

from dmtRoadNetworks.path import calc_deviation, calc_dist_sum_of_separate_trips
from dmtRoadNetworks.path_combinations import *
from dmtRoadNetworks.shortest_path import get_shortest_dist


def trips_2_graph(trips):
    edges = []
    for a, b in itertools.combinations(trips, 2):
        #TODO if isTimeTestFail(): continue
        best_dist = get_best_dist_for_two(a, b)
        sum_dist = calc_dist_sum_of_separate_trips((a, b))
        if best_dist > sum_dist:
            continue
        weight = weigh(a, b, best_dist, sum_dist)
        edges.append((a, b, weight))
    return edges


def weigh(a, b, bestDist, sumDist):
    dist_a = get_shortest_dist(a.src, a.dst)
    dist_b = get_shortest_dist(b.src, b.dst)
    # maxDist = max(dist_a, dist_b)
    delta = sumDist - bestDist
    # coPathCoeff = maxDist / bestDist
    effect = delta / sumDist
    p = get_best_path((a, b))
    deviation = calc_deviation(p)
    weight = effect * deviation
    return weight


# def calc_metrics_for_any_k(trips, Graph):
#     for a, b in itertools.combinations(trips, 2):
#         # if isTimeTestFail(): continue
#         # bestDist = Path.get_best_path(a, b).dist
#         sumDist = calc_dist_sum_of_separate_trips((a, b))
#         if bestDist > sumDist: continue
#         dist_a = get_shortest_dist(a.src, a.dst)
#         dist_b = get_shortest_dist(b.src, b.dst)
#         minDist = min(dist_a, dist_b)
#         maxDist = max(dist_a, dist_b)
#         delta = sumDist - bestDist
#         coPathCoeff = maxDist / bestDist
#         effect = delta / bestDist
#         weight = effect * coPathCoeff
#         edges.append((a, b, weight))
#         print('edge is added', weight)
#     return edges


def get_best_dist_for_two(a, b):
    d1 = get_shortest_dist(a.src, b.src) + get_shortest_dist(b.src, a.dst) + get_shortest_dist(a.dst, b.dst)
    d2 = get_shortest_dist(a.src, b.src) + get_shortest_dist(b.src, b.dst) + get_shortest_dist(b.dst, a.dst)
    d3 = get_shortest_dist(b.src, a.src) + get_shortest_dist(a.src, a.dst) + get_shortest_dist(a.dst, b.dst)
    d4 = get_shortest_dist(b.src, a.src) + get_shortest_dist(a.src, b.dst) + get_shortest_dist(b.dst, a.dst)
    return min(d1, d2, d3, d4)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
