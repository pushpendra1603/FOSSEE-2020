import random
from PyQt5 import QtCore, QtGui, QtWidgets


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setFixedHeight(300)

        lay = QtWidgets.QHBoxLayout(self)

        for letter in "ABCDEFG":
            label = QtWidgets.QLabel(letter, alignment=QtCore.Qt.AlignCenter)
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            label.setStyleSheet("background-color: {}".format(color.name()))
            lay.addWidget(label)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())