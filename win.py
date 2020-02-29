from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QToolBar, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPainter, QPixmap, QPen, QDrag, QColor
import math
import random
import sys

def get_unique_id():
    i = 1
    while True:
        yield i
        i += 1

circle_id = get_unique_id()
line_id = get_unique_id()


class state:
    def __init__(self):
        self.selected_circle = None
        self.list_circles = set()
        self.list_lines = {}

def midpoint(pos1, pos2):
    return ((pos1.x()+pos2.x())/2, (pos1.y()+pos2.y())/2)

class circ(QLabel):

    def __init__(self, parent, state):
        super(circ, self).__init__(parent=parent)
        self.resize(110, 110)
        self.state = state
        self.parent = parent
        self.x = random.randrange(0, 500)
        self.y = random.randrange(25, 500)
        self.color = QColor(*[random.randint(0, 255) for _ in range(3)])
        self.move(self.x, self.y)
        self.label = QLabel("Circle{}".format(next(circle_id)), self)
        self.label.setStyleSheet("color : {}".format(self.color.name()))
        self.label.move(7, 48)
        self.label.resize(96, 15)
        self.label.show()
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.show()
    
    def paintEvent(self, event):
        # print("ABC")
        painter = QPainter(self)
        painter.setPen(QPen(self.color, 3, Qt.SolidLine))
        painter.drawEllipse(5, 5, 100, 100)
        painter.end()
        self.parent.update()

    def mousePressEvent(self, event):
        print(type(event))
        print(event)
        self.parent.statusBar().showMessage(self.label.text())
        if self.state.selected_circle not in [None,self]:
            key = tuple(sorted([self.state.selected_circle, self], key = id))
            if key not in self.state.list_lines:
                # self.state.list_lines["Line{}".format(next(line_id))] = set([self.state.selected_circle, self])
                self.state.list_lines[key] = "Line{}".format(next(line_id))
                self.parent.repaint()
                self.parent.statusBar().showMessage("Line Drawn from {} to {}".format(self.state.selected_circle.label.text(), self.label.text()))
        self.state.selected_circle = self
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.__mouseMovePos = globalPos

    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog.getText(self, 'Name Box', 'Circle Name:')   
        if ok:
            self.label.setText(text)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            self.x = self.pos().x()
            self.y == self.pos().y()
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

    # def label(self):
    #     label = QLabel("Hello World!!!", self)
    #     label.move(50, 50)
    #     label.show()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.showMaximized()
        self.state = state()
        self.setWindowTitle("My Awesome App")
        self.toolbar()
        # self.label = QLabel()
        # self.canvas = QPixmap(500, 500)
        # self.label.setPixmap(self.canvas)
        # self.setCentralWidget(self.label)
        print(self.__dir__())

    # def repaint(self, *args, **kwargs):
    #     super(MainWindow, self).repaint(*args, **kwargs)
    #     for line_label, set_circles in self.state.list_lines.items():
    #         circle_list = list(set_circles)
    #         circleA = circle_list[0]
    #         circleB = circle_list[1]
    #         print("line drawin from {} to {}".format(circleA.pos(), circleB.pos()))


    def toolbar(self):
        toolbar = QToolBar("My Toolbar")
        addtool = QAction('Add',self)
        addtool.triggered.connect(self.add_circle)
        toolbar.addAction(addtool)
        toolbar.addAction(QAction('Generate',self))
        toolbar.addAction(QAction('Save',self))
        self.addToolBar(toolbar)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for set_circles, line_label in self.state.list_lines.items():
            circle_list = list(set_circles)
            circleA = circle_list[0]
            circleB = circle_list[1]
            # labelofline = QLabel(line_label, self)
            painter.drawText(*midpoint(circleA.pos(), circleB.pos()), line_label)
            # labelofline.move(*midpoint(circleA.pos(), circleB.pos()))
            # labelofline.show()
            painter.drawLine(circleA.pos().x()+55, circleA.pos().y()+55, circleB.pos().x()+55, circleB.pos().y()+55)
            # print("line drawin from {} to {}".format(circleA.pos(), circleB.pos()))

    def mousePressEvent(self, event):
        print("Empty")
        self.statusBar().showMessage("")
        self.state.selected_circle = None

    def add_circle(self):
        self.state.list_circles.add(circ(self, self.state))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.state.selected_circle != None:
            print("HAHAHAH")
            self.state.selected_circle.close()
            print(type(self.state.selected_circle))
            print(self.state.selected_circle.render.__doc__)
            print(self.state.selected_circle.repaint.__doc__)
            self.state.list_circles.remove(self.state.selected_circle)
            linesToRemove = list(filter(lambda x: self.state.selected_circle in x[0], self.state.list_lines.items()))
            for circle_set, label in linesToRemove:
                del self.state.list_lines[label]
            del self.state.selected_circle
            self.state.selected_circle = None


app = QApplication(sys.argv)

window = MainWindow()
# window.setStyleSheet("QMainWindow{background : 'white';}")
window.show()

app.exec_()