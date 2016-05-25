from trip import Trip
from path import Path
from taxi_tsp_bruteforce import get_best_path
from taxi_tsp_bruteforce import total_distance
from taxi_tsp_bruteforce import distance


def calc_dist_sum_of_separate_trips(trips):
    return sum([distance(trip.src, trip.dst) for trip in trips])


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


A = Trip((100, 300), (400, 100))
B = Trip((300, 100), (600, 200))
C = Trip((500, 100), (700, 400))
D = Trip((600, 350), (900, 200))
E = Trip((800, 150), (1000, 500))
F = Trip((900, 400), (1200, 300))
G = Trip((1050, 300), (1400, 500))
H = Trip((1300, 550), (1100, 200))

trips = [A, B, C, D, E, F, G, H]
# trips = [A, B, C, D, E]

all_partitions_set = list(get_partitions(set(range(len(trips)))))
# print(*all_partitions_set, sep='\n')
print(len(all_partitions_set))


min_sum = float('inf')


for partition_set in all_partitions_set:
    sum_dist = 0
    if max(len(partition) for partition in partition_set) > 4:
        # print('\nSkipped partition set', partition_set)
        continue
    for partition_index in partition_set:
        t = [trips[i] for i in partition_index]
        best_path = get_best_path(t)
        sum_dist += best_path.dist
    # print(partition_set)
    # print(sum_dist)
    if sum_dist < min_sum:
        min_sum = sum_dist
        min_partition_set = partition_set


print()
print(min_partition_set)
print(min_sum)
