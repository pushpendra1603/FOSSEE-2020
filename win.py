from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QToolBar, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPainter, QPixmap, QPen, QDrag, QColor
import random
import sys



class state:
    def __init__(self):
        self.list_circle = set([])
        self.list_lines = {}

class circ(QLabel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.resize(110, 110)
        self.x = random.randrange(0, 500)
        self.y = random.randrange(25, 500)
        self.color = QColor(*[random.randint(0, 255) for _ in range(3)])
        self.move(self.x, self.y)
        self.show()
        self.check = False
        self.label = QLabel("Circle", self)
        self.label.setStyleSheet("color : {}".format(self.color.name()))
        self.label.move(7, 48)
        self.label.resize(96, 15)
        self.label.show()
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.label()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.color, 3, Qt.SolidLine))
        painter.drawEllipse(5, 5, 100, 100)
        painter.end()

    def mousePressEvent(self, event):
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
    
    # def keyPressEvent(self, event):
    #     print("Hi")
    #     if event.key() == Qt.Key_Delete:
    #         if self.check:
    #             print("hello")
    #             del self

    # def mouseReleaseEvent(self, event):
    #     if self.__mousePressPos is not None:
    #         moved = event.globalPos() - self.__mousePressPos 
    #         if moved.manhattanLength() > 3:
    #             event.ignore()
    #             return

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

    def toolbar(self):
        toolbar = QToolBar("My Toolbar")
        addtool = QAction('Add',self)
        addtool.triggered.connect(self.addlabel)
        toolbar.addAction(addtool)
        toolbar.addAction(QAction('Generate',self))
        toolbar.addAction(QAction('Save',self))
        self.addToolBar(toolbar)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(QPen(Qt.green, 1.5, Qt.SolidLine))
    #     painter.drawEllipse(random.randrange(0,500), 0, 100, 100)
    #     label = QLabel("Hello World!!!")
    #     self.setCentralWidget(label)
    #     label.move(40,40)
    #     label.show()
    #     painter.end()
    #     return

    def addlabel(self):
        self.state.list_circle.add(circ(self))

    def keyPressEvent(self, event):
        print("Hi")
        if event.key() == Qt.Key_Delete:
            if self.cir1.check:
                print("hello")
                self.cir1.hide()


app = QApplication(sys.argv)

window = MainWindow()
# window.setStyleSheet("QMainWindow{background : 'white';}")
window.show()

app.exec_()