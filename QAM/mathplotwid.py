from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import matplotlib
import matplotlib as mpl
import numpy as np
from matplotlib import ticker, cm
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import scipy as sp
from matplotlib.pyplot import Figure
import matplotlib.mlab as mlab
import random
from matplotlib import ticker, cm
from matplotlib import colors
from PyQt5.QtWidgets import *
from matplotlib.ticker import PercentFormatter
import math

from multiprocessing import Process, Value, Array

from matplotlib.ticker import MaxNLocator

# -----

class MathPlotWid(QtWidgets.QWidget):


    markes_chan = {0: 'o',
              1: '^',
              2: 'D',
              3: 'X',
              4: 's',
              5: 'P',
              6: '*'
              }

    colors_chan = {
        0: 'b',
        1: 'g',
        2: 'r',
        3: 'c',
        4: 'm',
        5: 'y',
        6: 'b'

    }

    def updateHistColors(self, data):

        self.colors = []

        normalize = matplotlib.colors.Normalize(vmin=np.min(data)
                                                , vmax=np.max(data))

        self.colors = [self.cmap(normalize(val)) for val in data]

    def updateDiagColors(self, x, amp=False):

        self.colors = []



        a, b = np.unique(x, return_counts=True)

        normalize = matplotlib.colors.Normalize(vmin=np.min(b)
                                                , vmax=np.max(b))

        arr = dict(zip(a, b))

        if not amp:
            x = np.unique(x)

        for i in range(len(x)):
            col = arr[x[i]]
            col = normalize(col)
            col = self.cmap(col)
            self.colors.append(col)

        #self.colors = [normalize(arr[y[i]]) )]

        pass

    # ---- гистограмма

    def plotHist(self, data):



        self.clearHistSlot()


        data = [val.DEG for val in data]

        _min = self.hist.get_xlim()[0]
        _max = self.hist.get_xlim()[1]


        x, y = np.unique(data, return_counts=True)

        self.updateHistColors(y)

        self.bar = self.hist.bar(x, y,color=self.colors, width=2)





        tick_num = int(1 * ((_max - _min) / 35))

        if not  tick_num:
            tick_num = 1


        tick = [  round(val / 10) * 10 for val in x[::tick_num]]


        self.hist.set_xlim([_min,_max])


        self.hist.set_ylim([0, self.maxInRange(x, y, _min, _max)])


        self.figure.canvas.draw()

    def maxInRange(self, x, y, _min, _max):

        _val = 1

        for i in range(len(x)):
            if x[i] > _min and x[i] < _max:
                if y[i] > _val:
                    _val = y[i]

        return _val


    def enableGridHist(self, state):
        self.hist.grid(state)

    def setHistLables(self, title=None, xlabel=None, ylabel=None):

        if title:
            self.hist.set_title(title)
        if xlabel:
            self.hist.set_xlabel(xlabel)
        if ylabel:
            self.hist.set_ylabel(ylabel)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def clearHistSlot(self):

        if self.bar:

            self.bar.remove()
            self.bar = None

        self.figure.canvas.draw()

    def initHistSlot(self):


        self.hist = self.figure.subplots(1)
        self.hist.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.bar = None

        self.arr = []

        self.figure.tight_layout()
        self.figure.canvas.draw()



    # ----- колесо сансары

    def rangeColor(self, _min, _max):
        _min = math.radians(_min)
        _max = math.radians(_max)
        self.cmap = matplotlib.cm.get_cmap(self.cmap_type)
        pass


    def rangeHist(self,_min, _max):
        self.hist.set_xlim([_min-1,_max+1])
        self.figure.canvas.draw()


    def rangeDiag(self, _min, _max):

        try:
            self.diag.set_thetamin(_min)
            self.diag.set_thetamax(_max)

            self.figure.canvas.draw()

        except:
            raise

    def plotDiagSlot(self, data, amp_flg=False):

        # очистка старых значений
        """
        if self.scat:
            for _sc in self.scat:
                _sc.remove()
        """
        self.scat = []


        if amp_flg: # если отстраиваем амлитуду
            pass
        else: # ну а если подумать она не так уж нам и нужна

            for _chans in data.getChans():
                x = data.getArr('RAD', _chans, _np=True)
                y = np.full([1, len(x)], 0.55)

                self.scat.append(self.diag.scatter(x, y,marker=self.markes_chan[_chans], c=self.colors_chan[_chans]))

        self.diag.set_ylim(0, 0.6)
        self.figure.canvas.draw()

        """
        if not amp_flg:



            data = [val.DEG for val in data]

            self.updateDiagColors(data)


            data = np.unique(data)

            data = [round(math.radians(val),3) for val in data] # в радианы

            x = np.array(data)
            y = np.full([1, len(data)], 0.55)

            y = y.ravel()

            _min = self.diag.get_xlim()[0]
            _max = self.diag.get_xlim()[1]

            _min = round(_min, 3)
            _max = round(_max, 3)

            self.scat = self.diag.scatter(x, y, c=self.colors, s=25)

            self.diag.set_ylim(0, 0.6)
            self.figure.canvas.draw()

        else:

            x = []
            y = []

            self.updateDiagColors( [val.DEG for val in data], True)

            for i in range(len(data)):
                r =  math.sqrt( (data[i].Q * data[i].Q) +(data[i].I * data[i].I))
                x.append(math.radians(data[i].DEG))
                y.append(r)

            #for i in range()

            self.scat = self.diag.scatter(x, y, c=self.colors, s=25, cmap=self.cmap)



            self.diag.set_rmax(max(y) + 50)
            self.diag.set_rmin(min(y) - 50)

            #self.diag.autoscale(axis='y')
            self.figure.canvas.draw()

            pass

            #self.cbar = self.figure.colorbar(self.scat)
            #plt.colorbar()

    """

    def initDiagSlot(self, amp=False):

        if self.diag:
            self.diag.remove()

        if not amp:

            self.diag = self.figure.add_subplot(111, projection='polar')
            self.diag.invert_xaxis()
            self.diag.get_yaxis().set_visible(False)
            self.diag.set_ylim(0, 0.5)

            self.diag.grid(True)
            self.figure.canvas.draw()

        if amp:
            self.diag = self.figure.add_subplot(111, projection='polar')
            self.diag.invert_xaxis()
            self.figure.subplots_adjust(left=0.058,
                                        right=0.945)
            self.diag.grid(True)
            self.figure.canvas.draw()


    def clearDiagSlot(self):

        if self.scat:
            self.scat.remove()
            self.scat = None

        self.figure.canvas.draw()

    def setDiagLables(self, title=None, xlabel=None, ylabel=None):

        if title:
            self.diag.set_title(title)
        if xlabel:
            self.diag.set_xlabel(xlabel)
        if ylabel:
            self.diag.set_ylabel(ylabel)

    def setCmap(self, val):
        self.cmap_type = val
        self.cmap = matplotlib.cm.get_cmap(self.cmap_type)

    def __init__(self, parent=None):
        super(MathPlotWid, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.time = None

        self.diag = None

        self.bar = None
        self.scat = None
        self.cbar = None

        self.colors = []
        # мучаем колорбар


        self.cmap_type = 'gist_rainbow'
        #

        # --

        self.y_min = 0
        self.y_max = 360

       # self

        self.figure.canvas.draw()



