import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("QLabel{color : 'white';}")
        canvas = QtGui.QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.btn = QtWidgets.QPushButton("Hello", self)
        self.btn.show()
        self.btn.clicked.connect(self.draw_something)

    def draw_something(self):
        self.btn.hide()
        painter = QtGui.QPainter(self.label.pixmap())
        painter.setPen(QtGui.QPen(Qt.green,  1, Qt.SolidLine))
        painter.drawEllipse(100, 100, 200, 200)
        # painter.drawText(200, 200, "Hello World!!!!!")
        label = QtWidgets.QLabel("hello")
        label.setStyleSheet("QLabel{color : 'red';}")
        label.move(100,100)
        label.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()