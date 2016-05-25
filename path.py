class Path:
    def __init__(self, points, dist=None):
        self.points = points
        self.dist = dist
        # self.sum_dist = self.calc_dist_sum_of_separate_trips()
        # self.diviation = dist

    def get_clients(self):
        return


def calc_diviation(trips, path):
    sum([distance(point, path.points[index + 1]) for index, point in enumerate(path.points[:-1])])


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
