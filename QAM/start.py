# ---- обработка исключений

from structs import IQData_arr

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))


    print('\n\n-------------------------------------------- \n')
    print(text)
    print('\n----------------------------------------------\n')


import sys
sys.excepthook = log_uncaught_exceptions

# ------ системные импорты

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time

# ----- пользовательские импорты

from mainwindow import Ui_MainWindow
from FileReader import FileReader
from structs import IQData
from ThreadReader import ThreadReader

# ----- класс формы

class MW(QtWidgets.QMainWindow, Ui_MainWindow):

    # -----



    # -----


    def __init__(self):
        super(MW, self).__init__()

        self.setupUi(self)
        self.setCentralWidget(self.cw)

        # -----

        self.initSignals()

        self.chan_cnt = 0
        self.plot_flg = False
        self.time = 0

        # ---

        self.fr = FileReader()
        self.fr.plot_signal.connect(self.dataSlot)
        self.fr.end_signal.connect(self.endSlot)
        self.RD_stopFilePushButton.clicked.connect(self.fr.stop)



        self.tr = ThreadReader()
        self.tr.plot_signal.connect(self.dataSlot)
        self.tr.end_signal.connect(self.endSlot)
        self.tr.log_signal.connect(self.logSlot)
        self.TR_stopFilePushButton.clicked.connect(self.tr.stop)


        # --- данные класса

        self.data_len = self.clearSlider.value()

        self.points_arr = IQData_arr()


        self.clearSliderValueChanged()
        self.updateSliderValueChanged()
        #self.showFullScreen()


        # к-к-костыли!
        #time.sleep(1)
        self.hist.figure.tight_layout()


        # --- режимы работы
        self.mode = 0
        self.updateMode()
        self.viePushButtonClicked()
        self.setColorPushButtonClicked()
    def ishChanComboBoxStateChanged(self):

        if self.mode == 2:
            self.setLabels(self.mode)

            # указываем нужный нам канал
            chan_n = int(self.ampChanComboBox.currentText())
            self.hist.setChan(chan_n)
            self.diag.setChan(chan_n)
    def updateMode(self):

        amp_flg = self.FR_ampCheckBox.isChecked()
        delta_flg = self.TR_deltaCheckBox.isChecked()

        if amp_flg: # отображение только амплитуды по выбранному каналу
            self.mode = 3

            # отключаем разницу каналов
            #self.TR_deltaCheckBox.setEnabled(False)


            #выставляем  режим
            self.diag.setMode(self.mode)
            self.hist.setMode(self.mode)

            #указываем сколько нам нужно графиков на гистограмме
            self.hist.setCount(1)

            # выставляем писюльки
            self.setLabels(self.mode)

            #указываем нужный нам канал
            chan_n = int(self.ampChanComboBox.currentText())
            self.hist.setChan(chan_n)
            self.diag.setChan(chan_n)

        else:
            #self.TR_deltaCheckBox.setEnabled(True)

            if delta_flg:
                self.mode = 2

                self.diag.setMode(self.mode)
                self.hist.setMode(self.mode)

                self.hist.setCount(self.chan_cnt - 1)

                self.diag.setChan(int(self.ishChanComboBox.currentText()))
                self.hist.setChan(int(self.ishChanComboBox.currentText()))

                self.setLabels(self.mode)

            else:
                self.mode = 1

                self.diag.setMode(self.mode)
                self.hist.setMode(self.mode)

                self.hist.setCount(self.chan_cnt)

                self.setLabels(self.mode)

        self.viePushButtonClicked()






    def TR_offsetCheckBoxStateChanged(self):
        self.tr.setOffsFlag(self.TR_offsetCheckBox.isChecked())



    def initSignals(self):

        self.ishChanComboBox.currentIndexChanged.connect(self.ishChanComboBoxStateChanged)
        self.TR_offsetCheckBox.stateChanged.connect(self.TR_offsetCheckBoxStateChanged)
        self.ampChanComboBox.currentIndexChanged.connect(self.ampChanComboBoxCurrentIndexChanged)
        self.TR_startFilePushButton.clicked.connect(self. TR_startFilePushButtonClicked)

        self.FR_ampCheckBox.stateChanged.connect(self.updateMode)
        self.TR_deltaCheckBox.stateChanged.connect(self.updateMode)

        self.setColorPushButton.clicked.connect(self.setColorPushButtonClicked)
        self.updateSlider.valueChanged.connect(self.updateSliderValueChanged)
        self.clearSlider.valueChanged.connect(self.clearSliderValueChanged)
        self.clearPointPushButton.clicked.connect(self.clearPointPushButtonClicked)
        self.viePushButton.clicked.connect(self.viePushButtonClicked)
        self.clearPushButton.clicked.connect(self.clearSlot)
        self.readFilePushButton.clicked.connect(self.readFilePushButtonClicked)
        self.RD_startFilePushButton.clicked.connect(self.RD_startFilePushButtonClicked)

    def setColorPushButtonClicked(self):
        self.diag.setCmap(self.colorComboBox.currentText())
        self.hist.setCmap(self.colorComboBox.currentText())

        self.logSlot('Успешно.')


    def setLabels(self, mode=1):
        if mode  == 1:
            self.diag.setLabels('Расположение точек', None, None)

            self.hist.setAllLabels(None, 'Коорд. точек', 'Кол-во точек')
            for i in range(0, len(self.points_arr.getChans())):
                self.hist.setLabels(i, title='Канал #' + str(i))

        elif mode == 2:

            self.diag.setLabels('Расположение точек', None, None)

            chan_n = int(self.ishChanComboBox.currentText())


            sch = -1
            self.hist.setAllLabels(None, 'Коорд. точек', 'Кол-во точек')
            for i in range(0, len(self.points_arr.getChans())):
                if i == chan_n:
                    continue
                else:
                    sch = sch + 1
                    self.hist.setLabels(sch, title='Разница канала #' + str(chan_n) + ' и #' + str(i))

        elif mode == 3:
            chan_n = int(self.ampChanComboBox.currentText())
            self.diag.setLabels('Расположение точек', 'Амплитуда', None)

            self.hist.setAllLabels('Канал #' + str(chan_n), 'Коорд. точек', 'Кол-во точек')





    def ampChanComboBoxCurrentIndexChanged(self):
        chan_n = int(self.ampChanComboBox.currentText())

        self.hist.setChan(chan_n)
        self.diag.setChan(chan_n)

    def updateSliderValueChanged(self):
        self.updateLabel.setText(str(self.updateSlider.value()))

    def clearSliderValueChanged(self):
        self.clearLabel.setText(str(self.clearSlider.value()))

    def clearPointPushButtonClicked(self):

        _tout = self.updateSlider.value()
        _len = int(self.clearSlider.value())

        self.tr.setUpdateTime(_tout)
        self.points_arr.setSize(_len)
        #self.data_len = val

        self.logSlot('Успешно.')

    def viePushButtonClicked(self):


        try:
            _min = int(self.vieMinLineEdit.text())
            _max = int(self.vieMaxLineEdit.text())
        except:
            self.showErr('Недопустимые значения!')
            return

        flg = False

        if _min >= _max:
            flg = True

        if _min < 0:
            flg = True

        if _max > 360:
            flg = True


        if flg:
            self.showErr('Недопустимые значения!')
            return


        self.diag.setViev([_min, _max])
        self.hist.setViev([_min, _max])

        #self.MPL_hist.rangeHist(_min, _max)
        #self.MPL_diag.rangeDiag(_min, _max)
        #self.MPL_hist.rangeColor(_min, _max)
        #self.MPL_diag.rangeColor(_min, _max)
        self.logSlot('Успешно.')

    def readFilePushButtonClicked(self):
        self.readFileLineEdit.setText(QFileDialog.getOpenFileName()[0])


    def TR_startFilePushButtonClicked(self):

        _tout = int(self.updateSlider.value())
        _endian = self.endianComboBox.currentText()
        _dll = 'pshow_get.dll'


        self.logSlot('Запуск...')

        self.tr.setParams(_dll, _endian,_tout)

        self.clearPointPushButtonClicked()

        #self.points_arr.setSize(100)

        ret = self.tr.connectDLL()

        if ret:
            self.showErr('Невозможно подключить DLL библиотеку!')
            self.logSlot('Ошибка.')
            return

        self.tr.start()



    def RD_startFilePushButtonClicked(self):

        _tout = int(self.updateSlider.value())

        if self.RD_emulateCheckBox.isChecked():
            pass
        else:
            _tout = None

        _endian = self.endianComboBox.currentText()

        _file = self.readFileLineEdit.text()

        self.viePushButtonClicked()

        self.logSlot('Запуск...')

        self.fr.setParams(_file, _endian, _tout)

        self.fr.start()

    # ----- служебки

    def showErr(self, text):
        QMessageBox.critical(self, 'Ошибка!', text)


    def logSlot(self, text):
        if self.logTextEdit.toPlainText() == '':
            self.logTextEdit.setText(text)
        else:
            self.logTextEdit.setText(self.logTextEdit.toPlainText() + '\n' + text)

    def dataSlot(self, val):

        self.points_arr.addPoints(val)

        if len(self.points_arr.getChans()) != self.chan_cnt:
            self.chan_cnt =  len(self.points_arr.getChans())
            self.updateMode()

        if not self.plot_flg:
            self.plot_flg = True
            self.diag.plotDiag(self.points_arr)
            self.hist.plotHist(self.points_arr)
            self.plot_flg = False


    def clearSlot(self):
        self.points_arr.clearPoints()



    def endSlot(self, val):

        self.logSlot('Остановлено..')
        self.logSlot('Обработано точек: ' + str(val))

def start():

    app = QtWidgets.QApplication(sys.argv)

    mv = MW()

    mv.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    start()