#! /usr/bin/env python
# -*- coding: utf-8 -*-



def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))


    print('\n\n-------------------------------------------- \n')
    print(text)
    print('\n----------------------------------------------\n')

#входной с фигнейspecCalcMaxOffset

import sys
sys.excepthook = log_uncaught_exceptions

# TODO в отдельный файл

class MPL_3dPlot:
    def __init__(self):
        self.ready = False

        self.X = None
        self.Y = None
        self.Z = None

        self.sigma_x = None
        self.sigma_y = None
        self.sigma_y = None
        self.mode = None

        self.peak = None

        self.x_shape = None
        self.y_shape = None

class MPL_Plot:
    def __init__(self):
        self.x = []
        self.y = []
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        self.enabled = False

        self.col = ''

from structs import pn_params
import sys
#from mathplotwid import MPL_Plot
import shutil
#выходной тракт --- короткий черный
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from MainWindowUi import Ui_MainWindow
import pyqtgraph as pg
import sys
from Analyzer import Analyzer
from Generator import Generator
import visa
from helpGenerator import helpGenerator
from CAL_test import CAL_Test
from AFC_test import AFC_Test
from GAIN_test import GAIN_Test
from PIO import PIO_Test
from POC_test import POC_test
from PB_5 import PB
from ACC_test import ACC_Test
from EFF_test import EFF_Test
from IMD_test import IMD_Test
from BF_test import BF_Test
from UD_Test import UD_Test
from BW_test import BW_Test
from MIRR_test import MIRR_Test
from PN_test import PN_Test
from  NF_test import NF_Test
from SIF_test import SIF_Test
from ATT_test import ATT_Test
import math
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtWidgets import *
import xml.etree.ElementTree as et
from Panorama import Panorama
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import tostring
from GET_test import GET_Test
#100 dn
import time
import os
import errno
import datetime
import re
import pyqtgraph.exporters
#from PyQt5.QtGui import QScreen
import subprocess
from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors



# -*- coding: utf-8 -*-


class MW(QtGui.QMainWindow, Ui_MainWindow):

    flg = False
    sch = 0

    gen_ip = 'TCPIP0::192.168.1.3::inst0::INSTR'
    an_ip = 'TCPIP0::192.168.1.2::inst0::INSTR'

    h_gen_ip = 'TCPIP0::192.168.1.2::inst0::INSTR'

    pb5_ip = 'TCPIP0::192.168.1.101::inst0::INSTR'
    pb48_ip = 'USB0::0x0957::0x0807::N5767A-US10M4980H::INSTR'

    dir_name = 'test_log'

    cal_in = None
    cal_out = None

    pan = Panorama()

    # ----- Работа с Панарамкой




    def graphReadClicked(self):




        x = []
        y = []

        par_val = []
        par_val.append(' ')
        par_val.append(' ')
        sch = -1
        _type = ''


        sch_graphs = -1

        g = []

        for i in range(10):
            g.append(MPL_Plot())
            g[i].y.append([])


        try:
            file = open(self.grapPath.text(), 'r')

            for line in file:
                line = line.replace('\n', '')
                line = line.replace('\t', ' ')
                if line == '':
                    continue


                par_val = line.split(':')

                if par_val[0].find('type') != -1:
                    _type = par_val[1].replace(' ', '')

                if len(par_val) == 1 and sch:
                    if len(line.split(' ')) == 1:
                        sch = -5
                    elif len(line.split(' ')) == 3:
                        pass
                    else:

                        sch = -3


                if sch == -1: # идет парсинг параметров
                    self.logTextEditSlot(str(par_val[0])  + str(par_val[1]))
                elif sch == -3:
                    self.logTextEditSlot(line)
                else:
                    if _type == 'plotOverSpec':
                      if line.find('BIAS_CENT') != -1:
                          sch = 0
                          g[sch].title = 'Смещение центра полосы пропускания'
                          g[sch].col = 'g'
                          g[sch].y.append([])
                          continue
                      if line.find('BW_3') != -1:
                          sch  = 1
                          g[sch].title = 'Полоса пропускания по уровню -3 dB'
                          g[sch].col = 'y'
                          g[sch].y.append([])
                          g[sch].y.append([])
                          continue
                      if line.find('BW_6') != -1:
                          sch = 2
                          g[sch].title = 'Полоса пропускания по уровню -6 dB'
                          g[sch].col = 'b'
                          g[sch].y.append([])
                          g[sch].y.append([])
                          continue

                      if sch == 0:
                            line = line.replace('Freq:', '')
                            line = line.replace('Bias:', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y = tmp
                            g[sch].x.append(float(_x))
                            g[sch].y[0].append(float(_y))
                      if sch == 1:
                            line = line.replace('Freq:', '')
                            line = line.replace('Bw_3_freq_vals:', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y0, _y1 = tmp
                            g[sch].x.append(float(_x))
                            g[sch].y[0].append(float(_y0))
                            g[sch].y[1].append(float(_y1))
                      if sch == 2:
                            line = line.replace('Freq:', '')
                            line = line.replace('Bw_3_freq_vals:', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y0, _y1 = tmp
                            g[sch].x.append(float(_x))
                            g[sch].y[0].append(float(_y0))
                            g[sch].y[1].append(float(_y1))
                    if _type == 'AFC':
                        if line.find('AFC') != -1:
                            sch = 0
                            continue
                        if sch == 0:
                            line = line.replace('Freq:', '')
                            line = line.replace('Amp:', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y = tmp

                            x.append(float(_x))
                            y.append(float(_y))
                    if _type == 'GAIN':
                        if line.find('GAIN') != -1:
                            sch = 0
                            continue
                        if sch == 0:
                            line = line.replace('Freq:', '')
                            line = line.replace('Gain:', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y = tmp

                            x.append(float(_x))
                            y.append(float(_y))
                    if _type == 'ACC':
                        if line.find('ACC') != -1:
                            sch = 0
                            continue
                        if sch == 0:
                            line = line.replace('Freq:', '')
                            line = line.replace('Delta:', '')
                            line = line.replace('ppb', '')
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']
                            _x, _y = tmp

                            x.append(float(_x))
                            y.append(float(_y))
                    if _type == 'GET':
                        if line.find('GET') != -1:
                            sch = 0
                            self.MPL_additGraphicsView.initGraphSlot(2)

                            g[0].title = 'Гетеродин #1'
                            g[0].col = 'b'
                            g[0].y.append([])

                            g[1].title = 'Гетеродин #2'
                            g[1].col = 'r'
                            g[1].y.append([])

                            continue

                        if sch == 0:
                            tmp = [s for s in line.split(' ') if s != ' ' and s != '']

                            if len(tmp) == 3:
                                _x, _y0, _y1 = tmp
                            elif len(tmp) == 2:
                                _x, _y0 = tmp
                                y1 = np.nan
                            else:
                                continue

                            if _y0 != 'N/A':
                                g[0].y[0].append(float(_y0))
                                g[0].x.append(float(_x))
                            if _y1 != 'N/A':
                                g[1].y[0].append(float(_y1))
                                g[1].x.append(float(_x))

                    if _type == 'PN':
                        if line.find('PN') != -1:
                            sch = 0
                            self.MPL_additGraphicsView.initGraphSlot(1)
                            continue

                        if sch == 0: # читаем значения

                            tmp = [float(s) for s in line.split(' ') if s != ' ' and s != '']

                            _x = tmp[0]
                            del tmp[0]

                            __sch = -1
                            for _y in tmp:
                                __sch = __sch + 1
                                g[__sch].x.append(_x)
                                g[__sch].y[0].append(_y)
                                g[__sch].enabled = True

                    if _type == 'NF':
                        if line.find('NF') != -1:
                            sch = 0
                            self.MPL_additGraphicsView.initGraphSlot(1)
                            continue

                        if sch == 0:  # читаем значения

                            tmp = [float(s) for s in line.split(' ') if s != ' ' and s != '']

                            if len(tmp) == 2:
                                g[0].x.append(tmp[0])
                                g[0].y[0].append(tmp[1])
                                g[0].enabled = True




            if _type == 'plotOverSpec':
                self.MPL_graphicsView.initLabels('Смещение относительно частоты подстройки',
                                                 'Частота подстройки',
                                                 'Полоса пропускания')
                self.MPL_graphicsView.plotOverSpec([g[0], g[1], g[2]])
            if _type == 'AFC':
                self.mainGraphicsView.plotItem.setLabels(title='АЧХ', left='Амлитуда, dBm', bottom='Частота, MHz')
                self.plot_graph(x, y, 'red', True)

            if _type == 'GAIN':
                self.mainGraphicsView.plotItem.setLabels(title='Усиление', left='Усиление, dB', bottom='Частота, MHz')
                self.plot_graph(x, y, 'red', True)

            if _type == 'ACC':
                self.mainGraphicsView.plotItem.setLabels(title='Точность подстройки', left='Тоочность подстройки, ppb', bottom='Частота, MHz')
                self.plot_graph(x, y, 'red', True)

            if _type == 'GET':
                self.MPL_additGraphicsView.plotGraphSlot(g, False, 'Мощность сигнала гетеродина')

            if _type == 'NF':

                g[0].xlabel = 'Частота перестройки, MHz'
                g[0].ylabel = 'NF'
                g[0].zlabel = None
                g[0].col = 'r'

                self.MPL_additGraphicsView.plotGraphSlot(g, True, 'Коэф. шума')

            if _type == 'PN':
                col = ['r', 'g', 'b', 'y', 'c', 'k']
                names = ['Фазовый шум по маркеру 10 MHz',
                         'Фазовый шум по маркеру 1 MHz',
                         'Фазовый шум по маркеру 100 kHz',
                         'Фазовый шум по маркеру 10 kHz',
                         'Фазовый шум по маркеру 1 kHz',
                         'Фазовый шум по маркеру 100 Hz']

                for i in range(len(g)):
                    if g[i].enabled:
                        g[i].col = col[i]
                        g[i].title = names[i]

                g[0].xlabel = 'Частота перестройки, MHz'
                g[0].ylabel = 'Фазовый шум, dBc/Hz'
                g[0].zlabel = None

                self.MPL_additGraphicsView.plotGraphSlot(g, True, 'Фазовые шумы')

        except:
           raise
        finally:
            file.close()

    def ATT_gainPushButtonClicked(self):
        self.ATT_gainLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def NF_gainPushButtonClicked(self):
        self.NF_gainLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def graphSelectClicked(self):
        self.grapPath.setText(QFileDialog.getOpenFileName()[0])

    def TST_PIO_selectInFilePushButtonClicked(self):
        self.TST_PIO_getInFileLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def savePlotPushButtonClicked(self, name=None,path=None): #

        if not path:
            path = QFileDialog.getExistingDirectory()
        if not name:
            name = ''

    def CAL_selectFilePushButtonClicked(self):
        self.CAL_getFileLineEdit.setText(QFileDialog.getExistingDirectory())

    def clearTestFileClicked(self):
        f = open(self.fileDirLineEdit.text() + '\\' + self.saveFileLineEdit.text() + '.xml', 'w')
        f.close()
        self.logTextEditSlot('Файл успешно очищен')

    def POC_selectInFilePushButtonClicked(self):
        self.POC_getInFileLineEdit.setText(QFileDialog.getOpenFileName())

    def __del__(self):
        pass

    def dirResClicked(self):
        self.resFileDirLineEdit.setText(QFileDialog.getExistingDirectory())

    def fileDirPushButtonClicked(self):
        self.fileDirLineEdit.setText(QFileDialog.getExistingDirectory())

    def searchDevButtonClicked(self):

        self.checkAutoPushButton.setDisabled(False)

        self.logTextEditSlot('Список оборудования:')
        self.searchDev()

        if self.an.fullName and self.gen.fullName and self.pb48.fullName and self.pb5.fullName:
            self.startAutoPushButton.setDisabled(False)
            self.logTextEditSlot('Успешно, готово к запуску!')

    def setProgOnWork(self, state):
        if not state and self.flg:
            self.startAutoPushButtonClicked()

    def startAutoPushButtonClicked(self):


        file = self.resFileDirLineEdit.text() +  self.resFileLineEdit.text() + '.txt'

        f = None

        if not self.flg:
            f = open(file, 'w')
            f.write('ID устройства: ' + self.IDlineEdit.text())
            f.write('\n')
            f.write('Тип устройства: ' + self.devTypeComboBox.currentText())
            f.write('\n')
            f.write('Время создания файла: ' + time.ctime(time.time()))
            f.write('\n\n')
           # f.write('Выполненные тесты\tФайл теста\n')

            try:
                os.makedirs(self.resFileDirLineEdit.text() + '\\' + self.dir_name)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        else:
            f = open(file, 'a')


        if not self.flg:
            self.flg = True
            self.sch = 0

        t_f = self.destFileLineEdit.text()

        try:
            tree = et.parse(t_f)

            rt = tree.getroot()

            tmp = self.sch

            for root in rt:

                tag = root.tag

                if tmp:
                    tmp = tmp - 1
                    continue

                calFlg = self.CAL_calibEnableCheckBox.isChecked()

                if calFlg and not self.cal_in:
                    self.showErr('Отсутствует файл калибровки!')
                    self.flg = False

                self.an = Analyzer()
                an = root.find('an').text
                self.an.ip = an
                self.an.connect()

                gen = root.find('gen').text
                typ = root.find('gen').attrib['type']

                if typ == 'SMA100A':
                    self.gen = Generator()
                self.gen.ip = gen
                self.gen.connect()

                if tag == 'FR':
                    self.last_test = 'AFC'

                    self.logTextEditSlot('Test type:\t' + tag)

                    level = root.find('level').text
                    level = float(level)
                    self.logTextEditSlot('Level:\t' + str(level))

                    step = root.find('step').text
                    step = float(step)
                    self.logTextEditSlot('Step:\t' + str(step))

                    beg = root.find('beg').text
                    beg = float(beg)
                    self.logTextEditSlot('Beg:\t' + str(beg))

                    end = root.find('end').text
                    end = float(end)
                    self.logTextEditSlot('End:\t' + str(end))

                    calFlg = self.CAL_calibEnableCheckBox.isChecked()

                   # if self.calflg and not self.cal_in:
                  #      self.showErr('Не указаный файлы калибровки!')

                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text()  + self.dir_name + '\\' + 'FR_' + name + '.txt'

                    self.afc.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                                       self.colorComboBox.currentText(),
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                                       plot_flg=self.realPlotCheckBox.isChecked(),
                                       logfile=name)

                    self.logProgressBar.setMaximum(end)
                    self.logProgressBar.setMinimum(beg)

                    self.afc.start()

                    #f.write('AFC\t' + name + '\n')

                    self.sch = self.sch + 1
                    return

                if tag == 'Gain':
                    self.logTextEditSlot('Test type:\t' + tag)

                    level = root.find('level').text
                    level = float(level)
                    self.logTextEditSlot('Level:\t' + str(level))

                    step = root.find('step').text
                    step = float(step)
                    self.logTextEditSlot('Step:\t' + str(step))

                    beg = root.find('beg').text
                    beg = float(beg)
                    self.logTextEditSlot('Beg :\t' + str(beg))

                    end = root.find('end').text
                    end = float(end)
                    self.logTextEditSlot('End:\t' + str(end))

                    file_flg = root.find('file_flg').text
                    file_flg = int(file_flg)
                    self.logTextEditSlot('Generate gain file:\t' + str(file_flg))

                    file_dir = root.find('file_dir').text
                    self.logTextEditSlot('Gain file dir\t' + file_dir)

                    calFlg = self.CAL_calibEnableCheckBox.isChecked()

                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text() + self.dir_name + '\\' + 'Gain_' + name + '.txt'

                    user = [file_flg, file_dir]

                    self.gain.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                                       self.colorComboBox.currentText(),
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                                       plot_flg=self.realPlotCheckBox.isChecked(),
                                       logfile=name,
                                       user= user)

                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text() + self.dir_name + '\\' + 'Gain_' + name + '.txt'

                    self.gain.start()

                    self.sch = self.sch + 1
                    return

                if tag == 'P1dB':
                    self.logTextEditSlot('Test type:\t' + tag)

                    file = root.find('gain_f').text
                    self.logTextEditSlot('Gain file:\t' + file)

                    beg_l = root.find('beg_l').text
                    beg_l = float(beg_l)
                    self.logTextEditSlot('Begin level:\t' + str(beg_l))

                    end_l = root.find('end_l').text
                    end_l = float(end_l)
                    self.logTextEditSlot('End level:\t' + str(end_l))

                    step_l = root.find('step_l').text
                    step_l = float(step_l)
                    self.logTextEditSlot('Step level:\t' + str(step_l))

                    beg_f = root.find('beg_f').text
                    beg_f = float(beg_f)
                    self.logTextEditSlot('Begin freq:\t' + str(beg_f))

                    end_f = root.find('end_f').text
                    end_f = float(end_f)
                    self.logTextEditSlot('End freq:\t' + str(end_f))

                    step_f = root.find('step_f').text
                    step_f = float(step_f)
                    self.logTextEditSlot('Step freq:\t' + str(step_f))

                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text() + self.dir_name + '\\' + 'P1dB_'  + name + '.txt'

                    self.logProgressBar.setMaximum(end_f)
                    self.logProgressBar.setMinimum(beg_f)

                    self.poc.setParams(beg_f, end_f, step_f, None, None, self.gen, self.an, self.dev,
                                       self.colorComboBox.currentText(),
                                       plot_flg=self.realPlotCheckBox.isChecked(),
                                       logfile=name,
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                                       user=[beg_l, end_l, step_l, file])


                    self.poc.start()

                    self.sch = self.sch + 1
                    return

                if tag == 'P1dB_freq':
                    self.logTextEditSlot('Test type:\t' + tag)

                    freq = root.find('freq').text
                    freq = float(freq)
                    self.logTextEditSlot('Freq:\t' + str(freq))

                    step = root.find('step').text
                    step = float(step)
                    self.logTextEditSlot('Step:\t' + str(step))

                    beg = root.find('beg').text
                    beg = float(beg)
                    self.logTextEditSlot('Beg :\t' + str(beg))

                    end = root.find('end').text
                    end = float(end)
                    self.logTextEditSlot('End:\t' + str(end))

                    fl = root.find('file').text
                    self.logTextEditSlot('File:\t' + fl)


                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text() + self.dir_name + '\\' + 'P1dB_' + str(freq) + 'MHz' + name + '.txt'

                    self.pio.setParams(beg, end, step, freq, None, self.gen, self.an, None,
                                       self.colorComboBox.currentText(),
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                                       plot_flg=self.realPlotCheckBox.isChecked(),
                                       logfile=name,
                                       user=[self.TST_PIO_getInFileLineEdit.text(), False])

                    self.logProgressBar.setMaximum(end)
                    self.logProgressBar.setMinimum(beg)

                    self.pio.start()

                    self.sch = self.sch + 1
                    return

                if tag == 'EFF':
                    self.logTextEditSlot('Test type:\t' + tag)

                    freq = root.find('freq').text
                    freq = float(freq)
                    self.logTextEditSlot('Freq:\t' + str(freq))

                    step = root.find('step').text
                    step = float(step)
                    self.logTextEditSlot('Step:\t' + str(step))

                    beg = root.find('beg').text
                    beg = float(beg)
                    self.logTextEditSlot('Beg :\t' + str(beg))

                    end = root.find('end').text
                    end = float(end)
                    self.logTextEditSlot('End:\t' + str(end))

                    self.pb5 = PB()
                    pb = root.find('pb5').text
                    self.pb5.ip = pb
                    self.pb5.connect()

                    self.pb48 = PB()
                    pb = root.find('pb48').text
                    self.pb48.ip = pb
                    self.pb48.connect()

                    name = time.ctime(time.time())
                    name = name.replace(' ', '-')
                    name = name.replace(':', '-')

                    name = self.resFileDirLineEdit.text() + self.dir_name + '\\' + 'EFF_' + name + '.txt'

                    self.logProgressBar.setMaximum(end)
                    self.logProgressBar.setMinimum(beg)

                    self.eff.setParams(beg, end, step, freq, None, self.gen, self.an, None,
                                       self.colorComboBox.currentText(),
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                                       pb=self.pb48,
                                       logfile=name,
                                       plot_flg=self.realPlotCheckBox.isChecked())

                    self.eff.start()

                    self.sch = self.sch + 1
                    return

                if tag == 'IMD':
                    self.logTextEditSlot('Test type:\t' + tag)

                    level = root.find('level').text
                    level = float(level)
                    self.logTextEditSlot('Level:\t' + str(level))

                    step = root.find('step').text
                    step = float(step)
                    self.logTextEditSlot('Step:\t' + str(step))

                    beg = root.find('beg').text
                    beg = float(beg)
                    self.logTextEditSlot('Beg :\t' + str(beg))

                    end = root.find('end').text
                    end = float(end)
                    self.logTextEditSlot('End:\t' + str(end))

                    sep = root.find('sep').text
                    sep = float(sep)
                    self.logTextEditSlot('Sep:\t' + str(sep))

                    self.logProgressBar.setMaximum(end)
                    self.logProgressBar.setMinimum(beg)

                    self.imd.setParams(beg, end, step, None, level,
                                       self.gen, self.an, self.dev,
                                       self.colorComboBox.currentText(),
                                       cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out, user=sep)

                    if self.gen.type != 'N5182A':
                        self.showErr('Данный генератор не поддерживает двухтоновый сигнал!')
                    else:
                        self.imd.start()



                    self.sch = self.sch + 1
                    return

            self.flg = False

        except:
            self.logTextEditSlot('Неверный файл авто теста...')
        finally:
            f.close()

        self.logTextEditSlot('Автоматический режим завершен!')

    def searchDev(self):
            lst = self.rm.list_resources()


            for i in range(len(lst)):
                try:
                    dev = self.rm.open_resource(lst[i], open_timeout=100)
                    name = dev.query('*IDN?')
                except:
                    continue

                if name.find('N5182') != -1:
                    self.gen = helpGenerator()
                    self.gen.ip = lst[i]
                    self.gen.connect()
                    self.EQU_GEN_statusLabel.setText(self.gen.fullName)
                    self.EQU_GEN_resetPushButton.setDisabled(False)
                    self.logTextEditSlot('Generator: ' + self.gen.fullName)
                elif name.find('FSL-6') != -1:
                    self.an = Analyzer()
                    self.an.ip = lst[i]
                    self.an.connect()
                    self.logTextEditSlot('Analyzer: ' + self.an.fullName)
                    self.EQU_anStatusLabel.setText(self.an.fullName)
                elif name.find('6702') != -1:
                    self.pb5 = PB()
                    self.pb5.ip = lst[i]
                    self.pb5.connect()
                    self.logTextEditSlot('Power Block 5V:\t' + self.pb5.fullName)
                    self.EQU_pb5StatusLabel.setText(self.pb5.fullName)
                elif name.find('5767') != -1:
                    self.pb48 = PB()
                    self.pb48.ip = lst[i]
                    self.pb48.connect()
                    self.logTextEditSlot('Power Block 48V: ' + self.pb48.fullName)
                    self.EQU_pb48StatusLabel.setText(self.pb48.fullName)
                    #self.EQU_AN_statusLabel.setText(self.an.fullName)
                    #self.EQU_AN_resetPushButton.setDisabled(False)
                if name.find('SMA100A') != -1:
                    self.gen = Generator()
                    self.gen.ip = lst[i]
                    self.gen.connect()
                    self.EQU_GEN_statusLabel.setText(self.gen.fullName)
                    self.EQU_GEN_resetPushButton.setDisabled(False)
                    self.logTextEditSlot('Generator: ' + self.gen.fullName)

    def checkAutoPushButtonClicked(self):


        try:
            file = open(self.lineEdit.text())
        except:
            self.logTextEditSlot('Неверный путь к файлу теста!')
            return

        self.logTextEditSlot('Считывание файлов калибровки...')
        self.CAL_getFilePushButtonClicked()

        try:

            tree = et.parse(file)
            root = tree.getroot()
            tag = root.tag

            if tag == 'AFC':

                self.last_test = 'AFC'

                self.logTextEditSlot('Test type:\t' + tag)

                level = root.find('level').text
                level = float(level)
                self.logTextEditSlot('Level:\t' + str(level))

                step = root.find('step').text
                step = float(step)
                self.logTextEditSlot('Step:\t' + str(step))

                beg = root.find('beg').text
                beg = float(beg)
                self.logTextEditSlot('Beg :\t' + str(beg))

                end = root.find('end').text
                end = float(end)
                self.logTextEditSlot('End:\t' + str(end))

                calFlg = self.CAL_calibEnableCheckBox.isChecked()

                self.afc.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                                   self.colorComboBox.currentText(),
                                   cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out)

                self.logProgressBar.setMaximum(end)
                self.logProgressBar.setMinimum(beg)

            if tag == 'Gain':
                self.logTextEditSlot('Test type:\t' + tag)

                level = root.find('level').text
                level = float(level)
                self.logTextEditSlot('Level:\t' + str(level))

                step = root.find('step').text
                step = float(step)
                self.logTextEditSlot('Step:\t' + str(step))

                beg = root.find('beg').text
                beg = float(beg)
                self.logTextEditSlot('Beg :\t' + str(beg))

                end = root.find('end').text
                end = float(end)
                self.logTextEditSlot('End:\t' + str(end))

            if tag == 'POC':
                self.logTextEditSlot('Test type:\t' + tag)

                beg_l = root.find('beg_l').text
                beg_l = float(beg_l)
                self.logTextEditSlot('Begin level:\t' + str(beg_l))

                end_l = root.find('end_l').text
                end_l = float(end_l)
                self.logTextEditSlot('End level:\t' + str(end_l))

                step_l = root.find('step_l').text
                step_l = float(step_l)
                self.logTextEditSlot('Step level:\t' + str(step_l))

                beg_f = root.find('beg_f').text
                beg_f = float(beg_f)
                self.logTextEditSlot('Begin freq:\t' + str(beg_f))

                end_f = root.find('end_f').text
                end_f = float(end_f)
                self.logTextEditSlot('End freq:\t' + str(end_f))

                step_f = root.find('step_f').text
                step_f = float(step_f)
                self.logTextEditSlot('Step freq:\t' + str(step_f))

            if tag == 'PIO':
                self.logTextEditSlot('Test type:\t' + tag)

                freq = root.find('freq').text
                freq = float(freq)
                self.logTextEditSlot('Freq:\t' + str(freq))

                step = root.find('step').text
                step = float(step)
                self.logTextEditSlot('Step:\t' + str(step))

                beg = root.find('beg').text
                beg = float(beg)
                self.logTextEditSlot('Beg :\t' + str(beg))

                end = root.find('end').text
                end = float(end)
                self.logTextEditSlot('End:\t' + str(end))

                fl = root.find('file').text
                self.logTextEditSlot('File:\t' + fl)

            if tag == 'EFF':
                self.logTextEditSlot('Test type:\t' + tag)

                freq = root.find('freq').text
                freq = float(freq)
                self.logTextEditSlot('Freq:\t' + str(freq))

                step = root.find('step').text
                step = float(step)
                self.logTextEditSlot('Step:\t' + str(step))

                beg = root.find('beg').text
                beg = float(beg)
                self.logTextEditSlot('Beg :\t' + str(beg))

                end = root.find('end').text
                end = float(end)
                self.logTextEditSlot('End:\t' + str(end))

            if tag == 'IMD':
                self.logTextEditSlot('Test type:\t' + tag)

                level = root.find('level').text
                level = float(level)
                self.logTextEditSlot('Level:\t' + str(level))

                step = root.find('step').text
                step = float(step)
                self.logTextEditSlot('Step:\t' + str(step))

                beg = root.find('beg').text
                beg = float(beg)
                self.logTextEditSlot('Beg :\t' + str(beg))

                end = root.find('end').text
                end = float(end)
                self.logTextEditSlot('End:\t' + str(end))

                sep = root.find('sep').text
                sep = float(sep)
                self.logTextEditSlot('Sep:\t' + str(sep))

        except:
            self.startAutoPushButton.setDisabled(True)
            self.logTextEditSlot('Что то пошло не так...')

        file.close()

    def fileAutoPushButtonClicked(self):
        self.destFileLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def showErr(self, text):
        QMessageBox.critical(self, 'Ошибка!', text)


    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def saveParamsPushButtonClicked(self): # сохранение параметров теста

        fn = self.saveFileLineEdit.text()
        ind = self.testTabWidget.currentIndex()

        tree = False

        flg = False

        df = self.fileDirLineEdit.text() + '\\' + fn + '.xml'

        try:
            tree = et.parse(df)
        except:
            flg = True

        if flg:
            tree = et.Element('tests')
        else:
            tree = tree.getroot()

        if ind == 0: # AFC

            name = 'FR'
            level = self.TST_AFC_levelLineEdit.text()
            step = self.TST_AFC_stepLineEdit.text()
            beg = self.TST_AFC_freqBeginLineEdit.text()
            end = self.TST_AFC_freqEndLineEdit.text()

            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip
            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.gen_ip
                child.attrib["type"] = 'SMA100A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip

            child = et.SubElement(mn, 'level')
            child.text = level

            child = et.SubElement(mn, 'step')
            child.text = step

            child = et.SubElement(mn, 'beg')
            child.text = beg

            child = et.SubElement(mn, 'end')
            child.text = end


            f = None

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста АЧХ')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест АЧХ')

        if ind == 1: #  усиление
            name = 'Gain'

            level = self.TST_GAIN_levelLineEdit.text()
            beg = self.TST_GAIN_freqBeginLineEdit.text()
            end = self.TST_GAIN_freqEndLineEdit.text()
            step = self.TST_GAIN_stepFreqLineEdit.text()

            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip
            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.gen_ip
                child.attrib["type"] = 'SMA100A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip

            child = et.SubElement(mn, 'level')
            child.text = level

            child = et.SubElement(mn, 'step')
            child.text = step

            child = et.SubElement(mn, 'beg')
            child.text = beg

            child = et.SubElement(mn, 'end')
            child.text = end

            child = et.SubElement(mn, 'file_flg')
            tmp = self.GAIN_checkBox.isChecked()
            if tmp:
                tmp = '1'
            else:
                tmp = '0'
            child.text =tmp

            child = et.SubElement(mn, 'file_dir')
            if tmp == '0':
                child.text = '-1'
            else:
                child.text = self.GAIN_lineEdit.text()

            f = None

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста Усиление')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест Усиление')

        if ind == 2: # PIO
            name = 'P1dB_freq'

            freq = self.TST_PIO_freqLineEdit.text()
            beg = self.TST_PIO_levelBeginLineEdit.text()
            end = self.TST_PIO_levelEndLineEdit.text()
            step = self.TST_PIO_stepLineEdit.text()
            file = self.TST_PIO_getInFileLineEdit.text()

            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip
            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.gen_ip
                child.attrib["type"] = 'SMA100A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip

            child = et.SubElement(mn, 'freq')
            child.text = freq

            child = et.SubElement(mn, 'step')
            child.text = step

            child = et.SubElement(mn, 'beg')
            child.text = beg

            child = et.SubElement(mn, 'end')
            child.text = end

            child = et.SubElement(mn, 'file')
            child.text = file

            f = None

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста Входная-Выходная Мощность')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест  Входная-Выходная Мощность')

        if ind == 3: #POC
            name = 'P1dB'

            beg_f = self.TST_POC_freqBeginLineEdit.text()
            end_f = self.TST_POC_freqEndLineEdit.text()
            step_f = self.TST_POC_stepFreqLineEdit.text()

            beg_l = self.TST_POC_levelBeginLineEdit.text()
            end_l = self.TST_POC_levelEndLineEdit.text()
            step_l = self.TST_POC_stepLevelLineEdit.text()

            g_f = self.POC_getInFileLineEdit.text()

            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip
            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.gen_ip
                child.attrib["type"] = 'SMA100A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip

            child = et.SubElement(mn, 'gain_f')
            child.text = g_f

            child = et.SubElement(mn, 'beg_l')
            child.text = beg_l

            child = et.SubElement(mn, 'step_l')
            child.text = step_l

            child = et.SubElement(mn, 'end_l')
            child.text = end_l

            child = et.SubElement(mn, 'beg_f')
            child.text = beg_f

            child = et.SubElement(mn, 'step_f')
            child.text = step_f

            child = et.SubElement(mn, 'end_f')
            child.text = end_f



            f = None

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста PxdB')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест PxdB')

        if ind == 4: # EFF
            freq = self.TST_EFF_freqLineEdit.text()
            beg = self.TST_EFF_levelBeginLineEdit.text()
            end = self.TST_EFF_levelEndLineEdit.text()
            step =self.TST_EFF_stepLineEdit.text()

            name = 'EFF'

            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return
                if not self.pb48:
                    self.showErr('Не подключен БП!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip

                child = et.SubElement(mn, 'pb5')
                child.text = self.pb5_ip

                child = et.SubElement(mn, 'pb48')
                child.text = self.pb48_ip

            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.gen_ip
                child.attrib["type"] = 'SMA100A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip

                child = et.SubElement(mn, 'pb5')
                child.text = self.pb5_ip

                child = et.SubElement(mn, 'pb48')
                child.text = self.pb48_ip

            child = et.SubElement(mn, 'freq')
            child.text = freq

            child = et.SubElement(mn, 'step')
            child.text = step

            child = et.SubElement(mn, 'beg')
            child.text = beg

            child = et.SubElement(mn, 'end')
            child.text = end

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста КПД')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест КПД')

        if ind == 5: # IMD
            beg = self.TST_IMD_freqBeginLineEdit.text()
            end = self.TST_IMD_freqEndLineEdit.text()
            step =self.TST_IMD_stepLineEdit.text()
            level = self.TST_IMD_levelLineEdit.text()
            sep = self.TST_IMD_sepLineEdit.text()

            name = 'IMD'
            mn = et.SubElement(tree, name)

            if self.saveDevCheckBox.isChecked():

                if not self.gen:
                    self.showErr('Не подключен генератор!')
                    return
                if not self.an:
                    self.showErr('Не подключен анализатор!')
                    return

                child = et.SubElement(mn, 'gen')
                child.text = self.gen.ip
                child.attrib["type"] = self.gen.type

                child = et.SubElement(mn, 'an')
                child.text = self.an.ip
            else:
                child = et.SubElement(mn, 'gen')
                child.text = self.h_gen_ip
                child.attrib["type"] = 'N5182A'

                child = et.SubElement(mn, 'an')
                child.text = self.an_ip


            child = et.SubElement(mn, 'level')
            child.text = level

            child = et.SubElement(mn, 'step')
            child.text = step

            child = et.SubElement(mn, 'beg')
            child.text = beg

            child = et.SubElement(mn, 'end')
            child.text = end

            child = et.SubElement(mn, 'sep')
            child.text = sep

            f = None

            self.indent(tree)

            try:
                f = open(self.fileDirLineEdit.text() + '\\' + fn + '.xml', 'w')
                f.write(et.tostring(tree).decode("utf-8"))
                f.write('\n')
                f.close()
            except:
                self.logTextEditSlot('Ошибка в записи теста IMD')
                f.close()
                return

            self.logTextEditSlot('Успешно записан тест IMD')

    def test(self):

        self.gen.setLevel(-50)
        self.gen.setFrequency(1000)
        self.gen.setFreqTwoTone(10, 'MHz')
        self.gen.enableMod()
        self.gen.enableTwoTone(True)
        self.gen.RFOutON()

    def openParamsPushButtonClicked(self):
        pass

    def TST_GAIN_selectInFilePushButtonClicked(self):
        self.GAIN_lineEdit.setText(QFileDialog.getExistingDirectory())

    def manDirResClicked(self):
        self.manResFileDirLineEdit.setText(QFileDialog.getExistingDirectory())

    def EQU_controlPushButtonClicked(self):
        if self.an and self.an.fullName != '':
            try:
                self.an.setDisplay(self.EQU_displayOnRadio.isChecked())
                self.an.setSweep(float(self.EQU_sweepLineEdit.text()))
            except:
                pass
        else:
            self.showErr('Необходимое оборудование не подключено!')

    def devONpushButtonClicked(self):
        if self.pb5.fullName and self.pb48.fullName:
            self.pb5.setVolt(5, 3)
            self.pb5.setAmp(1.5, 3)
            self.pb48.setVolt(48.8)

            self.pb5.setOut(True, 3)

            time.sleep(3)

            self.pb48.setOut(True)

        else:
            self.showErr('Оборудование не подключено!')

    def devOFFpushButtonClicked(self):
        if self.pb5.fullName and self.pb48.fullName:
            self.pb48.setOut(False)
            time.sleep(3)
            self.pb5.setOut(False, 3)
        else:
            self.showErr('Оборудование не подключено!')


    def addScreenSlot(self, path=None):
        p = self.MPL_additGraphicsView.grab()

        if not path:
            date = datetime.datetime.now()

            path = QFileDialog.getExistingDirectory()
            path = path + '\\Screenshot_' + date.strftime('%Y-%m-%d_%H-%M._add.jpg')

            p.save(path, 'jpg')
        else:
            p.save(path + '.jpg', 'jpg')

    def specScreenSlot(self, path=None):
        p = self.MPL_graphicsView.grab()

        if not path:
            date = datetime.datetime.now()

            path = QFileDialog.getExistingDirectory()
            path = path + '\\Screenshot_' + date.strftime('%Y-%m-%d_%H-%M._spec.jpg')

            p.save(path, 'jpg')
        else:
            p.save(path + '.jpg', 'jpg')



    # -------------------- Работа со спектограммой

    def specCalcMaxOffset(self, Z, cent):

        Z = np.array(Z)

        _max = Z.max()

        ind = np.where(Z == _max)

        if len(ind[0]) == 1:
            return ind
        else:
            ind = min(ind[0], key=lambda t: abs(t - cent))
            return ind

    def specCalcBW(self, point, Z):
        pass

    def calcBW(self, n, x, y):

        y = y.tolist()
        x = x.tolist()
        maax = max(y)

        # -------

        val = maax - n

        val_l = min(y[0:y.index(maax)], key=lambda t: abs(t - val))
        val_l = y[0:y.index(maax)].index(val_l)
        val_l = x[val_l]

        val_r = min(y[y.index(maax):len(y)], key=lambda t: abs(t - val))
        val_r = y[y.index(maax):len(y)].index(val_r) + y.index(maax)
        val_r = x[val_r]

        res = round(val_r - val_l, 2)

        return [val_l, val_r, res]


    def specReadClicked(self):


        bias = MPL_Plot()  # нижняя граница
        bias.title = 'Смещение центра полосы пропускания'
        bias.col = 'g'
        bias.y.append([])

        bw6 = MPL_Plot()
        bw6.title = 'Полоса пропускания по уровню -6 dB'
        bw6.col = 'y'
        bw6.y.append([])
        bw6.y.append([])

        bw3 = MPL_Plot()
        bw3.title = 'Полоса пропускания по уровню -3 dB'
        bw3.col = 'b'
        bw3.y.append([])
        bw3.y.append([])

        file = open(self.grapPath.text(), 'r')

        X = []
        Y = []
        Z = []

        if True:
            sch = 0

            for line in file:
                if line.find('---') != -1:
                    sch = sch + 1
                    continue

                line = line.replace('\n', '')
                subarr = line.split(' ')

                if len(subarr) < 5:
                    continue

                subarr = [round(float(s),1) for s in subarr if s != '']

                if sch == 0:
                    X.append(subarr)
                if sch == 1:
                    Y.append(subarr)
                if sch == 2:
                    Z.append(subarr)

            _X = np.array(X)
            _Y = np.array(Y)
            _Z = np.array(Z)

            _size = _Z.shape


            cent = (_Z.shape[1] - 1) / 2


            for i in range(_size[0]):  #срезаем шум
                for j in range(_size[1]):
                   if _Z[i][j] < -50:
                       _Z[i][j] = -50

            for i in range(_size[0]): #вычислчяем все относительно пика
                _max = _Z[i].max()
                for j in range(_size[1]):
                    _Z[i][j] = _Z[i][j] -  _max

            for i in range(_size[0]):  #считаем
                ind_max = self.specCalcMaxOffset(Z[i], cent)
                _bw3 = self.calcBW(3, _Y[0], _Z[i])
                _bw6 = self.calcBW(6, _Y[0], _Z[i])
                freq = _X[i][0]
                offset = _Y[0][ind_max]

                bias.x.append(freq)
                bias.y[0].append(-offset)

                bw3.x.append(freq)
                bw3.y[0].append(-_bw3[0])
                bw3.y[1].append(-_bw3[1])

                bw6.x.append(freq)
                bw6.y[0].append(-_bw6[0])
                bw6.y[1].append(-_bw6[1])


            self.MPL_graphicsView.plotSpecSlot(_X, _Y, _Z)



            self.MPL_graphicsView.initLabels('Смещение относительно частоты подстройки',
                                             'Частота подстройки',
                                             'Полоса пропускания')

            self.MPL_graphicsView.plotOverSpec([bias, bw3, bw6])


            self.plot_graph( range(-350, 350+1),_Z[1270], 'red')
            self.plotAddLine(False,  -bias.y[0][1270], 'green')

        #except:
         #   raise
        #finally:
        file.close()
         #   return


    # ------------------------------------------------------------------





    def plot3dUpdateVals(self):
        self.plot3d_refreshParams()
        self.MPL_additGraphicsView.plot3D(self.plot3d)

    def plot3d_refreshParams(self):

 #        self.plot3d.sigma_x = float(self.plot3d_xSpinBox.text().replace(',', '.'))
 #       self.plot3d.sigma_y = float(self.plot3d_ySpinBox.text().replace(',', '.'))
 #       self.plot3d.mode = self.plot3d_modeComboBox.currentText()
        self.plot3d.peak = float(self.plot3dpeakLineEdit.text())
        self.plot3d.x_shape = int(self.plot3d_shapeXineEdit.text())
        self.plot3d.y_shape = int(self.plot3d_shapeYineEdit.text())

    def pushButton3dClicked(self, file=None):

        self.plot3d = MPL_3dPlot()
        self.plot3d_refreshParams()

        if not file:
            file = open(self.grapPath.text(), 'r')
        else:
            file = open(file, 'r')

        x  = []
        y  = []
        z  = []

        __z = 0

        for line in file:
            _x, _y, _z0, _z1 = line.split(' ')

            _x = float(_x)
            _y = float(_y)
            _z0 = float(_z0)
            _z1 = float(_z1)



            if _z1 != __z:
                x.append([])
                y.append([])
                z.append([])

            x[len(x) - 1].append(_x)
            y[len(x) - 1].append(_y)
            z[len(x) - 1].append(_z0 - _z1)

            __z = _z1




        self.MPL_additGraphicsView.init3Dslot()

        self.MPL_additGraphicsView.plot3D(self.plot3d, x, y, z)

        file.close()

        """
        

        #file = open('C:/Users/User/Desktop/Панорама_MIRR_500_505MHz.3d', 'r')
        
        file = open(self.grapPath.text(), 'r')

        sch = 0

        X = []
        Y = []
        Z = []

        for line in file:
            if line.find('---') != -1:
                sch = sch + 1
                continue

            line = line.replace('\n', '')
            subarr = line.split(' ')

            if len(subarr) < 5:
                continue

            subarr = [round(float(s), 1) for s in subarr if s != '']

            if sch == 0:
                X.append(subarr)
            if sch == 1:
                Y.append(subarr)
            if sch == 2:
                Z.append(subarr)

        # -------------------

        #a = 20
        #b = 200

        #X = X[a:b]
        #Y = Y[a:b]
        #Z = Z[a:b]



        # -----------------

        self.plot3d.X = np.array(X, dtype=np.double)
        self.plot3d.Y = np.array(Y, dtype=np.double)
        self.plot3d.Z = np.array(Z, dtype=np.double)



        _min = self.plot3d.Z.min()

        self.plot3d.Z[self.plot3d.Z == _min] = np.nan


        # --------
        """
#        self.MPL_additGraphicsView.plot3D(self.plot3d)

    #-----------------------------------------------------------------------------------

    def __init__(self):



        super(MW, self).__init__()




        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.initWindow()

        self.pushButton3d.clicked.connect(self.pushButton3dClicked)

        self.colors = {'red': (255, 0, 0),
                       'green': (0, 255, 0),
                       'blue': (0, 0, 255),
                       'yellow': (255, 255, 0),
                       'brown': (165, 42, 42)}


        self.an = None
        self.gen = None
        self.dev = None
        self.rm = visa.ResourceManager()
        self.pb48 = None
        self.pb5 = None

        # -----

        self.cal_out = {}
        self.cal_in = {}

        # -----
        self.GET_outCheckBox.stateChanged.connect(self.GET_outCheckBoxChecked)
        self.GET_inCheckBox.stateChanged.connect(self.GET_inCheckBoxChecked)
        self.GET_get1FixCheckBox.stateChanged.connect(self.GET_get1FixCheckBoxChecked)
        self.GET_get2FixCheckBox.stateChanged.connect(self.GET_get2FixCheckBoxChecked)
        self.GET_get2CheckBox.stateChanged.connect(self.GET_get2CheckBoxChecked)
        self.specScreenshotPushButton.clicked.connect(self.specScreenSlot)
        self.addScreenshotPushButton.clicked.connect(self.addScreenSlot)
        self.graphRead.clicked.connect(self.graphReadClicked)
        self.graphSelect.clicked.connect(self.graphSelectClicked)
        self.NF_gainPushButton.clicked.connect(self.NF_gainPushButtonClicked)
        self.ATT_gainPushButton.clicked.connect(self.ATT_gainPushButtonClicked)
        self.devONpushButton.clicked.connect(self.devONpushButtonClicked)
        self.devOFFpushButton.clicked.connect(self.devOFFpushButtonClicked)
        self.EQU_controlPushButton.clicked.connect(self.EQU_controlPushButtonClicked)
        self.EQU_PB5_connectPushButton.clicked.connect( self.EQU_PB5_connectPushButtonClicked)
        self.EQU_searchPushButton.clicked.connect(self.EQU_searchPushButtonClicked)
        self.manDirRes.clicked.connect(self.manDirResClicked)
        self.specRead.clicked.connect(self.specReadClicked)

        self.testTabWidget.currentChanged.connect(self.testTabWidgetSlot)

        self.TST_PIO_selectInFilePushButton.clicked.connect(self.TST_PIO_selectInFilePushButtonClicked)
        self.POC_selectInFilePushButton.clicked.connect(self.POC_selectInFilePushButtonClicked)
        self.fileDirPushButton.clicked.connect(self.fileDirPushButtonClicked)
        self.clearTestFile.clicked.connect(self.clearTestFileClicked)
        self.dirRes.clicked.connect(self.dirResClicked)
        self.CAL_selectFilePushButton.clicked.connect(self.CAL_selectFilePushButtonClicked)

        #-----

        self.cal_test = CAL_Test()
        self.cal_test.progress_signal.connect(self.progressSlot)
        self.cal_test.log_signal.connect(self.logTextEditSlot)

        # -----

        self.acc = ACC_Test()

        self.acc.progress_signal.connect(self.progressSlot)
        self.acc.log_signal.connect(self.logTextEditSlot)
        self.acc.plot_signal.connect(self.plot_graph)
        self.acc.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect( self.acc.stop)
        self.acc.savescreen_signal.connect(self.screenshotSlot)
        self.acc.tray_signal.connect(self.traySlot)

        # -----

        self.bf = BF_Test()

        self.bf.progress_signal.connect(self.progressSlot)
        self.bf.log_signal.connect(self.logTextEditSlot)
        self.bf.plot_signal.connect(self.plot_graph)
        self.bf.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.bf.stop)
        self.bf.savescreen_signal.connect(self.screenshotSlot)
        self.bf.savescreen_an_signal.connect(self.anScrSlot)
        self.bf.tray_signal.connect(self.traySlot)


        # -----

        self.mirr = MIRR_Test()

        self.mirr.progress_signal.connect(self.progressSlot)
        self.mirr.savescreen_signal.connect(self.screenshotSlot)
        self.mirr.log_signal.connect(self.logTextEditSlot)
        self.mirr.plot_signal.connect(self.plot_graph)
        self.stopTestPushButton.clicked.connect(self.mirr.stop)
        self.mirr.tray_signal.connect(self.traySlot)
        self.mirr.mpl_plot_3d.connect(self.pushButton3dClicked)


        # -----

        self.afc = AFC_Test()

        self.afc.progress_signal.connect(self.progressSlot)
        self.afc.log_signal.connect(self.logTextEditSlot)
        self.afc.plot_signal.connect(self.plot_graph)
        self.afc.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect( self.afc.stop)
        self.afc.savescreen_signal.connect(self.screenshotSlot)
        self.afc.tray_signal.connect(self.traySlot)
        self.afc.addline_signal.connect(self.plotAddLine)
        self.afc.savescreen_an_signal.connect(self.anScrSlot)

        # ----

        self.att = ATT_Test()

        self.att.progress_signal.connect(self.progressSlot)
        self.att.log_signal.connect(self.logTextEditSlot)
        self.att.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.att.stop)
        self.att.mpl_plot.connect(self.MPL_additGraphicsView.plotGraphSlot)

        # ---

        self.sif = SIF_Test()

        self.sif.progress_signal.connect(self.progressSlot)
        self.sif.log_signal.connect(self.logTextEditSlot)
        self.sif.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.sif.stop)
        self.sif.mpl_plot.connect(self.MPL_additGraphicsView.plotGraphSlot)

        # -----

        self.nf = NF_Test()

        self.nf.progress_signal.connect(self.progressSlot)
        self.nf.log_signal.connect(self.logTextEditSlot)
        self.nf.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.nf.stop)
        self.nf.mpl_plot.connect(self.MPL_additGraphicsView.plotGraphSlot)

        # -----

        self.pn = PN_Test()
        self.pn.progress_signal.connect(self.progressSlot)
        self.pn.log_signal.connect(self.logTextEditSlot)
        self.pn.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.pn.stop)
        self.pn.mpl_plot.connect(self.MPL_additGraphicsView.plotGraphSlot)
        self.pn.mpl_set_graph_title.connect(self.MPL_additGraphicsView.setTitleGraph)
        self.pn.tray_signal.connect(self.traySlot)

        # -----

        self.ud = UD_Test()

        self.ud.progress_signal.connect(self.progressSlot)
        self.ud.log_signal.connect(self.logTextEditSlot)
        self.ud.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect( self.ud.stop)
        self.ud.savescreen_an_signal.connect(self.anScrSlot)

        # -----

        self.gain = GAIN_Test()

        self.gain.progress_signal.connect(self.progressSlot)
        self.gain.log_signal.connect(self.logTextEditSlot)
        self.gain.plot_signal.connect(self.plot_graph)
        self.gain.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.gain.stop)
        self.gain.savescreen_signal.connect(self.screenshotSlot)
        self.gain.tray_signal.connect(self.traySlot)
        # -----

        self.pio = PIO_Test()

        self.pio.progress_signal.connect(self.progressSlot)
        self.pio.log_signal.connect(self.logTextEditSlot)
        self.pio.plot_signal.connect(self.plot_graph)
        self.pio.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect( self.pio.stop)
        self.pio.savescreen_signal.connect(self.screenshotSlot)
        self.pio.tray_signal.connect(self.traySlot)
        # -----

        self.poc = POC_test()

        self.poc.progress_signal.connect(self.progressSlot)
        self.poc.log_signal.connect(self.logTextEditSlot)
        self.poc.plot_signal.connect(self.plot_graph)
        self.poc.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect( self.poc.stop)
        self.poc.savescreen_signal.connect(self.screenshotSlot)
        self.poc.tray_signal.connect(self.traySlot)
        # -----

        self.eff = EFF_Test()

        self.eff.progress_signal.connect(self.progressSlot)
        self.eff.log_signal.connect(self.logTextEditSlot)
        self.eff.plot_signal.connect(self.plot_graph)
        self.eff.end_signal.connect(self.setProgOnWork)
        self.stopTestPushButton.clicked.connect(self.eff.stop)
        self.eff.tray_signal.connect(self.traySlot)
        # -----

        self.imd = IMD_Test()

        self.imd.progress_signal.connect(self.progressSlot)
        self.imd.log_signal.connect(self.logTextEditSlot)
        self.imd.plot_signal.connect(self.plot_graph)
        self.stopTestPushButton.clicked.connect(self.imd.stop)
        self.imd.tray_signal.connect(self.traySlot)

        # -----


        self.bw = BW_Test()

        self.bw.progress_signal.connect(self.progressSlot)
        self.bw.mpl_plot_over_spec.connect(self.MPL_graphicsView.plotOverSpec)
        self.bw.log_signal.connect(self.logTextEditSlot)
        self.stopTestPushButton.clicked.connect(self.bw.stop)
        self.bw.spec_signal.connect(self.MPL_graphicsView.plotSpecSlot)
        self.bw.mpl_plot_signal.connect(self.MPL_additGraphicsView.plotGraphSlot)
        self.bw.mpl_set_plot_count.connect(self.MPL_additGraphicsView.initGraphSlot)
        self.bw.mpl_set_spec_count.connect(self.MPL_graphicsView.initSpecSlot)
        self.bw.mpl_set_graph_title.connect(self.MPL_additGraphicsView.setTitleGraph)
        self.bw.mpl_set_spec_title.connect(self.MPL_graphicsView.setTitleSpec)
        self.bw.mpl_save_add_graph.connect(self.addScreenSlot)   # не проверено
        self.bw.mpl_save_spec.connect(self.specScreenSlot)

        #--------

        self.get =  GET_Test()

        self.get.mpl_set_graph_title.connect(self.MPL_additGraphicsView.setTitleGraph)
        self.get.progress_signal.connect(self.progressSlot)
        self.get.log_signal.connect(self.logTextEditSlot)
        self.stopTestPushButton.clicked.connect(self.get.stop)
        self.get.mpl_plot_signal.connect(self.MPL_additGraphicsView.plotGraphSlot)
        self.get.mpl_set_plot_count.connect(self.MPL_additGraphicsView.initGraphSlot)
        self.get.mpl_set_graph_title.connect(self.MPL_additGraphicsView.setTitleGraph)
        self.get.mpl_save_add_graph.connect(self.addScreenSlot)


        # ------

        #self.plotTestGraph()

       # self.PAN_portComboBox.addItems(self.pan.listPorts())

        self.screenshotPushButton.clicked.connect(self.screenshotSlot)
        self.PAN_autosearchPushButton.clicked.connect(self.PAN_autosearchPushButtonClicked)
        self.PAN_sendConsolePushButton.clicked.connect(self.PAN_sendConsolePushButtonClicked)
        self.PAN_connectPushButton.clicked.connect(self.PAN_connectPushButtonClicked)
        self.PAN_disconnectPushButton.clicked.connect(self.PAN_disconnectPushButtonClicked)
        self.PAN_clearConsolePushButton.clicked.connect(self.PAN_clearConsolePushButtonClicked)
        self.PAN_refreshPortsPushButton.clicked.connect(self.PAN_refreshPortsPushButtonClicked)
        self.PAN_testConnectionPushButton.clicked.connect( self.PAN_testConnectionPushButtonClicked)
        self.PAN_setAttenPushButton.clicked.connect(self.PAN_setAttenPushButtonClicked)
        self.PAN_getAttenPushButton.clicked.connect(self.PAN_getAttenPushButtonClicked)
        self.PAN_getDacPushButton.clicked.connect(self.PAN_getDacPushButtonClicked)
        self.PAN_setDacPushButton.clicked.connect(self.PAN_setDacPushButtonClicked)
        self.PAN_setInjPushButton.clicked.connect(self.PAN_setInjPushButtonClicked)
        self.PAN_getInjPushButton.clicked.connect(self.PAN_getInjPushButtonClicked)
        self.PAN_setModePushButton.clicked.connect(self.PAN_setModePushButtonClicked)
        self.PAN_getModePushButton.clicked.connect(self.PAN_getModePushButtonClicked)
        self.PAN_setTcxoPushButton.clicked.connect(self.PAN_setTcxoPushButtonClicked)
        self.PAN_getTcxoPushButton.clicked.connect(self.PAN_getTcxoPushButtonClicked)
        self.PAN_setRefPushButton.clicked.connect(self.PAN_setRefPushButtonClicked)
        self.PAN_getRefPushButton.clicked.connect(self.PAN_getRefPushButtonClicked)
        self.PAN_SetFreqPushButton.clicked.connect(self.PAN_SetFreqPushButtonClicked)
        self.PAN_GetFreqPushButton.clicked.connect(self.PAN_GetFreqPushButtonClicked)
        self.getAnScrPushButton.clicked.connect(self.anScrSlot)
        self.PAN_setLnaPushButton.clicked.connect(self.PAN_setLnaPushButtonClicked)
        self.PAN_getLnaPushButton.clicked.connect(self.PAN_getLnaPushButtonClicked)
        self.AN_consolePushButton.clicked.connect(self.AN_consolePushButtonClicked)



        self.testTabWidgetSlot(self.testTabWidget.currentIndex())
        # ----- Что бы не тыкать при старте

        #self.searchDev()
        self.CAL_getFilePushButtonClicked()
        self.PAN_autosearchPushButtonClicked()

        self.EQU_AN_connectPushButtonClicked()
        self.EQU_GEN_connectPushButtonClicked()

        # ------ Трей

        icon = QIcon("123.png")
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.show()


        # ---- выставление настроек графиков
        # ---- выставление настроек графиков

        self.plot3d_xSpinBox.valueChanged.connect(self.plot3dUpdateVals)
        self.plot3d_ySpinBox.valueChanged.connect(self.plot3dUpdateVals)
        self.plot3d_modeComboBox.currentIndexChanged.connect(self.plot3dUpdateVals)

        #self.MPL_additGraphicsView.initGraphSlot(2)
        self.MPL_graphicsView.initSpecSlot()

        # ------- Тестовая область

        self.MPL_additGraphicsView.init3Dslot()

        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

       # self.MPL_additGraphicsView.plot3D(X, Y, Z)

        #self.test3D()
        #self.specReadClicked()


       # self.pushButton3dClicked()
    def test3D(self):

        self.MPL_additGraphicsView.init3Dslot()

        x = np.arange(500, 800 + 1, 1)
        y = np.arange(750, 1000 + 1, 1)

        X, Y = np.meshgrid(x, y)

        def_value = 0

        _size = X.shape

        Z = np.zeros(shape=(_size[0], _size[1]))

        for i in range(_size[0]):
            for j in range(_size[1]):
                Z[i][j] = np.random.randint(-70, -68)
                Z[i][j] = -10

        def_value = Z.min() - 1

        for i in range(_size[0]):
            for j in range(_size[1]):
                if (j < i + 200) and (j > i - 200):
                    Z[i][j] = def_value



        self.MPL_additGraphicsView.plot3D(X, Y, Z)

#        surf = plot_surface(X, Y, Z, cmap=cm.coolwarm,
     #                          linewidth=0, antialiased=False)

    def GET_inCheckBoxChecked(self):
        if self.GET_inCheckBox.isChecked():
            self.GET_outCheckBox.setChecked(False)
        else:
            self.GET_outCheckBox.setChecked(True)

    def GET_outCheckBoxChecked(self):
        if self.GET_outCheckBox.isChecked():
            self.GET_inCheckBox.setChecked(False)
        else:
            self.GET_inCheckBox.setChecked(True)

    def GET_get2CheckBoxChecked(self):
        if self.GET_get2CheckBox.isChecked():
            if self.GET_get2FixCheckBox.isChecked():
                self.GET_get2lineEdit.setEnabled(True)
            self.GET_get2FixCheckBox.setEnabled(True)
        else:
            self.GET_get2lineEdit.setEnabled(False)
            self.GET_get2FixCheckBox.setEnabled(False)


    def AN_consolePushButtonClicked(self):
        self.an.hAnalyzer.write(self.AN_consoleLineEdit.text())
        #self.MPL_graphicsView.testPlot()

    def progressSlot(self, val):
        self.logProgressBar.setValue(val)
        self.traySlot('Status', str(self.logProgressBar.text()))

    def anScrSlot(self, name=None, path=None):

        try:
            self.an.getScreenshot()
            while not os.path.isfile('C:\\NET\\scr.BMP'):
                pass
            time.sleep(0.3)
            if not name:
                shutil.copy('C:\\NET\\scr.BMP', QFileDialog.getExistingDirectory())
                time.sleep(0.3)
                os.remove('C:\\NET\\scr.BMP')
            else:
                shutil.copy('C:\\NET\\scr.BMP', path)
                time.sleep(0.3)
                os.remove('C:\\NET\\scr.BMP')
                time.sleep(0.3)
                os.rename(path + 'scr.BMP', path + name)
        except Exception as e:
            self.showErr(str(e))


    #  ----- Управление Панорамой

    def PAN_setLnaPushButtonClicked(self):
        val = self.PAN_setLnaComboBox.currentText()

        if val == 'ON':
            self.pan.setLNA(True)
        elif val == 'OFF':
            self.pan.setLNA(False)

    def PAN_getLnaPushButtonClicked(self):
        val = self.pan.getLNA()
        if(val):
            self.PAN_setLnaComboBox.setCurrentIndex(self.PAN_setLnaComboBox.findText('ON', QtCore.Qt.MatchFixedString))
        else:
            self.PAN_setLnaComboBox.setCurrentIndex(self.PAN_setLnaComboBox.findText('OFF', QtCore.Qt.MatchFixedString))

    def PAN_setTcxoPushButtonClicked(self):
        val = self.PAN_setTcxoComboBox.currentText()

        if val == 'ON':
            res = self.pan.setTcxo('on')
            if not res:
                self.logTextEditSlot('Ошибка при выполнении команды!')
            else:
                self.logTextEditSlot('Успешно.')
        elif val == 'OFF':
            res = self.pan.setTcxo('off')
            if not res:
                self.logTextEditSlot('Ошибка при выполнении команды!')
            else:
                self.logTextEditSlot('Успешно.')

    def PAN_getTcxoPushButtonClicked(self):
        val = self.pan.getTcxo()

        if val:
            self.logTextEditSlot('Успешно.')
            self.PAN_setTcxoComboBox.setCurrentIndex(self.PAN_setTcxoComboBox.findText(val, QtCore.Qt.MatchFixedString))
        else:
            self.logTextEditSlot('Ошибка при выполнении команды!')

    def PAN_setRefPushButtonClicked(self):
        val = self.pan.setRef(self.PAN_setRefComboBox.currentText())
        if not val:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')

    def PAN_getRefPushButtonClicked(self):
        val = self.pan.getRef()

        if not val:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')
            self.PAN_setRefComboBox.setCurrentIndex(self.PAN_setRefComboBox.findText(val, QtCore.Qt.MatchFixedString))

    def PAN_SetFreqPushButtonClicked(self):
        val = self.pan.setFreq(float(self.PAN_FreqLineEdit.text()))

        if not val:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')

    def PAN_GetFreqPushButtonClicked(self):
        res = self.pan.getFreq()

        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')
            self.PAN_FreqLineEdit.setText(str(res))

    def PAN_setModePushButtonClicked(self):
        res = self.pan.setMode(self.PAN_setModeComboBox.currentText())

        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')

    def PAN_getModePushButtonClicked(self):
        res = self.pan.getMode()

        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')
            if res == 'work':
                self.PAN_setModeComboBox.setCurrentIndex(
                    self.PAN_setModeComboBox.findText('work', QtCore.Qt.MatchFixedString))
            elif res == 'standby':
                self.PAN_setModeComboBox.setCurrentIndex(
                    self.PAN_setModeComboBox.findText('standby', QtCore.Qt.MatchFixedString))

    def PAN_setInjPushButtonClicked(self):
        val = self.PAN_setInjComboBox.currentText()
        if val == 'ON':
            res = self.pan.setInj(True)
            if not res:
                self.logTextEditSlot('Ошибка при выполнении команды!')
            else:
                self.logTextEditSlot('Успешно.')
        if val == 'OFF':
            res = self.pan.setInj(False)
            if not res:
                self.logTextEditSlot('Ошибка при выполнении команды!')
            else:
                self.logTextEditSlot('Успешно.')

    def PAN_getInjPushButtonClicked(self):
        res = self.pan.getInj()

        if res == None:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')
            if res:
                self.PAN_setInjComboBox.setCurrentIndex(self.PAN_setInjComboBox.findText('ON', QtCore.Qt.MatchFixedString))
            else:
                self.PAN_setInjComboBox.setCurrentIndex(self.PAN_setInjComboBox.findText('OFF', QtCore.Qt.MatchFixedString))

    def PAN_setAttenPushButtonClicked(self):
        res = self.pan.setAtt(float(self.PAN_attenLineEdit.text()))
        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')

    def PAN_getAttenPushButtonClicked(self):
        res = self.pan.getAtt()
        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.PAN_attenLineEdit.setText(str(res))
            self.logTextEditSlot('Успешно.')

    def PAN_setDacPushButtonClicked(self):
        res = self.pan.setDAC(int(self.PAN_dacLineEdit.text()))
        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.logTextEditSlot('Успешно.')

    def PAN_getDacPushButtonClicked(self):
        res = self.pan.getDAC()
        if not res:
            self.logTextEditSlot('Ошибка при выполнении команды!')
        else:
            self.PAN_dacLineEdit.setText(str(res))
            self.logTextEditSlot('Успешно.')

    def PAN_testConnectionPushButtonClicked(self):
        try:
            if self.pan.testConnection():
                self.logTextEditSlot('Успешно.')
            else:
                self.logTextEditSlot('Ошибка при чтении ответа.')
        except:
            self.logTextEditSlot('Ошибка при отправке сообщения.')

    def PAN_refreshPortsPushButtonClicked(self):
        try:
            self.PAN_portComboBox.clear()
            self.PAN_portComboBox.addItems(self.pan.listPorts())
        except:
            pass

    def PAN_clearConsolePushButtonClicked(self):
        self.PAN_consoleLineEdit.clear()
        self.PAN_consoleTextBrowser.clear()

    def PAN_disconnectPushButtonClicked(self):
        try:
            self.pan.disconnect()
        except:
            pass

        self.PAN_statusLabel.setText('Отключено')
        self.PAN_sendConsolePushButton.setEnabled(False)
        self.PAN_testConnectionPushButton.setEnabled(False)
        self.PAN_disconnectPushButton.setEnabled(False)
        self.PAN_autosearchPushButton.setDisabled(False)
        self.PAN_connectPushButton.setDisabled(False)
        self.PAN_allComGroupBox.setDisabled(True)

    def PAN_connectPushButtonClicked(self):

        port = self.PAN_portComboBox.currentText()

        try:
            self.pan.connect(port)
            self.PAN_statusLabel.setText('Подключено')
            self.PAN_sendConsolePushButton.setEnabled(True)
            self.PAN_testConnectionPushButton.setEnabled(True)
            self.PAN_disconnectPushButton.setEnabled(True)
            self.PAN_autosearchPushButton.setDisabled(True)
            self.PAN_connectPushButton.setDisabled(True)
            self.PAN_allComGroupBox.setDisabled(False)
            self.logTextEditSlot('Warninig:\tПорт открыт, но не проверена правильность подключения.')
        except:
            self.logTextEditSlot('Не удалось подключиться к устройству!')
            self.PAN_statusLabel.setText('Ошибка подключения!')

    def PAN_sendConsolePushButtonClicked(self):

        self.PAN_consoleTextBrowserWriteToLog('Request:\t' + self.PAN_consoleLineEdit.text())

        try:
            resp = self.pan.ask(self.PAN_consoleLineEdit.text())

            if not resp:
                self.PAN_consoleTextBrowserWriteToLog('Error:\tНе удалось выполнить команду!')
            else:
                self.PAN_consoleTextBrowserWriteToLog('Response:')
                for text in resp:
                    self.PAN_consoleTextBrowserWriteToLog('\t' + text)

        except:
            #raise
            self.PAN_consoleTextBrowserWriteToLog('Error:\tОшибка при выполнении!')

        self.PAN_consoleLineEdit.setText('')

    def PAN_autosearchPushButtonClicked(self):

        port = self.pan.search()

        if port:
            try:
                self.pan.connect(port)
                self.PAN_statusLabel.setText('Подключено')
                self.PAN_sendConsolePushButton.setEnabled(True)
                self.PAN_testConnectionPushButton.setEnabled(True)
                self.PAN_disconnectPushButton.setEnabled(True)
                self.PAN_autosearchPushButton.setDisabled(True)
                self.PAN_connectPushButton.setDisabled(True)
                self.PAN_allComGroupBox.setDisabled(False)

                self.logTextEditSlot('Успешно.')
            except:
                self.logTextEditSlot('Не удалось подключиться к устройству!')
                self.PAN_statusLabel.setText('Ошибка подключения!')

        else:
            self.logTextEditSlot('Не удалось найти устройство!')

    def PAN_consoleTextBrowserWriteToLog(self, text):
        if self.PAN_consoleTextBrowser.toPlainText() == '':
            self.PAN_consoleTextBrowser.setText(text)
        else:
            self.PAN_consoleTextBrowser.setText(self.PAN_consoleTextBrowser.toPlainText() + '\n' + text)

    # -----

    def plotTestGraph(self):
        x = []
        y = []

        for i in range(100):
            x.append(i)
            y.append(math.exp(i))

        self.plot_graph(x, y)

    def setPB(self, state):
        self.pb5.setAmp(1.5, 4)
        self.pb5.setVolt(5, 4)

        if state:
            self.pb5.setOut(True, 4)
            time.sleep(3)
            self.pb48.setOut(True)
        else:

            self.pb48.setOut(False)
            time.sleep(3)
            self.pb5.setOut(False, 4)

    def initWindow(self):

        # ----- Общие настройки

        self.setupUi(self)
        self.setCentralWidget(self.cw)

        self.mainGraphicsView.plotItem.showGrid(x=None, y=None, alpha=1.0)
        self.mainGraphicsView.plotItem.showGrid(1, 1)

        self.initSignals()
        self.initTextFilters()

        # ----- Сигналы

    def initSignals(self):
        self.startAutoPushButton.clicked.connect(self.startAutoPushButtonClicked)

        self.fileAutoPushButton.clicked.connect(self.fileAutoPushButtonClicked)
        self.saveParamsPushButton.clicked.connect( self.saveParamsPushButtonClicked)


        # ----- Управление устройством

        self.DEV_connectPushButton.clicked.connect(self. DEV_connectPushButtonClicked)
        self.DEV_disconnectPushButton.clicked.connect(self.DEV_disconnectPushButtonClicked)
        self.DEV_setAttenPushButton.clicked.connect(self.DEV_setAttenPushButtonClicked)
        self.DEV_getAttenPushButton.clicked.connect(self.DEV_getAttenPushButtonClicked)
        self.DEV_getTempPushButton.clicked.connect(self.DEV_getTempPushButtonClicked)
        self.DEV_getStatusPushButton.clicked.connect(self.DEV_getStatusPushButtonClicked)

        # ----- Кнопки управления

        self.startTestPushButton.clicked.connect(self.startTestPushButtonClicked)
        self.clearLogPushButton.clicked.connect( self.clearLogPushButtonClicked)
        self.stopTestPushButton.clicked.connect( self.stopTestPushButtonClicked)

        # ----- Кнопки калибровки

        self.CAL_getFilePushButton.clicked.connect(self.CAL_getFilePushButtonClicked)
        self.CAL_selectInFilePushButton.clicked.connect(self.CAL_selectInFilePushButtonClicked)
        self.CAL_selectOutFilePushButton.clicked.connect(self.CAL_selectOutFilePushButtonClicked)
        self.CAL_startPushButton.clicked.connect(self.CAL_startPushButtonClicked)

        # ----- Кнопки оборудования

        self.EQU_AN_connectPushButton.clicked.connect(self. EQU_AN_connectPushButtonClicked)
        self.EQU_AN_disconnectPushButton.clicked.connect(self.EQU_AN_disconnectPushButtonClicked)

        self.EQU_PB48_connectPushButton.clicked.connect(self.EQU_PB48_connectPushButtonClicked)

        self.EQU_AN_resetPushButton.clicked.connect(self.EQU_AN_resetPushButtonClicked)
        self.EQU_GEN_connectPushButton.clicked.connect(self.EQU_GEN_connectPushButtonClicked)
        self.EQU_GEN_disconnectPushButton.clicked.connect(self.EQU_GEN_disconnectPushButtonClicked)
        self.EQU_GEN_resetPushButton.clicked.connect(self.EQU_GEN_resetPushButtonClicked)

        self.EQU_refreshPushButton.clicked.connect(self.EQU_refreshPushButtonClicked)

    # ----- Работа с графиком

    def plot_graph(self, x, y, color=None, clr=True):

        self._x = x
        self._y = y

        if not color:
            color = 'red'

        if clr:
            self.mainGraphicsView.plotItem.clear()
        try:
            self.plot = self.mainGraphicsView.plotItem.plot(x, y)
            self.plot.setPen(self.colors[color])
        except:
            pass

    def plotAddLine(self, flg, pos, pen):
        # flg == True ---> паралельно OX
        if flg:
            line = pg.InfiniteLine(angle=0, pos=(0, pos), pen=self.colors[pen])
        else:
            line = pg.InfiniteLine(angle=90, pos=(pos), pen=self.colors[pen])
        self.mainGraphicsView.plotItem.addItem(line)

    # ----- Текстовые фильтры

    def initTextFilters(self):

        self.num = QtGui.QRegExpValidator(QtCore.QRegExp('[\d]+'))
        self.num_sign = QtGui.QRegExpValidator(QtCore.QRegExp('-?[\d]+'))
        self.num_float = QtGui.QRegExpValidator(QtCore.QRegExp('[\d]+\.?[\d]+'))
        self.num_sign_float = QtGui.QRegExpValidator(QtCore.QRegExp('-?[\d]+\.?[\d]+'))

    # ------ Лог

    def logTextEditSlot(self, text):
        if self.logTextEdit.toPlainText() == '':
            self.logTextEdit.setText(text)
        else:
            self.logTextEdit.setText(self.logTextEdit.toPlainText() + '\n' + text)

    # ----- Работа с оборудованием

    def screenshotSlot(self, path=None):
        self.mainGraphicsView.plotItem.vb.enableAutoRange(axis=pg.ViewBox.YAxis, enable=True)
        self.mainGraphicsView.plotItem.vb.enableAutoRange(axis=pg.ViewBox.XAxis, enable=True)

        p = self.mainGraphicsView.grab()

        if not path:
           date = datetime.datetime.now()

           path = QFileDialog.getExistingDirectory()
           path = path + '\\Screenshot_' + date.strftime('%Y-%m-%d_%H-%M.jpg')

           p.save(path, 'jpg')
        else:
            p.save(path + '.jpg', 'jpg')

    def EQU_refreshPushButtonClicked(self):
        dev = self.rm.list_resources()

        self.EQU_AN_addrComboBox.clear()
        self.EQU_GEN_addrComboBox.clear()
        self.EQU_PB5_addrComboBox.clear()
        self.EQU_PB48_addrComboBox.clear()

        self.EQU_AN_addrComboBox.addItems(dev)
        self.EQU_GEN_addrComboBox.addItems(dev)
        self.EQU_PB5_addrComboBox.addItems(dev)
        self.EQU_PB48_addrComboBox.addItems(dev)


        #p.save('src.jpg', 'jpg')

    def EQU_PB5_connectPushButtonClicked(self):

        self.pb5.ip = self.EQU_PB48_addrComboBox.currentText()
        self.pb5.connect()
        self.EQU_pb5StatusLabel.setText(self.pb5.fullName)

    def EQU_PB48_connectPushButtonClicked(self):

        self.pb48.ip = self.EQU_PB48_addrComboBox.currentText()
        self.pb48.connect()
        self.EQU_pb48StatusLabel.setText(self.pb48.fullName)

    def EQU_AN_connectPushButtonClicked(self):

        self.an = Analyzer()
        self.an.ip = self.EQU_AN_addrComboBox.currentText()

        try:
            self.an.connect()
        except:
            pass

        self.EQU_anStatusLabel.setText(self.an.fullName)

        if self.an.fullName and self.an.fullName != 'Error':
            self.EQU_AN_resetPushButton.setDisabled(False)
            self.EQU_AN_connectPushButton.setDisabled(True)
            self.EQU_AN_disconnectPushButton.setEnabled(True)

    def EQU_searchPushButtonClicked(self):
        self.searchDev()

    def EQU_AN_disconnectPushButtonClicked(self):
        if self.an:
            self.an.hAnalyzer = None
            self.an.fullName = None
            self.EQU_anStatusLabel.setText('Не подключен')

        self.EQU_AN_connectPushButton.setDisabled(False)
        self.EQU_AN_disconnectPushButton.setDisabled(True)
        self.EQU_AN_resetPushButton.setDisabled(True)

    def EQU_AN_resetPushButtonClicked(self):
        if self.an:
            if self.an.hAnalyzer:
                self.an.reset()

    def EQU_GEN_connectPushButtonClicked(self):

        if self.EQU_GEN_typeComboBox.currentText() == 'SMA100A':
            self.gen = Generator()
        elif self.EQU_GEN_typeComboBox.currentText() == 'Agilent N5182A':
            self.gen = helpGenerator()

        self.gen.ip = self.EQU_GEN_addrComboBox.currentText()

        self.gen.connect()

        self.EQU_GEN_statusLabel.setText(self.gen.fullName)
        self.EQU_GEN_resetPushButton.setDisabled(False)
        self.EQU_GEN_disconnectPushButton.setEnabled(True)

    def EQU_GEN_disconnectPushButtonClicked(self):
        if self.gen:
            self.gen.hGenerator = None
            self.gen.fullName = None
            self.EQU_GEN_statusLabel.setText('Не подключен')

        self.EQU_GEN_connectPushButton.setDisabled(False)
        self.EQU_GEN_disconnectPushButton.setDisabled(True)
        self.EQU_GEN_resetPushButton.setDisabled(True)

    def EQU_GEN_resetPushButtonClicked(self):
        if self.gen:
            self.gen.reset()

    # ----- Работа с устройством

    def DEV_connectPushButtonClicked(self):
        self.setPB(True)

    def DEV_disconnectPushButtonClicked(self):
        self.setPB(False)

    def DEV_setAttenPushButtonClicked(self):
        pass

    def DEV_getAttenPushButtonClicked(self):
        pass

    def DEV_getTempPushButtonClicked(self):
        pass

    def DEV_getStatusPushButtonClicked(self):
        pass

    def GET_get1FixCheckBoxChecked(self):

        if self.GET_get1FixCheckBox.isChecked():
            self.GET_get1lineEdit.setEnabled(True)
        else:
            self.GET_get1lineEdit.setEnabled(False)

    def GET_get2FixCheckBoxChecked(self):
        if self.GET_get2FixCheckBox.isChecked():
            self.GET_get2lineEdit.setEnabled(True)
        else:
            self.GET_get2lineEdit.setEnabled(False)


    def get_cmap(self, n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    # ----- Работа с тестами


    def readGain(self, file):
        gain_file = open(file, 'r')
        gain = {}

        flg = False
        for line in gain_file:
            line = line.replace('\n', '');
            line = line.replace('\t', ' ')

            if line == 'GAIN':
                flg = True
                continue

            if flg:
                line = line.replace('Freq: ', '');
                line = line.replace('Gain:', '');

                arr = [s for s in line.split(' ') if s != ' ' and s != '']

                if len(arr) == 2:
                    gain[round(float(arr[0]))] = float(arr[1])

        gain_file.close()


        return gain
        # ----

    def ATT_func(self):

        try:

            # рутина
            # когда нибудь автоматизирую ее

            beg = int(self.ATT_beginLineEdit.text())
            end = int(self.ATT_endLineEdit.text())
            step = int(self.ATT_stepLineEdit.text())
            level = float(self.ATT_levelLineEdit.text())


            att_beg = int(self.ATT_attBeginLineEdit.text())
            att_end = int(self.ATT_attEndLineEdit.text())
            att_step = int(self.ATT_attStepComboBox.currentText())


            gain_file = self.ATT_gainLineEdit.text()

            nominal_gain = self.AT_nominalGainCheckBox.isChecked()

            #et = self.ATT_enCheckBox.isChecked()

            # --- инициализация графиков

            col = ['r', 'g', 'b', 'y', 'c', 'm']




            sch = -1

            data = range(att_beg, att_end + 1, att_step)

            _cmap = self.get_cmap(len(data))

            g = []

            for i in range(len(data)):
                sch = sch + 1
                g.append(MPL_Plot())
                g[sch].col = col[sch]
                g[sch].title = 'Значение подавления по атт.: ' + str(data[i]) + ' dB'
                g[sch].y.append([])
                #g[sch].x = []

            # --- эталон

            """
            if et:
                _g = MPL_Plot()
                _g.col = 'k'
                _g.title = 'Эталон, 0 dB'
                _g.y.append([])

                g = [_g ] + g
            """



            # ----


            g[0].xlabel = 'Частота перестройки, MHz'
            g[0].ylabel = 'Подавление сигнала, dB'
            g[0].zlabel = None

            # -----

            # --- логи

            calFlg = self.CAL_calibEnableCheckBox.isChecked()

            path = self.manResFileDirLineEdit.text() + '\\'
            name = str(int(beg)) + '_' + str(int(end)) + 'MHz'
            name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_ATT_' + name

            if self.TEST_devTypeComboBox.currentText() == 'Панорама':
                self.dev = self.pan

            # ---

            self.att.setParams(beg, end, step,
                               None, level,
                               self.gen, self.an,
                               self.dev,
                               color=self.colorComboBox.currentText(),
                               logfile=name,
                               cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                               user=[att_beg, att_end, att_step, self.readGain(gain_file), g,nominal_gain])

            self.logProgressBar.setMaximum(end)
            self.logProgressBar.setMinimum(beg)

            self.MPL_additGraphicsView.initGraphSlot(1)
            self.MPL_additGraphicsView.enableGridGraph(True)
            self.MPL_additGraphicsView.plotGraphSlot(g, True, 'Глубина регулировки коэффициента передачи и шаг регулировки коэффициента передачи конвертера')
            self.MPL_additGraphicsView.invertAxis('y')


            self.att.start()

        except:
            raise
            pass

    def SIF_func(self):

        try:
            beg =   int(self.SIF_beginLineEdit.text())
            end =   int(self.SIF_endLineEdit.text())
            step =  int(self.SIF_stepLineEdit.text())
            level = float(self.SIF_levelLineEdit.text())

            _if = []

            if self.SIF_if1checkBox.isChecked():
                _if.append(int(self.SIF_if1lineEdit.text()))

            if self.SIF_if2checkBox.isChecked():
                _if.append(int(self.SIF_if2LineEdit.text()))

            if self.SIF_if3checkBox.isChecked():
                _if.append(int(self.SIF_if3lineEdit.text()))

            col = ['r', 'g', 'b', 'y', 'c', 'k']
            sch = -1

            # ----

            gain_file = open(self.NF_gainLineEdit.text(), 'r')
            gain = {}

            flg = False
            for line in gain_file:
                line = line.replace('\n', '');
                line = line.replace('\t', ' ')

                if line == 'GAIN':
                    flg = True
                    continue

                if flg:
                    line = line.replace('Freq: ', '');
                    line = line.replace('Gain:', '');

                    arr = [s for s in line.split(' ') if s != ' ' and s != '']

                    if len(arr) == 2:
                        gain[round(float(arr[0]))] = float(arr[1])

            gain_file.close()

            # ----


            g = []

            for i in range(len(_if)):
                sch = sch + 1
                g.append(MPL_Plot())
                g[i].col = col[sch]
                g[i].title = 'Подавление ПЧ по значению: ' + str(_if[i]) + ' MHz'
                g[i].y.append([])

            g[0].xlabel = 'Частота перестройки, MHz'
            g[0].ylabel = 'Подавление ПЧ , dB'
            g[0].zlabel = None

            # --- логи

            calFlg = self.CAL_calibEnableCheckBox.isChecked()

            path = self.manResFileDirLineEdit.text() + '\\'
            name = str(int(beg)) + '_' + str(int(end)) + 'MHz'
            name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_SIF_' + name

            if self.TEST_devTypeComboBox.currentText() == 'Панорама':
                self.dev = self.pan

            # ---

            self.sif.setParams(beg, end, step,
                              None, level,
                              self.gen, self.an,
                              self.dev,
                              color=self.colorComboBox.currentText(),
                              logfile=name,
                              cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                              user=[_if, g, gain])

            self.logProgressBar.setMaximum(end)
            self.logProgressBar.setMinimum(beg)

            self.MPL_additGraphicsView.initGraphSlot(1)
            self.MPL_additGraphicsView.plotGraphSlot(g, True, 'Подавление сигнала ПЧ')

            self.sif.start()

        except:
            raise
            self.showErr('Неверные параметры теста!')


    def NF_func(self):

        beg = int(self.NF_beginLineEdit.text())
        end = int(self.NF_endLineEdit.text())
        step = int(self.NF_stepLineEdit.text())
        span = int(self.NF_spanLineEdit.text())

        # -----

        g = MPL_Plot()

        g.y.append([])

        g.col = 'r'
        g.title = 'Коэффициент шума'
        g.y.append([])

        g.xlabel = 'Частота перестройки, MHz'
        g.ylabel = 'NF'
        g.zlabel = None

        # -----
        gain_file = open(self.NF_gainLineEdit.text(), 'r')
        gain = {}

        flg  = False
        for line in gain_file:
            line = line.replace('\n', ''); line = line.replace('\t', ' ')

            if line == 'GAIN':
                flg = True
                continue

            if flg:
                line = line.replace('Freq: ', '');
                line = line.replace('Gain:', '');

                arr = [s for s in line.split(' ') if s != ' ' and s != '']

                if len(arr) == 2:
                    gain[round(float(arr[0]))] = float(arr[1])

        gain_file.close()

        # -----

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        path = self.manResFileDirLineEdit.text() + '\\'
        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'
        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_NF_' + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        # -----

        self.nf.setParams(beg, end, step,
                          None, None,
                          self.gen, self.an,
                          self.dev,
                          color=self.colorComboBox.currentText(),
                          logfile=name,
                          span=span,
                          cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                          user=[gain, g])

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.MPL_additGraphicsView.initGraphSlot(1)
        self.MPL_additGraphicsView.plotGraphSlot([g], True, 'Коэффициент шума')

        self.nf.start()

    def PN_func(self):

        beg = int(self.PN_beginLineEdit.text())
        end = int(self.PN_endLineEdit.text())
        step = int(self.PN_stepLineEdit.text())
        level = float(self.PN_levelLineEdit.text())
        rbw = float(self.PN_rwbLineEdit.text())
        _span = []

        # ------------------------------------------------

        g = []

        """
        g.append(MPL_Plot())
        g[0].title = 'Фазовый шум'
        g[0].xlabel = 'Частота перестройки, MHz'
        g[0].ylabel = 'Фазовый шум, dBc/Hz'
        g[0].zlabel = None

        for i in range(len(_span)):
            g[0].y.append([])
        """
        # ---------------------------------------------------


        if self.PN_10MHzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (10, 'MHz')
            tmp.span = (25, 'MHz')
            tmp.rbw =  (1,  'MHz')
            _span.append(tmp)

        if self.PN_1MHzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (1,  'MHz')
            tmp.span = (3,  'MHz')
            tmp.rbw =  (100, 'kHz')
            _span.append(tmp)

        if self.PN_100kHzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (100, 'kHz')
            tmp.span = (1,   'MHz')
            tmp.rbw =  (30,  'kHz')
            _span.append(tmp)

        if self.PN_10kHzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (10,  'kHz')
            tmp.span = (100, 'kHz')
            tmp.rbw =  (3,   'kHz')
            _span.append(tmp)

        if self.PN_1kHzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (1, 'kHz')
            tmp.span = (2.5, 'kHz')
            tmp.rbw =  (100, 'Hz')
            _span.append(tmp)

        if self.PN_100HzcheckBox.isChecked():
            tmp = pn_params()
            tmp.mkr =  (100, 'Hz')
            tmp.span = (300, 'Hz')
            tmp.rbw =  (30, 'Hz')
            _span.append(tmp)

        col = ['r', 'g', 'b', 'y', 'c', 'k']
        sch = -1



        for i in range(len(_span)):
            sch = sch + 1
            g.append(MPL_Plot())
            g[i].col = col[sch]
            g[i].title = 'Фазовый шум по маркеру ' + str(_span[i].mkr[0]) + ' ' + str(_span[i].mkr[1])
            g[i].y.append([])

        g[0].xlabel = 'Частота перестройки, MHz'
        g[0].ylabel = 'Фазовый шум, dBc/Hz'
        g[0].zlabel = None






        self.MPL_additGraphicsView.initGraphSlot(1)
        self.MPL_additGraphicsView.plotGraphSlot(g, True, 'Фазовые шумы')


        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        path = self.manResFileDirLineEdit.text() + '\\'
        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'
        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_PN_' + name

        if not _span:
            self.showErr('Не выбрано ничего!')



        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan






        self.pn.setParams(beg, end, step,
                          None, level,
                          self.gen, self.an,
                          self.dev,
                          color=self.colorComboBox.currentText(),
                          logfile=name,
                          cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                          user=[_span, rbw, g])

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.pn.start()

    def BW_func(self):

        beg = int(self.BW_freqBeginLineEdit.text())
        end = int(self.BW_freqEndLineEdit.text())
        space = int(self.BW_spaceLineEdit.text())
        level = float(self.BW_levelLineEdit.text())
        step_f = int(self.BW_stepComboBox.currentText())
        step_space = int(self.BW_spaceComboBox.currentText())

        specFlg = self.BW_specCheckBox.isChecked()


        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        path = self.manResFileDirLineEdit.text() + '\\'
        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'
        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_BW_' + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        #self.MPL_graphicsView.setTitleSpec('Test')

        self.MPL_graphicsView.initLabels('Смещение относительно частоты подстройки',
                                            'Частота подстройки',
                                            'Полоса пропускания')



        self.bw.setParams(beg, end, step_f, None, level,
                          self.gen, self.an, self.dev,
                          self.colorComboBox.currentText(),
                          cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                          plot_flg=self.realPlotCheckBox.isChecked(),
                          logfile=name, path=path,
                          user=[space, step_space, [specFlg]]
                          )

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.bw.start()


    def EFF_func(self):

        self.mainGraphicsView.plotItem.setLabels(title='КПД', left='Eff, %', bottom='Pin, dBm')

        name = time.ctime(time.time())
        name = name.replace(' ', '-')
        name = name.replace(':', '-')

        name = self.manResFileDirLineEdit.text() + '\\' + 'EFF_' + name + '.txt'

        if not self.pb48_ip:
            self.showErr('Отсутствует БП!')
            return

        freq = float(self.TST_EFF_freqLineEdit.text())
        beg = float(self.TST_EFF_levelBeginLineEdit.text())
        end = float(self.TST_EFF_levelEndLineEdit.text())
        step = float(self.TST_EFF_stepLineEdit.text())
        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        self.eff.setParams(beg, end, step, freq, None, self.gen, self.an, None,
                           self.colorComboBox.currentText(),
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                           pb=self.pb48,
                           logfile=name,
                           plot_flg=self.realPlotCheckBox.isChecked())

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.eff.start()

    def PIO_func(self):

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        if not calFlg or not self.cal_in:
            self.showErr('Данный тест не имеет смысла без наличия калибровки!')
            return

        freq = float(self.TST_PIO_freqLineEdit.text())
        beg = float(self.TST_PIO_levelBeginLineEdit.text())
        end = float(self.TST_PIO_levelEndLineEdit.text())
        step = float(self.TST_PIO_stepLineEdit.text())

        self.mainGraphicsView.plotItem.setLabels(title='PIO', left='Выходная мощность, dBm',
                                                 bottom='Входная мощность, dBm')

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan
            pan = True

        name = str(int(beg)) + '_' + str(int(end)) + 'dBm_' + str(int(freq)) + 'MHz'
        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_PIO_' + name

        self.pio.setParams(beg, end, step, freq, None, self.gen, self.an, self.dev,
                           self.colorComboBox.currentText(),
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                           plot_flg=self.realPlotCheckBox.isChecked(),
                           logfile=name,
                           user= [self.TST_PIO_getInFileLineEdit.text(), False, pan, self.TEST_devTypeComboBox.currentText()])

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.pio.start()

    def POC_func(self):
        beg_f = float(self.TST_POC_freqBeginLineEdit.text())
        end_f = float(self.TST_POC_freqEndLineEdit.text())
        step_f = float(self.TST_POC_stepFreqLineEdit.text())
        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        beg_l = float(self.TST_POC_levelBeginLineEdit.text())
        end_l = float(self.TST_POC_levelEndLineEdit.text())
        step_l = float(self.TST_POC_stepLevelLineEdit.text())

        name = str(int(beg_f)) + '_' + str(int(end_f)) + 'MHz'

        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_P1dB_' + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.mainGraphicsView.plotItem.setLabels(title='PxdB', left='PxdB, dBm', bottom='Частота, MHz')

        if not calFlg or not self.cal_in:
            self.showErr('Данный тест не имеет смысла без наличия калибровки!')
            return

        file = self.POC_getInFileLineEdit.text()

        self.logProgressBar.setMaximum(end_f)
        self.logProgressBar.setMinimum(beg_f)

        self.poc.setParams(beg_f, end_f, step_f, None, None, self.gen, self.an, self.dev,
                           self.colorComboBox.currentText(),
                           plot_flg=self.realPlotCheckBox.isChecked(),
                           logfile=name,
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                           user=[beg_l, end_l, step_l, file, self.TEST_devTypeComboBox.currentText()])

        self.poc.start()

    def UD_func(self):

        level = float(self.TST_UD_levelLineEdit.text()) # +
        beg = float(self.TST_UD_begLineEdit.text())     # +
        end = float(self.TST_UD_endLineEdit.text())     # +
        count = float(self.TST_UD_countLineEdit.text()) # +
        span = int(self.TST_UD_spanLineEdit.text())     # +
        time = float(self.TST_UD_timeLineEdit.text())   # +

        name = self.manResFileDirLineEdit.text() + '\\' # +

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.ud.setParams(beg, end, None, None, level,
                          self.gen, self.an, self.dev,
                          None,
                          logfile=name,
                          user=[count, span, time])

        self.logProgressBar.setMaximum(count)
        self.logProgressBar.setMinimum(0)

        self.ud.start()
    def GET_func(self):

        beg = int(self.GET_beginLineEdit.text())
        end = int(self.GET_endLineEdit.text())
        step = int(self.GET_stepLineEdit.text())

        get1_fix = self.GET_get1FixCheckBox.isChecked()
        get1_freq = float(self.GET_get1lineEdit.text())


        get2_en = self.GET_get2CheckBox.isChecked()
        get2_fix = self.GET_get2FixCheckBox.isChecked()

        if get2_en and get2_fix:
            get2_freq = float(self.GET_get2lineEdit.text())
        else:
            get2_freq = None



        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        i_o = self.GET_outCheckBox.isChecked()

        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'

        if i_o: #если по выходу
            name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_GET_OUT_' + name
        else:
            name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_GET_IN_' + name



        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan


        self.get.setParams(beg, end, step, None, None,
                           None, self.an, self.dev,
                           self.colorComboBox.currentText(),
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                           plot_flg=self.realPlotCheckBox.isChecked(),
                           logfile=name,
                           user=[i_o, get1_fix, get1_freq, get2_en, get2_fix, get2_freq])

        self.get.start()

        #self.mainGraphicsView.plotItem.setLabels(title='Мо', left='Амлитуда, dBm', bottom='Частота, MHz')

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

    def MIRR_func(self):
        self.mainGraphicsView.plotItem.setLabels(title='Зеркальные частоты', left='Подавление, dB', \
                                                 bottom='Частота настройки, MHz')

        level = float(self.MIRR_levelLineEdit.text())

        beg = int(self.MIRR_beginLineEdit.text())

        end = int(self.MIRR_endLineEdit.text())

        step = [int(self.MIRR_freqStepLineEdit.text()),int(self.MIRR_setStepLineEdit.text())]

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'

        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_MIRR_' + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan


        self.MPL_additGraphicsView.init3Dslot()

        self.mirr.setParams(beg, end, step, None, level,
                            self.gen, self.an, self.dev,
                            self.colorComboBox.currentText(),
                            cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                            plot_flg=self.realPlotCheckBox.isChecked(),
                            logfile=name,
                            )

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.mirr.start()

    def AFC_func(self):

        self.mainGraphicsView.plotItem.setLabels(title='АЧХ', left='Амлитуда, dBm', bottom='Частота, MHz')

        level = float(self.TST_AFC_levelLineEdit.text())
        beg = float(self.TST_AFC_freqBeginLineEdit.text())
        end = float(self.TST_AFC_freqEndLineEdit.text())
        step = float(self.TST_AFC_stepLineEdit.text())
        calFlg = self.CAL_calibEnableCheckBox.isChecked()
        path = self.manResFileDirLineEdit.text() + '\\'


        name = str(int(beg)) + '_' + str(int(end)) + 'MHz'

        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + '_FR_' + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.afc.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                           self.colorComboBox.currentText(),
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                           plot_flg=self.realPlotCheckBox.isChecked(),
                           logfile=name,path=path,
                           user=[self.TEST_devTypeComboBox.currentText(), self.manResFileDirLineEdit.text(), self.AFC_bwCheckBox.isChecked(), self.AFC_noiseCheckBox.isChecked(),
                           self.AFC_noiseSpanLineEdit.text(), self.AFC_noiseTheLineEdit.text()])

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.afc.start()

    def IMD_func(self):
        self.mainGraphicsView.plotItem.setLabels(title='IMD', left='None', bottom='None')

        if self.gen.type != 'N5182A':
            self.showErr('Данный генератор не поддерживает двухтоновый сигнал!')
            return

        beg = float(self.TST_IMD_freqBeginLineEdit.text())
        end = float(self.TST_IMD_freqEndLineEdit.text())
        step = float(self.TST_IMD_stepLineEdit.text())
        level = float(self.TST_IMD_levelLineEdit.text())
        sep = float(self.TST_IMD_sepLineEdit.text())
        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.imd.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                           self.colorComboBox.currentText(),
                           cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out, user=sep)



        self.imd.start()

    def GAIN_func(self):
        self.mainGraphicsView.plotItem.setLabels(title='Усиление', left='Усиление, dBm', bottom='Частота, MHz')

        level = float(self.TST_GAIN_levelLineEdit.text())
        beg = float(self.TST_GAIN_freqBeginLineEdit.text())
        end = float(self.TST_GAIN_freqEndLineEdit.text())
        step = float(self.TST_GAIN_stepFreqLineEdit.text())
        path = self.manResFileDirLineEdit.text() + '\\'

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        name = '_GAIN_' + str(int(beg)) + '_' + str(int(end)) + 'MHz'
        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + name

        user = [None, name, self.TEST_devTypeComboBox.currentText()]



        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.gain.setParams(beg, end, step, None, level, self.gen, self.an, self.dev,
                            self.colorComboBox.currentText(),
                            cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
                            plot_flg=self.realPlotCheckBox.isChecked(),
                            logfile=name,
                            user=user, path=path)

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.gain.start()

    def ACC_func(self):
        self.mainGraphicsView.plotItem.setLabels(title='Точность подстройки',
                                                 left='Отношение REF и DELTA, ppb', bottom='Частота, MHz')

        beg = float(self.TST_ACC_freqBeginLineEdit.text())
        end = float(self.TST_ACC_freqEndLineEdit.text())
        span = float(self.TST_ACC_spanLineEdit.text())
        path = self.manResFileDirLineEdit.text() + '\\'
        level = int(self.TST_ACC_levelLineEdit.text())

        name = '_ACC_' + str(int(beg)) + '_' + str(int(end)) + 'MHz' + '_SPAN_' + str(span) + 'MHz'

        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.acc.setParams(
            beg, end, None, None, level, self.gen, self.an, self.dev,
            self.colorComboBox.currentText(),
            plot_flg=self.realPlotCheckBox.isChecked(),
            logfile=name,
            user=[self.TEST_devTypeComboBox.currentText(), self.manResFileDirLineEdit.text()],
            span=span, path=path
        )

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.acc.start()

    def BF_func(self):
        self.mainGraphicsView.plotItem.setLabels(title='Пораженные частоты')

        beg = float(self.TST_BF_freqBeginLineEdit.text())
        end = float(self.TST_BF_freqEndLineEdit.text())
        step = float(self.TST_BF_stepLineEdit.text())
        span = int(self.TST_BF_spanLineEdit.text())
        threshold = float(self.TST_BF_thresholdLineEdit.text())
        path = self.manResFileDirLineEdit.text() + '\\'

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        name = '_BF_' + str(int(beg)) + '_' + str(int(end)) + 'MHz' + '_SPAN_' + str(span) + 'MHz'

        name = self.manResFileDirLineEdit.text() + '\\' + self.TEST_devTypeComboBox.currentText() + name

        if self.TEST_devTypeComboBox.currentText() == 'Панорама':
            self.dev = self.pan

        self.bf.setParams(
            beg, end, step, None, None, None, self.an, self.dev,
            self.colorComboBox.currentText(),
            cal_flg=calFlg, cal_in=self.cal_in, cal_out=self.cal_out,
            plot_flg=self.realPlotCheckBox.isChecked(),
            logfile=name,
            user=[self.TEST_devTypeComboBox.currentText(), self.manResFileDirLineEdit.text()],
            span=span, threshold=threshold, path=path
        )

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.bf.start()

    # ----- Работа с кнопками управления

    def testTabWidgetSlot(self, val):

        if val == 0:
            self.currTestLabel.setText('АЧХ')
        if val == 1:
            self.currTestLabel.setText('Усиление')
        if val == 2:
            self.currTestLabel.setText('Входная-выходная мощность')
        if val == 3:
            self.currTestLabel.setText('PxdB')
        if val == 4:
            self.currTestLabel.setText('КПД')
        if val == 5:
            self.currTestLabel.setText('IMD')
        if val == 6:
            self.currTestLabel.setText('Пораженные частоты')
        if val == 7:
            self.currTestLabel.setText('Точность подстройки')
        if val == 8:
            self.currTestLabel.setText('UP-DOWN')
        if val == 9:
            self.currTestLabel.setText('Мощность сигнала гет.')
        if val == 10:
            self.currTestLabel.setText('Полоса пропускания')
        if val == 11:
            self.currTestLabel.setText('Побочные каналы')
        if val == 12:
            self.currTestLabel.setText('Фазовые шумы')
        if val == 13:
            self.currTestLabel.setText('Коэф. шума')
        if val == 14:
            self.currTestLabel.setText('Подавление сигнала ПЧ')
        if val == 15:
            self.currTestLabel.setText('Глубина регулировки КП')

    def startTestPushButtonClicked(self):

#        test = self.testSelectComboBox.currentText()

        calFlg = self.CAL_calibEnableCheckBox.isChecked()

        if calFlg and not self.cal_in:
            #self.showErr('Отсутствует файл калибровки!')
            pass
          #return

        if not self.an:
            #self.showErr('Отсутствует генератор!')
            pass
            #return

        if not self.gen:
            #self.showErr('Отсутствует анализатор!')
            pass
          #  return

        if self.testTabWidget.currentIndex() == 0:
            self.AFC_func()
        if self.testTabWidget.currentIndex() == 1:
            self.GAIN_func()
        if self.testTabWidget.currentIndex() == 2:
            self.PIO_func()
        if self.testTabWidget.currentIndex() == 3:
            self.POC_func()
        if self.testTabWidget.currentIndex() == 4:
            self.EFF_func()
        if self.testTabWidget.currentIndex() == 5:
            self.IMD_func()
        if self.testTabWidget.currentIndex() == 6:
            self.BF_func()
        if self.testTabWidget.currentIndex() == 7:
            self.ACC_func()
        if self.testTabWidget.currentIndex() == 8:
            self.UD_func()
        if self.testTabWidget.currentIndex() == 9:
            self.GET_func();
        if self.testTabWidget.currentIndex() == 10:
            self.BW_func()
        if self.testTabWidget.currentIndex() == 11:
            self.MIRR_func()
        if self.testTabWidget.currentIndex() == 12:
            self.PN_func()
        if self.testTabWidget.currentIndex() == 13:
            self.NF_func()
        if self.testTabWidget.currentIndex() == 14:
            self.SIF_func()
        if self.testTabWidget.currentIndex() == 15:
            self.ATT_func()
        else:
            return

    def traySlot(self, title, message):
        self.tray.showMessage(title, message)

    def clearLogPushButtonClicked(self):
        self.logTextEdit.clear()
        self.mainGraphicsView.plotItem.clear()

        self.MPL_graphicsView.initSpecSlot()
        self.MPL_additGraphicsView.initGraphSlot(0)

    def stopTestPushButtonClicked(self):
        pass

        #self.traySlot('Title', 'Message')


        self.tray.showMessage("Titile", "text")

    # ----- Работа с калибровкой

    def CAL_getFilePushButtonClicked(self):
        file_cal_in = open(self.CAL_getInFileLineEdit.text(), 'r')
        file_cal_out = open(self.CAL_getOutFileLineEdit.text(), 'r')

        self.cal_in = {}
        self.cal_out = {}

        for line in file_cal_in:
            key, val = line.split()
            self.cal_in[int(key)] = float(val)

        for line in file_cal_out:
            key, val = line.split()
            self.cal_out[int(key)] = float(val)

        self.logTextEditSlot('Файлы калибровки успешно считаны!')
        print('Файлы калибровки успешно считаны!')

    def CAL_selectInFilePushButtonClicked(self):
        self.CAL_getInFileLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def CAL_selectOutFilePushButtonClicked(self):
        self.CAL_getOutFileLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def CAL_startPushButtonClicked(self):

        step = float(self.calibrStepLineEdit.text())
        level = float(self.calibrLevelLineEdit.text())
        beg = float(self.calibrFreqBeginLineEdit.text())
        end = float(self.calibrFreqEndLineEdit.text())
        typ = self.CAL_calibrTypeComboBox.currentText()

        self.logProgressBar.setMaximum(end)
        self.logProgressBar.setMinimum(beg)

        self.cal_test.setParams(beg, end, step, None, level, self.gen, self.an, self.dev, None, type=typ,
                                logfile=self.CAL_getFileLineEdit.text())

        self.cal_test.start()


def start():
    app = QtGui.QApplication(sys.argv)

    mv = MW()

    mv.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    start()