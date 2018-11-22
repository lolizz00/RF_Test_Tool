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
        self.preInitPlots()


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

        self.data = []
        self.data_len = self.clearSlider.value()

        self.points_arr = IQData_arr()

        self.viePushButtonClicked()
        self.clearSliderValueChanged()
        self.updateSliderValueChanged()
        #self.showFullScreen()


    def FR_ampCheckBoxstateChanged(self):
        if self.FR_ampCheckBox.isChecked():
            self.MPL_diag.initDiagSlot(amp=True)
            self.MPL_diag.setDiagLables('Расположение точек', None, None)
        else:
            self.MPL_diag.initDiagSlot(amp=False)
            self.MPL_diag.setDiagLables('Расположение точек', 'I', 'Q')



    def initSignals(self):
        self.TR_startFilePushButton.clicked.connect(self. TR_startFilePushButtonClicked)
        self.FR_ampCheckBox.stateChanged.connect(self.FR_ampCheckBoxstateChanged)
        self.setColorPushButton.clicked.connect(self.setColorPushButtonClicked)
        self.updateSlider.valueChanged.connect(self.updateSliderValueChanged)
        self.clearSlider.valueChanged.connect(self.clearSliderValueChanged)
        self.clearPointPushButton.clicked.connect(self.clearPointPushButtonClicked)
        self.viePushButton.clicked.connect(self.viePushButtonClicked)
        self.clearPushButton.clicked.connect(self.clearSlot)
        self.readFilePushButton.clicked.connect(self.readFilePushButtonClicked)
        self.RD_startFilePushButton.clicked.connect(self.RD_startFilePushButtonClicked)

    def setColorPushButtonClicked(self):
        self.MPL_diag.setCmap(self.colorComboBox.currentText())
        self.MPL_hist.setCmap(self.colorComboBox.currentText())

        self.logSlot('Успешно.')

    def preInitPlots(self):

        # ---- Инициализация гистограммы

        self.MPL_hist.initHistSlot()
        self.MPL_hist.setHistLables('Распределение кол-ва точек', 'Коорд. точек', 'Кол-во точек')
        self.MPL_hist.enableGridHist(True)


        # ----- Иницициализация кружочка

        self.MPL_diag.initDiagSlot()
        self.MPL_diag.setDiagLables('Расположение точек', None, None)


    # -----

    def updateSliderValueChanged(self):
        self.updateLabel.setText(str(self.updateSlider.value()))

    def clearSliderValueChanged(self):
        self.clearLabel.setText(str(self.clearSlider.value()))

    def clearPointPushButtonClicked(self):

        _tout = self.updateSlider.value()
        val = int(self.clearSlider.value())

        self.fr.setUpdateTime(_tout)
        self.data_len = val

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

        self.MPL_hist.rangeHist(_min, _max)
        self.MPL_diag.rangeDiag(_min, _max)
        self.MPL_hist.rangeColor(_min, _max)
        self.MPL_diag.rangeColor(_min, _max)
        self.logSlot('Успешно.')

    def readFilePushButtonClicked(self):
        self.readFileLineEdit.setText(QFileDialog.getOpenFileName()[0])


    def TR_startFilePushButtonClicked(self):
        _tout = int(self.updateSlider.value())
        _endian = self.endianComboBox.currentText()
        _dll = 'pshow_get.dll'

        self.logSlot('Запуск...')

        self.tr.setParams(_dll, _endian,_tout)

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
        self.MPL_diag.plotDiagSlot(self.points_arr)



        """
        

        self.data.append(val)

        while len(self.data) > self.data_len:
            self.data.pop(0)

        _amp_flg = self.FR_ampCheckBox.isChecked()
        #print(_amp_flg)

        #self.MPL_diag.updateColors(self.data)

        self.MPL_hist.plotHist(self.data)
        self.MPL_diag.plotDiagSlot(self.data, amp_flg=_amp_flg)

        if not _amp_flg:
            self.MPL_diag.setDiagLables('Расположение точек', None, None)
        else:
            self.MPL_diag.setDiagLables('Расположение точек', 'Амплитуда', None)
            
        """

    def clearSlot(self):
        self.data = []

        self.logTextEdit.setText('')
        self.MPL_hist.clearHistSlot()
        self.MPL_diag.clearDiagSlot()



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