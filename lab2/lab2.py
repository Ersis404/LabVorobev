from random import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

import pandas as pd

from PandasModel import PandasModel

FILE_PATH = ""


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        self.setFilter = QtWidgets.QPushButton("Apply filter", self)
        self.plotShow = QtWidgets.QPushButton("Show plot", self)
        self.listFilter = QtWidgets.QListWidget(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        hLayout.addWidget(self.loadBtn)
        hLayout.addWidget(self.setFilter)
        hLayout.addWidget(self.plotShow)
        hLayout.addWidget(self.listFilter)

        vLayout.addLayout(hLayout)
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        hLayout.addWidget(self.canvas)
        self.loadBtn.clicked.connect(self.loadFile)
        self.setFilter.clicked.connect(self.applyFilter)
        self.plotShow.clicked.connect(self.setPlot)
        self.pandasTv.setSortingEnabled(True)


    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        global FILE_PATH
        FILE_PATH = fileName
        self.pathLE.setText(fileName)
        df = pd.read_csv(fileName)
        cols = df.columns
        for i in range(len(cols)):
            self.listFilter.addItem(cols[i])
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def applyFilter(self):
        df = pd.read_csv(FILE_PATH)
        filter_str = self.listFilter.currentItem().text()
        df2 = df.loc[:, [filter_str]]
        model = PandasModel(df2)
        self.pandasTv.setModel(model)

    def setPlot(self):

        self.canvas.draw()
        df = pd.read_csv(FILE_PATH)
        filter_str = self.listFilter.currentItem().text()
        df2 = df.loc[:, [filter_str]]

        # create an axis
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()


        # plot data
        ax.plot(df2, '*-')

        # refresh canvas
        self.canvas.draw()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())