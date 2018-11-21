from PyQt5 import *
from PyQt5.QtWidgets import *
from mpl_toolkits.mplot3d import *
import matplotlib
import matplotlib as mpl
import numpy as np
from matplotlib import ticker, cm
import time
import math
from pylab import rcParams
import scipy.interpolate
from scipy.signal import savgol_filter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import scipy as sp
from matplotlib.pyplot import Figure
import random
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.colors import BoundaryNorm
import matplotlib.animation as animation
from scipy.interpolate import griddata
import scipy.interpolate as interpolate
from start import MPL_Plot
from start import MPL_3dPlot

#matplotlib.use('Agg')

class Point:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.i = None
        self.j = None

class MathPlotWid(QtWidgets.QWidget):

    n_max = 5
    plots = []
    cbar = None
    con = None
    spec = None

    def setSpecSize(self):
        pass

    def initLabels(self, y_label, x_label, title):
        self.y_label = y_label
        self.x_label = x_label
        self.title = title



    def setPlotLabels(self):
        pass

    def setSpecLabels(self):

        self.spec.set_ylabel(self.y_label)
        self.spec.set_xlabel(self.x_label)
        self.spec.set_title(self.title)
        self.figure.canvas.draw()

        """""""""
        self.spec.set_ylabel('Смещение относительно частоты подстройки')
        self.spec.set_xlabel('Частота подстройки')
        self.spec.set_title('Полоса пропускания')
        self.figure.canvas.draw()
        """""

    def initSpecSlot(self):

        #self.figure.set_size_inches(5,5, forward = False)

        if self.spec:
            self.figure.delaxes(self.spec)

        #TODO чертова фигура не меняет размер !!!!
        #TODO ---- пофикшено
        #TODO НОЭТОНЕТОЧНО

        self.spec = self.figure.subplots(1)
        self.spec.clear()

        self.figure.subplots_adjust(bottom=0.2)

        self.figure.tight_layout()
        self.figure.canvas.draw()





    def plotSpecSlot(self, X, Y, Z):


        try:
            #self.figure.subplots_adjust(right=0.90)

            if self.cbar:
                self.cbar.remove()

                # self.spec.cla()

            #levels = np.linspace(int(np.min(Z)) - 1, int(np.max(Z)) + 1, 10000)

            #self.con = self.spec.contourf(X, Y, Z, levels, cmap=cm.nipy_spectral)

            self.con = self.spec.imshow(Z.transpose(),vmax=Z.max(), vmin=Z.min(),  aspect='auto',cmap=cm.nipy_spectral,
                                        extent=[X[0][0],X[-1][0] ,Y[0][0], Y[0][-1] ])
            #self.spec.ax.set_aspect(2)

            if False:
                self.con = self.spec.imshow(Z.transpose(), vmax=Z.max(), vmin=Z.min(), aspect='auto',
                                            cmap=cm.nipy_spectral
                                            )

            #self.spec.set_ylim([-250,250])

            self.cbar = self.figure.colorbar(self.con)

            self.figure.canvas.draw()

        except:
           raise

    def clearGraph(self, NUM):
        if NUM >= self.n:
            return

        self.plots[NUM].clear()

    def clearSpec(self):

        self.spec.clear()
        self.figure.canvas.draw()

    def smooth(self, y, box_pts):
        box = np.ones(box_pts) / box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth


    def calcPeak(self, X, Y, Z):
        pass

    def isPeak(self, peaks):
        pass

    def mean(self, numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

    def plot3D(self, plot3d, x, y, z):

        _cmap = cm.nipy_spectral
        _cmap.set_bad('white', 1.)

        # тестовая часть
        """"""""" 
        x = []
        y = []
        z = []


      

        for i in range(500, 2500 + 1):
            x.append([])
            y.append([])
            z.append([])

            for j in range(750, 6000 + 1):
                x[len(x)- 1].append(i)
                y[len(x) -1].append(j)
                z[len(x) - 1].append(np.random.randint(80, 85))

        print('Генерация закончена')
        """""

        #self.plot_3d.plot(x, y, z)

        #z[3987] = 50
#        z[5][20] = 73
 #       z[670][600] = 68
        #z[9932] = 48

        # конец тестовой части

        self.peaks = []
        self.peaks.append([])
        self.peaks.append([])
        self.peaks.append([])


        for i in range(len(z)):
            #_mn = self.mean(z[i])
            for j in range(len(z[i])):


                # ручной фильтр гармоник генератора


                """""""""
                t = 200


                if ((y[i][j] * 3) > (x[i][j] - t)) and ((y[i][j] * 3) < (x[i][j] + t)) and (z[i][j] > -70):
                    z[i][j] = - 70

                if ((y[i][j] * 2) > (x[i][j] - t)) and ((y[i][j] * 2) < (x[i][j] + t)) and (z[i][j] > -70):
                    z[i][j] = - 70

                if z[i][j] > -55:
                    print(str(x[i][j]) + ' ' + str(y[i][j]) + ' ' + str(z[i][j]))
                """""

                if z[i][j] > -58:
                   self.peaks[0].append(x[i][j])
                   self.peaks[1].append(y[i][j])
                   self.peaks[2].append(z[i][j])
                  # print('Пик\t' + str(z[i][j]))

        print('Поиск пиков закончен')

        # формирование маски


        _X = np.array([])
        _Y = np.array([])
        _Z = np.array([])

        _pre_y = int(len(y[i]) / plot3d.y_shape)
        _pre_x = int(len(x)    / plot3d.x_shape)

        if not _pre_y:
            _pre_y = 1

        if not _pre_x:
            _pre_x = 1

        for i in range(len(z)):
            if not (i % _pre_x)  or (True in np.in1d(self.peaks[2], np.array(z[i]))):

                mask_x = []
                for j in range(len(z[i])):

                    if not(j % _pre_y) or z[i][j] in self.peaks[2]:
                        pass
                    else:
                        mask_x.append(j)

                    #if (j % _pre) and not (z[i][j] in self.peaks[2]):


                _x = np.array(x[i])
                _x = np.delete(_x, mask_x)

                _y = np.array(y[i])
                _y = np.delete(_y, mask_x)

                _z = np.array(z[i])
                _z = np.delete(_z, mask_x)

                _X = np.append(_X, _x)
                _Y = np.append(_Y, _y)
                _Z = np.append(_Z, _z)



        _X = _X.reshape(-1)
        _Y = _Y.reshape(-1)
        _Z = _Z.reshape(-1)

        print('Установка маски закончена')


        self.surf = self.plot_3d.plot_trisurf(_X, _Y, _Z,cmap=cm.gnuplot)

        print('График построен')

        self.plot_3d.autoscale()
        self.cbar = self.figure.colorbar(self.surf, shrink=0.5, aspect='auto')

        for i in range(len(self.peaks[0])):
            #self.plot_3d.scatter(self.peaks[0][i], self.peaks[1][i], self.peaks[2][i], marker='o', linewidths=1, c='y')
            pass

        print('Пики построены')

        if self.first:
            #self.plot_3d.invert_zaxis()
            self.plot_3d.view_init(30, 160)
            self.first = False
            self.plot_3d.set_title('Побочные каналы приема', pad=10)
            self.plot_3d.set_xlabel('Перестройка Панорамы, MHz', labelpad=10)
            self.plot_3d.set_ylabel('Перестройка Генератора, MHz', labelpad=10)
            self.plot_3d.set_zlabel('Подавление,  dBc', labelpad=10)

        self.figure.canvas.draw()

        return


        # ----------------------------------------------- еще одна попытка -----------------------------------

        # формирование новой сетки
        xi = np.arange(_X.min(), _X.max())
        yi = np.arange(_Y.min(), _Y.max())
        X, Y = np.meshgrid(xi, yi)
        Z = np.nan_to_num(interpolate.griddata((_X, _Y), _Z, (X, Y),fill_value=np.nan))

        print('Сетка закончена')

        #self.surf = self.plot_3d.plot_surface(X, Y, Z,  cmap=cm.jet, vmax=np.nanmax(Z), vmin=np.nanmin(Z))

        print('График построен')



        print('Точки пиков построены')






        self.figure.canvas.draw()

        return

        # ----- прошлая часть -----------------------------------


        peak = plot3d.peak



        sigma_y = plot3d.sigma_y
        sigma_x = plot3d.sigma_x
        sigma = [sigma_y, sigma_x]

        mode = plot3d.mode

        Z = np.ma.array(Z, mask=np.isnan(Z))

        Z = sp.ndimage.filters.gaussian_filter(Z, sigma, mode=mode)

        _size = plot3d.Z.shape

        _cmap = cm.nipy_spectral
        _cmap.set_bad('white', 1.)


        # -----




        peak = 10

        for i in range(_size[1]):
            mn = np.nanmean(plot3d.Z[i])

            for j in range(_size[0]):
                if plot3d.Z[j][i]  < mn - peak:
                    tmp = Point()
                    tmp.x = plot3d.X[0][i]
                    tmp.y = plot3d.Y[j][0]
                    tmp.z = plot3d.Z[j][i]
                    self.peaks.append(tmp)

        # -----


        if self.cbar:
            self.cbar.remove()
            self.cbar = None

        if self.surf:
            self.surf.remove()
            self.surf = None


        _shape = X.shape

        """""""""

        stp0 = int(_shape[0] / plot3d.x_shape)
        stp1 = int(_shape[1] / plot3d.y_shape)

        if stp0:
            X = X[::stp0]
            Y = Y[::stp0]
            Z = Z[::stp0]

        if stp1:
            X = X[::1, ::stp1]
            Y = Y[::1, ::stp1]
            Z = Z[::1, ::stp1]
        
        
        """""

        xi = np.linspace(X.min(), X.max(), plot3d.x_shape)
        yi = np.linspace(Y.min(), Y.max(), plot3d.y_shape)

        X = X[1,:]
        Y = np.transpose(Y[:,1])

        Z = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='cubic')

        X, Y = np.meshgrid(xi, yi)

        #plt.hold(True)

        for pk in self.peaks:
            self.plot_3d.scatter(pk.x, pk.y, pk.z, marker='o', linewidths=5, c='y')

       #self.surf = self.plot_3d.scatter(X, Y, Z)

        _shape = X.shape


        for pk in self.peaks:
            pass





        self.surf = self.plot_3d.plot_surface(X, Y, Z, cmap=_cmap, vmax=np.nanmax(Z), vmin=np.nanmin(Z),
                                              antialiased=False,
                                              rstride=1, cstride=1)

        #plt.hold(False)

        if self.first:
            self.plot_3d.invert_zaxis()
            self.plot_3d.view_init(30, 160)
            self.first = False
            self.plot_3d.set_title('Sample Plot')

        self.plot_3d.autoscale()

        #self.plot_3d.set_zlim3d(np.nanmin(Z) - 10, np.nanmax(Z) + 10)


        self.cbar = self.figure.colorbar(self.surf,shrink=0.5, aspect=5)


        self.figure.canvas.draw()


    def init3Dslot(self):

        for plot in self.plots:
            self.figure.delaxes(plot)

        if self.plot_3d:
            self.figure.delaxes(self.plot_3d)

        self.plot_3d = self.figure.add_subplot(111, projection='3d')
        #self.figure.tight_layout()

    def initGraphSlot(self, count=0):

        for plot in self.plots:
            self.figure.delaxes(plot)
            self.plots = []



        if self.plot_3d:
            self.figure.delaxes(self.plot_3d)
            self.plot_3d = None

        self.plots = []

        if count > self.n_max:
            return

        if count == 0:
            pass
        if count == 1:
            ax = self.figure.subplots(1)
            self.plots.append(ax)
        else:
            self.plots = self.figure.subplots(count)

        #self.figure.tight_layout()
        self.figure.subplots_adjust(top=0.962,
                                    bottom=0.063,
                                    left=0.063,
                                    right=0.985,
                                    hspace=0.76,
                                    wspace=0.2)

        #self.figure.subplots_adjust(wspace=10)

        self.figure.canvas.draw()

    def setTitleSpec(self, title):
        self.figure.canvas.draw()

    def setTitleGraph(self, NUM, title):
        if NUM >= len(self.plots):
            return

        self.plots[NUM].set_title(title)

        self.figure.canvas.draw()

    def enableGridGraph(self, state):

       self.grid = state

    def invertAxis(self, axis):

        if axis == 'y':
            self.invert_y = True


    def plotGraphSlot(self, plot_arr, atOne=False, _title=None):

        if len(self.plots):
            legend = []

            if atOne:  # плотим на одном графике

                self.plots[0].clear()

                if self.grid:

                    x = np.arange(0, 50, 1)
                   # self.plots[0].set_yticks(x)
                    self.plots[0].grid(self.grid)

                    if self.invert_y:
                        self.plots[0].invert_yaxis()


                sch = -1

                self.figure.subplots_adjust(top=0.962,
                                            bottom=0.288,
                                            left=0.063,
                                            right=0.985,
                                            hspace=0.76,
                                            wspace=0.2)

                if plot_arr[0].xlabel:
                    self.plots[0].set_xlabel(plot_arr[0].xlabel)

                if plot_arr[0].ylabel:
                    self.plots[0].set_ylabel(plot_arr[0].ylabel)

                if plot_arr[0].zlabel:
                    self.plots[0].set_zlabel(plot_arr[0].zlabel)

                for plot in plot_arr: # перечисляем графки
                    sch = sch + 1
                    if plot.title:
                        tmp = mpatches.Patch(color=plot.col, label=plot.title)
                        legend.append(tmp)

                    #self.plots[0].clear()


                    if len(plot.x) and len(plot.y):
                        self.plots[0].plot(plot.x, plot.y[0], plot.col)

                self.plots[0].legend(handles=legend, loc=8, borderaxespad=-10., ncol=2)

                if _title:
                    self.plots[0].set_title(_title)

            else:  # каждый в отдельное окно

                sch = -1

                for plot in plot_arr:  # перечисляем графки
                    sch = sch + 1

                    if plot.title:
                        self.plots[sch].set_title(plot.title)

                    if plot.xlabel:
                        self.plots[sch].set_xlabel(plot.xlabel)

                    if plot.ylabel:
                        self.plots[sch].set_ylabel(plot.ylabel)

                    if plot.zlabel:
                        self.plots[sch].set_zlabel(plot.zlabel)

                    for _y in plot.y:
                        if len(_y):
                            self.plots[sch].clear()
                            if plot.col:
                                self.plots[sch].plot(plot.x, _y, plot.col)
                            else:
                                self.plots[sch].plot(plot.x, _y, 'r')

                # ------------------




        self.figure.canvas.draw()

    def plotOverSpec(self, plot_arr):

        #self.spec.clear()
        #self.figure.canvas.draw()

        if self.spec:
            legend = []

            for plot in plot_arr:

                for _y in plot.y:
                    self.spec.plot(plot.x, _y, plot.col)

                if plot.title:
                    tmp = mpatches.Patch(color=plot.col, label=plot.title)
                    legend.append(tmp)

            self.spec.legend(handles=legend, loc=8,borderaxespad=-10.)
            self.setSpecLabels()
            self.figure.canvas.draw()

    def _plotOverSpec(self, x, y, col, title):

        if self.spec:
            self.spec.plot(x, y, col)

            red_patch = mpatches.Patch(color=col, label='The red data')
            self.spec.legend(handles=[red_patch])

            self.figure.canvas.draw()


    def __init__(self, parent=None):
        super( MathPlotWid, self).__init__(parent)

        self.grid = False

        self.peaks = []

        self.plot_3d = None

        self.surf = None
        self.cbar = None

        self.first = True

        self.invert_y = False

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


        self.figure.canvas.draw()










