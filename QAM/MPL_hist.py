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
from matplotlib.ticker import MaxNLocator


# -----


class MPL_Hist(QtWidgets.QWidget):
    # временное решение что бы не париться с палитрой цветов, ы
    colors_chan = {
        0: 'b',
        1: 'g',
        2: 'r',
        3: 'c',
        4: 'm',
        5: 'y',
        6: 'b'

    }

    def __init__(self, parent=None):
        super(MPL_Hist, self).__init__(parent)

        # рутина по элемнтам mpl

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # рутина элементам класса

        self.cmap_type = 'nipy_spectral' # тип набора цветов
        self.cmap = None
        self.setCmap(self.cmap_type)
        self.colors = []

        self.amp_chan_n = None

        self.hists = []                  # набор гистограмм
        self.bars_plots = []             # набор данных
        self.mode = False
        self.bar_width =  2

        self.count = 0                   # количество графиков

        self.y_lim = [0, 30]  # min max без амплитуды
        self.x_lim = []

        # ---
        self.figure.canvas.draw()

    # mode == False --- отображение амплитуды вылючено
    # mode == True  --- отображение амплитуды вкключено
    def setMode(self,_mode=False, _count=None):

        if self.mode != _mode: # если перещелкиваемся
            if _mode:
                self.init(_count=1)
            else:
                self.init(_count)

            self.mode = _mode


    def setLabels(self,n_chan, title=None, xlabel=None, ylabel=None):
        if title:
            self.hists[n_chan].set_title(title)
        if xlabel:
            self.hists[n_chan].set_xlabel(xlabel)
        if ylabel:
            self.hists[n_chan].set_ylabel(ylabel)


        self.figure.tight_layout()

    def setAllLabels(self,title=None, xlabel=None, ylabel=None):

        for _hist in self.hists:
            if title:
                _hist.set_title(title)
            if xlabel:
                _hist.set_xlabel(xlabel)
            if ylabel:
                _hist.set_ylabel(ylabel)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def init(self, _count=4):

        self.count = _count

        if len(self.hists): # чистим старье
            for _hist in self.hists:
                _hist.remove()

        self.hists = []

        self.hists = self.figure.subplots(self.count)

        if _count == 1:
            self.hists = [self.hists]

        for _hist in self.hists:
            _hist.yaxis.set_major_locator(MaxNLocator(integer=True))
            _hist.grid(True)


        self.figure.canvas.draw()

    def clear(self):
        if self.bars_plots:
            for _bar_plot in  self.bars_plots:
                _bar_plot.remove()


        self.bars_plots = []

    # ---

    def updateColors(self, data, chan_n):

        a, b = data.countbyRAD(chan_n)


        self.colors = []

        self.normalize = matplotlib.colors.Normalize(vmin=np.min(b)
                                                , vmax=np.max(b))



        self.colors = [self.cmap(self.normalize(val)) for val in b]


    def setCmap(self, name):

        self.cmap_type = name
        self.cmap = matplotlib.cm.get_cmap(self.cmap_type)



    # ---

    def plotHist(self, data, _chan=None):


         self.clear()

         if not self.mode: # работаем со всеми каналами

            for _chan in data.getChans():  # бежим по списку каналов
                x, y = data.countbyDEG(_chan)


                # цветоканалы
                #_plot =  self.hists[_chan].bar(x, y, width=self.bar_width, color=self.colors_chan[_chan])

                #цветоколичества
                self.updateColors(data, _chan)
                _plot = self.hists[_chan].bar(x, y, width=self.bar_width, color=self.colors)


                self.bars_plots.append(_plot)
         else:
            x, y = data.countbyDEG(self.amp_chan_n)

            # цветоканалы
            # _plot =  self.hists[0].bar(x, y, width=self.bar_width, color=self.colors_chan[_chan])

            # цветоколичества
            self.updateColors(data, self.amp_chan_n)
            _plot = self.hists[0].bar(x, y, width=self.bar_width, color=self.colors)

            self.bars_plots.append(_plot)

         self.figure.canvas.draw()


    # для работы с ампли туду-туду-туду ой
    def setChan(self, n):
        self.amp_chan_n = n

    def setViev(self, lim):

        self.x_lim = lim


        for _hist in self.hists:
            _hist.set_xlim(lim)

        self.figure.canvas.draw()