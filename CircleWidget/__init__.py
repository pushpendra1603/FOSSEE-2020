from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
import random

from Circle import Circle
from Label import Label
from State import State
from Utils import circleId, lineId
from Point import Point

DIAMETER = 100
THICKNESS = 3


class CircleWidget(Label):
    def __init__(self, canvas: QWidget, state: State):
        super(CircleWidget, self).__init__(parent=canvas)
        self.__mouseMovePos = None
        self.canvas = canvas
        self.state = state
        self.resize((DIAMETER + 2 * THICKNESS), (DIAMETER + 2 * THICKNESS))
        position = Point(random.randrange(0, self.canvas.width()),
                         random.randrange(0, self.canvas.height()))
        self.color = QColor(*[random.randint(0, 255) for _ in range(3)])
        self.circle = Circle(position, DIAMETER / 2, None)
        self.circle.label = Label("Circle{}".format(next(circleId)), self)
        self.circle.label.resize((DIAMETER - 2 * THICKNESS), (DIAMETER - 2 * THICKNESS))
        self.circle.label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter | Qt.AlignVCenter)
        self.circle.label.move(THICKNESS + DIAMETER / 2, THICKNESS + DIAMETER / 2)
        self.circle.label.show()
        self.move(*self.circle.center)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.color, THICKNESS, Qt.SolidLine))
        painter.drawEllipse(THICKNESS, THICKNESS, DIAMETER, DIAMETER)
        painter.end()
        self.move(*self.circle.center)
        self.canvas.update()

    def removeCircle(self):
        self.close()
        self.state.circlesSet.remove(self.circle)
        linesToRemove: list[tuple[tuple[Circle, Circle], Label]]
        linesToRemove = list(filter(lambda x: self.circle in x[0], self.state.circlesLineMap.items()))
        for circles_set, lines in linesToRemove:
            lines.close()
            del self.state.circlesLineMap[circles_set]
        del self.state.selectedCircle
        self.state.selectedCircle = None
        self.canvas.window.status.setText("")

    def mousePressEvent(self, event):
        self.__mouseMovePos = None
        if event.buttons() == Qt.LeftButton:
            if self.state.selectedCircle not in [None, self.circle]:
                key: tuple[Circle, Circle] = tuple(sorted([self.state.selectedCircle, self.circle], key=id))
                if key not in self.state.circlesLineMap:
                    lineLabel = Label("Line{}".format(next(lineId)), self.canvas)
                    lineLabel.show()
                    self.state.circlesLineMap[key] = lineLabel
                    self.canvas.window.status.setText("{} Drawn from {} to {}"
                                                      .format(lineLabel.text(),
                                                              self.state.selectedCircle.label.text(),
                                                              self.circle.label.text()))
            self.state.selectedCircle = self.circle
            self.canvas.window.status.setText(self.state.selectedCircle.label.text())
            self.__mouseMovePos = event.globalPos()
            self.setFocus()
        if event.buttons() == Qt.RightButton:
            self.removeCircle()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            diffPos = Point(diff.x(), diff.y())
            self.circle.center = self.circle.center + diffPos
            self.__mouseMovePos = globalPos

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and self.state.selectedCircle is not None:
            self.removeCircle()
