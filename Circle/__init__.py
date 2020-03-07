import math

from Label import Label
from Point import Point, translate, lineAngle


class Circle:
    def __init__(self, center: Point, radius: int, label: Label):
        self.radius = radius
        self.center = center
        self.label = label


def getCirclePointAtAngle(position: Point, radius: int, angle: float):
    newPosition = Point(0, 0)
    delta = translate(position, newPosition)
    circleEdgePoint = Point(radius * math.cos(angle), radius * math.sin(angle))
    return circleEdgePoint + delta


def getNewPositionOfCircle(circle1: Circle, circle2: Circle):
    angleBetweenTwoCircles = lineAngle(circle1.center, circle2.center)
    return (getCirclePointAtAngle(circle1.center, circle1.radius, angleBetweenTwoCircles),
            getCirclePointAtAngle(circle2.center, circle2.radius, math.pi + angleBetweenTwoCircles),)
