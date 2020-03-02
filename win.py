from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QToolBar, QLabel, QInputDialog, QScrollArea, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QPixmap
from fpdf import FPDF
from collections import namedtuple
import math
import random
import sys





Position = namedtuple("position", ['x', 'y'])


def getUniqueId():
    i = 1
    while True:
        yield i
        i += 1


circleId = getUniqueId()
lineId = getUniqueId()


def midpoint(point1, point2):
    return ((point1.x + point2.x) / 2, (point1.y + point2.y) / 2)


class state:
    def __init__(self):
        self.selectedCircle = None
        self.circlesSet = set()
        self.circlesLineMap = {}


class Label(QLabel):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter | Qt.AlignHCenter | Qt.AlignVCenter)

    def center(self):
        return Position(self.x() + self.width()/2, self.y() + self.height()/2)

    def move(self, x, y):
        super(Label, self).move(x - self.width()/2, y - self.height()/2)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            text, ok = QInputDialog.getText(self, 'change {} to'.format(self.text()), 'New name:')
            if ok:
                self.setText(text)


class Circle(Label):
    def __init__(self, canvas, state, diameter=100):
        super(Circle, self).__init__(parent=canvas)
        self.canvas = canvas
        self.state = state
        self.diameter = diameter
        self.thickness = 3
        self.cen = self.center()
        self.resize((self.diameter + 2*self.thickness), (self.diameter + 2*self.thickness))
        self.move(random.randrange(0, self.canvas.width()) + self.width()/2, random.randrange(0, self.canvas.height()) + self.height()/2)
        self.color = QColor(*[random.randint(0, 255) for _ in range(3)])
        self.circleLabel = Label("Circle{}".format(next(circleId)), self)
        self.circleLabel.resize((self.diameter - 2*self.thickness), (self.diameter - 2*self.thickness))
        # self.setStyleSheet("""
        # QLabel {
        #     background-color: rgba(255,0,0,0.5);
        #     color: Black;
        #     }
        # """)
        # self.circleLabel.setStyleSheet("""
        # QLabel {
        #     background-color: rgba(0,255,0,0.5);
        #     color: Black;
        #     }
        # """)
        self.circleLabel.setAlignment(Qt.AlignCenter | Qt.AlignHCenter | Qt.AlignVCenter)
        self.circleLabel.move(self.thickness + diameter/2, self.thickness + diameter/2)
        self.circleLabel.show()
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.color, self.thickness, Qt.SolidLine))
        painter.drawEllipse(self.thickness, self.thickness, self.diameter, self.diameter)
        self.move(*self.cen)
        painter.end()
        self.canvas.update()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.canvas.window.statusBar().showMessage(self.circleLabel.text())
            if self.state.selectedCircle not in [None,self]:
                key = tuple(sorted([self.state.selectedCircle, self], key = id))
                if key not in self.state.circlesLineMap:
                    lineLabel = Label("Line{}".format(next(lineId)), self.canvas)
                    lineLabel.show()
                    self.state.circlesLineMap[key] = lineLabel
                    self.canvas.window.statusBar().showMessage("{} Drawn from {} to {}".format(lineLabel.text(), 
                                                                self.state.selectedCircle.circleLabel.text(), self.circleLabel.text()))
            self.state.selectedCircle = self
            self.__mousePressPos = None
            self.__mouseMovePos = None
            if event.button() == Qt.LeftButton:
                self.__mousePressPos = event.globalPos()
                self.__mouseMovePos = event.globalPos()
        if event.buttons() == Qt.RightButton:
            self.close()
            self.state.circlesSet.remove(self)
            linesToRemove = list(filter(lambda x: self in x[0], self.state.circlesLineMap.items()))
            for circles_set, lines in linesToRemove:
                lines.close()
                del self.state.circlesLineMap[circles_set]
            del self.state.selectedCircle
            self.state.selectedCircle = None

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.cen = Position(newPos.x()+self.width()/2, newPos.y()+self.height()/2)
            self.__mouseMovePos = globalPos

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         # currPos = self.mapToGlobal(self.pos())
    #         globalPos = event.globalPos()
    #         diff = globalPos - self.__mouseMovePos
    #         diffPos = Position(diff.x(), diff.y())
    #         self.cen = Position(self.cen.x + diffPos.x, self.cen.y + diffPos.y)
    #         self.__mouseMovePos = globalPos
    #         # print(self.circle.center, newPos, globalPos)



class canvas(QWidget):
    def __init__(self, window, state):
        super(canvas, self).__init__(parent=window)
        self.window = window
        self.state = state

    def mousePressEvent(self, event):
        self.window.statusBar().showMessage("Select a Circle")
        self.state.selectedCircle = None

    def paintEvent(self, event):
        painter = QPainter(self)
        for circle_set, line_label in self.state.circlesLineMap.items():
            circle_list = list(circle_set)
            circle1 = circle_list[0]
            circle2 = circle_list[1]
            line_label.move(*midpoint(circle1.center(), circle2.center()))
            painter.drawLine(*circle1.center(), *circle2.center())



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.showMaximized()
        self.state = state()
        self.setWindowTitle("Fossee Screening Task 3")
        self.statusBar().setStyleSheet("""QStatusBar{background-color: white;}""")
        self.toolbar()
        self.canvas = canvas(self, self.state)
        self.canvas.setGeometry(0, 0, 900, 500)
        self.setCentralWidget(self.canvas)
        # self.setStyleSheet("""
        #         QMainWindow {
        #             background-color: white;
        #             }
        #         """)
        # self.scrollarea = QScrollArea()
        # self.scrollarea.setBackgroundRole(QPalette.Dark)
        # self.scrollarea.setWidget(self.canvas)


    def toolbar(self):
        addTool = QAction('Add', self)
        addTool.triggered.connect(self.addCircle)
        addTool.setShortcut("Ctrl+A")
        generateTool = QAction('Generate Report', self)
        generateTool.triggered.connect(self.generatePDF)
        generateTool.setShortcut("Ctrl+G")
        saveTool = QAction('Save', self)
        saveTool.triggered.connect(self.saveImage)
        saveTool.setShortcut("Ctrl+S")
        toolbar = QToolBar("My Toolbar")
        toolbar.addAction(addTool)
        toolbar.addAction(generateTool)
        toolbar.addAction(saveTool)
        self.addToolBar(toolbar)
        
    def addCircle(self):
        self.state.circlesSet.add(Circle(self.canvas, self.state))

    def generatePDF(self):
        saveFile = list(QFileDialog.getSaveFileName(self, 'Save File', '', 'PDF Files (*.pdf)'))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=25, style='BU')
        pdf.cell(0, 10, txt="Report", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        for circles_set, line in self.state.circlesLineMap.items():
            circle1 = circles_set[0].circleLabel.text()
            circle2 = circles_set[1].circleLabel.text()
            pdf.cell(0, 10, txt="[{}: ({}, {})]".format(line.text(), circle1, circle2), ln=1, align="C")
        pdf.output(saveFile[0], 'F')
    
    def saveImage(self):
        saveFile = list(QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG Files (*.png);;JPEG Files (*.jpeg)'))
        image = QPixmap(self.canvas.size())
        self.canvas.render(image)
        image.save(saveFile[0])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.state.selectedCircle != None:
            self.state.selectedCircle.close()
            self.state.circlesSet.remove(self.state.selectedCircle)
            linesToRemove = list(filter(lambda x: self.state.selectedCircle in x[0], self.state.circlesLineMap.items()))
            for circles_set, lines in linesToRemove:
                lines.close()
                del self.state.circlesLineMap[circles_set]
            del self.state.selectedCircle
            self.state.selectedCircle = None


app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
app.exec_()