from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QToolBar, QFileDialog, QStatusBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from fpdf import FPDF
import sys

from State import State
from CircleWidget import CircleWidget
from Canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(900, 500)
        self.state = State()
        self.setWindowTitle("Fossee Screening Task 3")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.status = QLabel("", self)
        self.help = QLabel("Select: L_Click     Delete: Space, R_Click     Rename: Double Click", self)
        self.help.setAlignment(Qt.AlignRight)
        self.statusBar.addWidget(self.status)
        self.statusBar.addWidget(self.help, 1)
        self.statusBar.setStyleSheet("""QStatusBar{background-color: white;color: Black;}""")
        self.toolbar()
        self.canvas = Canvas(self, self.state)
        self.setCentralWidget(self.canvas)
        self.showMaximized()

    def toolbar(self):
        addTool = QAction('Add (Ctrl + A)', self)
        addTool.triggered.connect(self.addCircle)
        addTool.setShortcut("Ctrl+A")
        generateTool = QAction('Generate Report (Ctrl + G)', self)
        generateTool.triggered.connect(self.generatePDF)
        generateTool.setShortcut("Ctrl+G")
        saveTool = QAction('Save (Ctrl + S)', self)
        saveTool.triggered.connect(self.saveImage)
        saveTool.setShortcut("Ctrl+S")
        toolbar = QToolBar("My Toolbar")
        toolbar.addAction(addTool)
        toolbar.addAction(generateTool)
        toolbar.addAction(saveTool)
        self.addToolBar(toolbar)

    def addCircle(self):
        self.state.circlesSet.add(CircleWidget(self.canvas, self.state).circle)

    def generatePDF(self):
        saveFile, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PDF Files (*.pdf)')
        if len(saveFile.strip()) == 0:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=25, style='BU')
        pdf.cell(0, 10, txt="Report", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        for circles_set, line in self.state.circlesLineMap.items():
            circle1 = circles_set[0].label.text()
            circle2 = circles_set[1].label.text()
            pdf.cell(0, 10, txt="[{}: ({}, {})]".format(line.text(), circle1, circle2), ln=1, align="C")
        pdf.output(saveFile, 'F')

    def saveImage(self):
        saveFile, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG Files (*.png);;JPEG Files (*.jpeg)')
        if len(saveFile.strip()) == 0:
            return
        image = QPixmap(self.canvas.size())
        self.canvas.render(image)
        image.save(saveFile)


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()
