import itertools
from path_combinations import *


def calc_metrics(trips, Graph):
    edges = []
    for a, b in itertools.combinations(trips, 2):
        #TODO if isTimeTestFail(): continue
        bestDist = get_best_dist_for_two(a, b)
        sumDist = calc_dist_sum_of_separate_trips((a, b))
        if bestDist > sumDist:
            continue

        weight = weigh(a, b, bestDist, sumDist)
        edges.append((a, b, weight))
    return edges


def weigh(a, b, bestDist, sumDist):
    dist_a = distance(a.src, a.dst)
    dist_b = distance(b.src, b.dst)
    maxDist = max(dist_a, dist_b)
    delta = sumDist - bestDist
    coPathCoeff = maxDist / bestDist
    effect = delta / bestDist
    weight = effect * coPathCoeff
    return weight


# def calc_metrics_for_any_k(trips, Graph):
#     for a, b in itertools.combinations(trips, 2):
#         # if isTimeTestFail(): continue
#         # bestDist = Path.get_best_path(a, b).dist
#         sumDist = calc_dist_sum_of_separate_trips((a, b))
#         if bestDist > sumDist: continue
#         dist_a = distance(a.src, a.dst)
#         dist_b = distance(b.src, b.dst)
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
    d1 = distance(a.src, b.src) + distance(b.src, a.dst) + distance(a.dst, b.dst)
    d2 = distance(a.src, b.src) + distance(b.src, b.dst) + distance(b.dst, a.dst)
    d3 = distance(b.src, a.src) + distance(a.src, a.dst) + distance(a.dst, b.dst)
    d4 = distance(b.src, a.src) + distance(a.src, b.dst) + distance(b.dst, a.dst)
    return min(d1, d2, d3, d4)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
