from Circle import Circle
from Label import Label


class State:
    def __init__(self):
        self.selectedCircle: Circle = None
        self.circlesSet: set[Circle] = set()
        self.circlesLineMap: dict[tuple[Circle, Circle], Label] = {}
