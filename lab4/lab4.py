from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

import pandas as pd

from PandasModel import PandasModel
import numpy as np

FILE_PATH = ""


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()

        hLayout2 = QtWidgets.QHBoxLayout()

        self.pathLE = QtWidgets.QLineEdit(self)
        vLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        self.setFilter = QtWidgets.QPushButton("Apply filter", self)
        self.plotShow = QtWidgets.QPushButton("Show plot", self)
        self.filterCh = QtWidgets.QPushButton("Filter che", self)
        self.showW = QtWidgets.QPushButton("Show Bar plot", self)
        #self.showL20 = QtWidgets.QPushButton("Show Last 20", self)
        #self.showUnique = QtWidgets.QPushButton("Show Unique Filter", self)
        #self.showM10 = QtWidgets.QPushButton("Show 10 Max Filter", self)
        self.listFilter = QtWidgets.QListWidget(self)
        self.figure = Figure()
        self.figure.set_size_inches(600, 400)
        self.canvas = FigureCanvas(self.figure)

        self.pandasTv = QtWidgets.QTableView(self)
        self.pandasTv.setFixedSize(1895, 400)
        vLayout.addWidget(self.loadBtn)
        hLayout.addWidget(self.filterCh)
        hLayout.addWidget(self.showW)
        hLayout.addWidget(self.setFilter)
        #hLayout.addWidget(self.save100CSV)
        #hLayout.addWidget(self.showM10)
        #hLayout.addWidget(self.showUnique)
        hLayout.addWidget(self.plotShow)
        vLayout.addLayout(hLayout)
        vLayout.addStretch(2)
        hLayout.addWidget(self.listFilter)

        hLayout2.addWidget(self.pandasTv)
        vLayout.addWidget(self.canvas)
        vLayout.addLayout(hLayout2)
        vLayout.addStretch(1)



        self.loadBtn.clicked.connect(self.loadFile)
        self.setFilter.clicked.connect(self.applyFilter)
        self.plotShow.clicked.connect(self.setPlot)
        self.filterCh.clicked.connect(self.toCsv100)
        self.showW.clicked.connect(self.showWeather)
        #self.showF20.clicked.connect(self.show20)
        #self.showM10.clicked.connect(self.showMax10Filter)
        #self.showUnique.clicked.connect(self.showUniqueFilter)
        self.pandasTv.setSortingEnabled(True)


    def showWeather(self):
        self.canvas.draw()
        df = pd.read_csv(FILE_PATH)
        df2 = df["Prov_or_Ter"].value_counts()

        # create an axis
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        df2.plot(kind='bar', legend=False, ax=ax)

        # refresh canvas
        self.canvas.draw()

    def loadFile(self):
        self.listFilter.clear()
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
        print('File info: ', df.info())

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
        ax.plot(df2)

        # refresh canvas
        self.canvas.draw()

    def toCsv100(self):
        self.listFilter.clear()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        global FILE_PATH
        FILE_PATH = fileName
        self.pathLE.setText(fileName)
        df = pd.read_csv(fileName)

        #df.columns = [s.replace("0.0", '') for s in df.columns]
        #df[df["solar flux (Kw/m2)"].str.contains("0.0") == False]
        df = df.dropna(how='all', axis=1)
        cols = df.columns
        for i in range(len(cols)):
            self.listFilter.addItem(cols[i])
        #df2 = df.drop(['rainfall (mm)'], axis=1)
        df3 = df.dropna(how='any', axis=0)
        model = PandasModel(df3)
        self.pandasTv.setModel(model)
        print('File info: ', df.info())
        #for i in range(len(cols)):
            #testcase_name = str(cols[i])
            #item = QtWidgets.QListWidgetItem(testcase_name)
            #item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            #item.setCheckState(QtCore.Qt.Unchecked)
            #self.listFilter.addItem(item)
            #self.listFilter.addItem(cols[i])

    #def filterPlot(self):


    def show20(self):
        df = pd.read_csv(FILE_PATH)
        df2 = df.loc[:20]
        model = PandasModel(df2)
        self.pandasTv.setModel(model)

    def showLast20(self):
        df = pd.read_csv(FILE_PATH)
        df2 = df.tail(20)
        model = PandasModel(df2)
        self.pandasTv.setModel(model)

    def showUniqueFilter(self):
        df = pd.read_csv(FILE_PATH)
        filter_str = self.listFilter.currentItem().text()
        df2 = df[filter_str].unique()
        list = df2.tolist()
        self.listFilter.clear()
        self.listFilter.addItem('Всего уникальных: ' + str(len(list)))
        for row in range(0, len(list)-1):
            self.listFilter.addItem(str(list[row]))


    def showMax10Filter(self):
        df = pd.read_csv(FILE_PATH)
        filter_str = self.listFilter.currentItem().text()
        df2 = df.sort_values([filter_str], ascending = False)[:10][filter_str]
        list = df2.tolist()
        self.listFilter.clear()
        self.listFilter.addItem('Максимальные значения:')
        for row in range(0, len(list)-1):
            self.listFilter.addItem(str(list[row]))

        # create an axis
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        df2.plot(kind='bar', legend=False, ax=ax)
        # refresh canvas
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())