from trip import Trip
from path import Path
from taxi_tsp_bruteforce import get_best_path
from taxi_tsp_bruteforce import total_distance
from taxi_tsp_bruteforce import distance

def calc_dist_sum_of_sepparate_trips(trips):
    return sum([distance(trip.src, trip.dst) for trip in trips])

A = Trip((100, 300), (400, 100))
B = Trip((300, 100), (600, 200))
C = Trip((500, 100), (700, 400))
D = Trip((600, 350), (900, 200))
E = Trip((800, 150), (1000, 500))
F = Trip((900, 400), (1200, 300))
G = Trip((1050, 300), (1400, 500))


# trips = [A, B, C, D, E, F]
trips = [A, B, C, D, E, F, G]

sum_of_separate_trips = calc_dist_sum_of_sepparate_trips(trips)
best_path = get_best_path(trips)


print(best_path.dist)
print(sum_of_separate_trips)
print(sum_of_separate_trips - best_path.dist)


print(*best_path.points, sep='\n')

