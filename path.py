from enum import IntEnum


class PointType(IntEnum):
    src = 0
    dst = 1


class Path:
    def __init__(self, points):
        self.points = points
        self.clients = set(points)
        self.path_points = []
        self.path_points_type = []

        passengers_in_car_from = dict.fromkeys(self.clients, 0)
        for path_point in points:
            self.path_points.append(path_point.src if passengers_in_car_from[path_point] == 0 else path_point.dst)
            self.path_points_type.append(PointType.src if passengers_in_car_from[path_point] == 0 else PointType.dst)
            passengers_in_car_from[path_point] ^= 1  # XOR

        self.dist = total_distance(self.path_points)
        self.sum_dist = calc_dist_sum_of_separate_trips(self.clients)
        # self.diviation = calc_diviation(self, points)

    def display(self):
        for i, p in enumerate(self.points):
            print(p.name, self.path_points_type[i].name, self.path_points[i])
        print(self.dist)
        print(self.sum_dist)


    for i, p in enumerate(path.points):
        print(p.name, path.path_points_type[i].name, path.path_points[i])


    for client in path.clients:
        client_path = []
        in_car = False
        for i, client_point in enumerate(path.points):
            if client == client_point and path.path_points_type[i] == PointType.src:
                in_car = True
            if in_car:
                client_path.append(path.path_points[i])
            if client == client_point and path.path_points_type[i] == PointType.dst:
                break

    for c in path.clients:


def calc_dist_sum_of_separate_trips(trips):
    return sum([distance(trip.src, trip.dst) for trip in trips])


def distance(point1, point2):
    """
    Returns the Euclidean distance of two points in the Cartesian Plane.

    >>> distance([3,4],[0,0])
    5.0
    >>> distance([3,6],[10,6])
    7.0
    """
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5


def total_distance(points):
    """
    Returns the length of the path passing through
    all the points in the given order.

    >>> total_distance([[1,2],[4,6]])
    5.0
    >>> total_distance([[3,6],[7,6],[12,6]])
    9.0
    >>> total_distance([(100, 300), (300, 100), (400, 100), (500, 100), (600, 200), (600, 350), (700, 400), (900, 200)])
    1168.9101800615372
    """
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])
