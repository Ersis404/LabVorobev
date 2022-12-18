import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import pandas as pd

from PandasModel import PandasModel
import numpy as np

FILE_PATH = ""
df = []

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
        self.downloadURL = QtWidgets.QPushButton("DownloadURL", self)
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
        hLayout.addWidget(self.downloadURL)
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
        self.showW.clicked.connect(self.showWeatherSnow)
        self.downloadURL.clicked.connect(self.downloadURLcsv)
        self.pandasTv.setSortingEnabled(True)


    def downloadURLcsv(self):
        url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
        url = url.format(month = 3, year = 2009)
        #custom_date_parser = lambda x: datetime.strptime(x, "%Y-%d-%m %H:%M:%S")
        global df
        df = pd.read_csv(url, parse_dates=['Date/Time (LST)'],  encoding='UTF-8')
        df.columns = [s.replace("°", '') for s in df.columns]
        df.to_csv('weather_mar_2008_now.csv', index = False, header = True, encoding = 'UTF-8')
        self.pathLE.setText('Файл успешно загружен!')



    def loadFile(self):
        self.listFilter.clear()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        global FILE_PATH
        FILE_PATH = fileName
        self.pathLE.setText(fileName)
        global df
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
        #df = pd.read_csv(FILE_PATH)
        filter_str = self.listFilter.currentItem().text()
        df2 = df.loc[:, [filter_str]]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(df['Date/Time (LST)'], df2)
        self.canvas.draw()

    def toCsv100(self):
        self.listFilter.clear()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        global FILE_PATH
        FILE_PATH = fileName
        self.pathLE.setText(fileName)
        global df
        df = pd.read_csv(fileName)
        df = df.drop(['Wind Spd Flag', 'Station Name'], axis = 1)
        df = df.dropna(how = 'all', axis = 1)
        df = df.dropna(how='any', axis=0)

        'Wind Spd Flag'
        cols = df.columns
        for i in range(len(cols)):
            self.listFilter.addItem(cols[i])
        model = PandasModel(df)
        self.pandasTv.setModel(model)
        self.pathLE.setText("Очистка выполнена успешно!")
        print('File info: ', df.info())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())