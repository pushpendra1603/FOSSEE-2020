from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPainter

from Point import midpoint
from Circle import getNewPositionOfCircle
from State import State


class Canvas(QWidget):
    def __init__(self, window: QMainWindow, state: State):
        super(Canvas, self).__init__(parent=window)
        self.window = window
        self.state = state

    def mousePressEvent(self, event):
        self.window.status.setText("Select a CircleWidget")
        self.state.selectedCircle = None

    def paintEvent(self, event):
        painter = QPainter(self)
        for circle_set, line_label in self.state.circlesLineMap.items():
            circle_list = list(circle_set)
            circle1 = circle_list[0]
            circle2 = circle_list[1]
            line_label.move(*midpoint(circle1.center, circle2.center))
            (c1, c2) = getNewPositionOfCircle(circle1, circle2)
            painter.drawLine(*c1, *c2)
