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

class MPL_Diag(QtWidgets.QWidget):

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

    def setMode(self, _mode):
        self.mode = _mode
        self.clear()

        if self.mode == 1:
            self.diag.get_yaxis().set_visible(False)
            self.diag.set_ylim(self.y_lim[0], self.y_lim[1])

        elif self.mode == 3:
            self.diag.get_yaxis().set_visible(True)

    def __init__(self, parent=None):
        super(MPL_Diag, self).__init__(parent)

        # рутина по элемнтам mpl

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # рутина элементам класса

        self.cmap_type = 'nipy_spectral'  # тип набора цветов
        self.cmap = None

        self.setCmap(self.cmap_type)

        self.colors = []
        self.normalize = None

        self.amp_chan_n = None

        self.diag = None # сама диаграма
        self.diag_plots = None # данные диаграммы
        self.mode = 0 # ампл / без ампл
        self.y_lim = [0, 30] # min max без амплитуды
        self.x_lim = []
        self.mrk_size = 10 # размер точки
        self.delta_flg = False

        # ---
        self.init()
        self.figure.canvas.draw()





    # mode == False --- отображение амплитуды вылючено
    # mode == True  --- отображение амплитуды вкключено


    #первоначальная инициализация
    def init(self):
        self.clear()

        if self.diag: # кыш старые графики
            self.diag.remove()
        self.diag = None

        self.diag = self.figure.add_subplot(111, projection='polar')
        self.diag.invert_xaxis()

        self.figure.subplots_adjust(top=0.918,
                                    bottom=0.076,
                                    left=0.053,
                                    right=0.952,
                                    hspace=0.2,
                                    wspace=0.2)

        self.diag.grid(True)



        self.figure.canvas.draw()

    # очистка
    def clear(self):
        if self.diag_plots:

            for _diag_plots in self.diag_plots:
                _diag_plots.remove()

        self.diag_plots = []

    # установка надписей
    def setLabels(self, title=None, xlabel=None, ylabel=None):
        if title:
            self.diag.set_title(title)
        if xlabel:
            self.diag.set_xlabel(xlabel)
        if ylabel:
            self.diag.set_ylabel(ylabel)

        #self.figure.tight_layout()
        self.figure.canvas.draw()



    def setCmap(self, name):

        self.cmap_type = name
        self.cmap = matplotlib.cm.get_cmap(self.cmap_type)


    def updateColorsDelta(self, arr):

        a, b = np.unique(arr, return_counts=True)

        dic = dict(zip(a, b))

        self.normalize = matplotlib.colors.Normalize(vmin=np.min(b)
                                                     , vmax=np.max(b))

        self.colors = [self.cmap(self.normalize(dic[val])) for val in arr]


    # формируем палитру цветов
    def updateColors(self, data, chan_n):

        a, b =  data.countbyRAD(chan_n)
        arr = dict(zip(a, b))


        self.normalize = matplotlib.colors.Normalize(vmin=np.min(b)
                                                ,vmax=np.max(b))


        x = data.getArr('RAD', chan_n, _np=True)

        self.colors = [ self.cmap(self.normalize(arr[val])) for val in x]

    def setViev(self, lim):

        lim[0] = np.radians(lim[0])
        lim[1] = np.radians(lim[1])

        self.x_lim = lim

        self.diag.set_xlim(self.x_lim)

        self.figure.canvas.draw()


    def plotDiag(self, data):

        self.clear()

        if self.mode   == 1:
            for _chans in data.getChans():  # бежим по списку каналов
                x = data.getArr('RAD', _chans, _np=True)  # получаем  данные

                _y = np.linspace(self.y_lim[0] + 5, self.y_lim[1] - 5,
                                 len(data.getChans()) * 2 - 1)  # распределяем зоны в графике
                _y = _y[::2]
                _y = _y[_chans]
                y = np.full([1, len(x)], _y)

                # --- палитра по каче.... не по количеству
                # _plot = self.diag.scatter(x, y, c=self .colors_chan[_chans],s=self.mrk_size) # отсроили график

                # палитра по количеству
                self.updateColors(data, _chans)
                _plot = self.diag.scatter(x, y, c=self.colors, s=self.mrk_size)  # отсроили график

                self.diag_plots.append(_plot)
                # добавлили график
        elif self.mode == 2:

            sch = -1

            for i in range(len(data.getChans())):
                if i == self.amp_chan_n:
                    continue
                else:
                    sch = sch + 1

                    x = data.getDeltaArr('RAD', self.amp_chan_n, i)

                    _y = np.linspace(self.y_lim[0] + 5, self.y_lim[1] - 5,
                                     len(data.getChans()) * 2 - 1)  # распределяем зоны в графике
                    _y = _y[::2]
                    _y = _y[i]
                    y = np.full([1, len(x)], _y)

                    # палитра по количеству
                    self.updateColorsDelta(x)

                    _plot = self.diag.scatter(x, y, c=self.colors, s=self.mrk_size)
                    self.diag_plots.append(_plot)
        elif self.mode == 3:
                x = data.getArr('RAD', self.amp_chan_n, _np=True)  # получаем  данные
                y = data.getArr('AMP', self.amp_chan_n, _np=True)  # получаем  данные

                self.updateColors(data, self.amp_chan_n)
                _plot = self.diag.scatter(x, y, c=self.colors, s=self.mrk_size)  # отсроили график

                self.diag_plots.append(_plot)

                self.diag.set_ylim(np.min(y) - 100, np.max(y) + 100)


        self.figure.canvas.draw()

        # для работы с ампли туду-туду-туду ой
    def setChan(self, n):
        self.amp_chan_n = n