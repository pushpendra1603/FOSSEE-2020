from PyQt5.QtWidgets import QLabel, QInputDialog, QMainWindow
from PyQt5.QtCore import Qt

from Point import Point


class Label(QLabel):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter | Qt.AlignHCenter | Qt.AlignVCenter)

    def center(self):
        return Point(self.x() + self.width() / 2, self.y() + self.height() / 2)

    def move(self, x, y):
        super(Label, self).move(x - self.width() / 2, y - self.height() / 2)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            text, ok = QInputDialog.getText(self, 'change {} to'.format(self.text()), 'New name:')
            if ok:
                self.setText(text)
                self.updateStatusText("Name changed to {}".format(text))

    def updateStatusText(self, msg):
        parent = self
        while not isinstance(parent, QMainWindow):
            parent = parent.parent()
        parent.statusBar().showMessage(msg)
