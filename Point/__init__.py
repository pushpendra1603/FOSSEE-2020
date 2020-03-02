import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tup = (x, y)

    def __getitem__(self, item):
        return self.tup[item]

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Position(x: {}, y: {})".format(self.x, self.y)


def translate(position: Point, newPosition: Point):
    return position - newPosition


def lineAngle(position1: Point, position2: Point):
    return math.atan2((position2.y - position1.y), (position2.x - position1.x))


def midpoint(point1: Point, point2: Point):
    return (point1.x + point2.x) / 2, (point1.y + point2.y) / 2
