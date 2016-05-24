class Path:
    def __init__(self, points):
        self.points = points
        self.dst = self.total_distance(points)

    def display(self):
        print("Src: ", self.src, ", Dst: ", self.dst)

    def distance(self, point1, point2):
        """
        Returns the Euclidean distance of two points in the Cartesian Plane.

        >>> distance([3,4],[0,0])
        5.0
        >>> distance([3,6],[10,6])
        7.0
        """
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

    def total_distance(self, points):
        """
        Returns the length of the path passing through
        all the points in the given order.

        >>> total_distance([[1,2],[4,6]])
        5.0
        >>> total_distance([[3,6],[7,6],[12,6]])
        9.0
        """
        return sum([self.distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])
