# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\RF_Test_Tool\QAM\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1516, 1012)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cw = QtWidgets.QWidget(self.centralwidget)
        self.cw.setGeometry(QtCore.QRect(0, 0, 1310, 670))
        self.cw.setMinimumSize(QtCore.QSize(1310, 670))
        self.cw.setObjectName("cw")
        self.gridLayout = QtWidgets.QGridLayout(self.cw)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.controlGroupBox = QtWidgets.QGroupBox(self.cw)
        self.controlGroupBox.setMinimumSize(QtCore.QSize(400, 0))
        self.controlGroupBox.setMaximumSize(QtCore.QSize(350, 16777215))
        self.controlGroupBox.setObjectName("controlGroupBox")
        self.layoutWidget = QtWidgets.QWidget(self.controlGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 361, 620))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dataControlGroupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.dataControlGroupBox.setMinimumSize(QtCore.QSize(350, 150))
        self.dataControlGroupBox.setMaximumSize(QtCore.QSize(350, 150))
        self.dataControlGroupBox.setObjectName("dataControlGroupBox")
        self.clearPointPushButton = QtWidgets.QPushButton(self.dataControlGroupBox)
        self.clearPointPushButton.setGeometry(QtCore.QRect(150, 110, 75, 23))
        self.clearPointPushButton.setObjectName("clearPointPushButton")
        self.layoutWidget1 = QtWidgets.QWidget(self.dataControlGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(11, 30, 321, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.updateSlider = QtWidgets.QSlider(self.layoutWidget1)
        self.updateSlider.setMinimum(100)
        self.updateSlider.setMaximum(1000)
        self.updateSlider.setSingleStep(100)
        self.updateSlider.setPageStep(100)
        self.updateSlider.setProperty("value", 500)
        self.updateSlider.setOrientation(QtCore.Qt.Horizontal)
        self.updateSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.updateSlider.setObjectName("updateSlider")
        self.horizontalLayout_3.addWidget(self.updateSlider)
        self.updateLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.updateLabel.setObjectName("updateLabel")
        self.horizontalLayout_3.addWidget(self.updateLabel)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.layoutWidget2 = QtWidgets.QWidget(self.dataControlGroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 70, 321, 31))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.clearSlider = QtWidgets.QSlider(self.layoutWidget2)
        self.clearSlider.setMinimum(10)
        self.clearSlider.setMaximum(1000)
        self.clearSlider.setSingleStep(50)
        self.clearSlider.setPageStep(50)
        self.clearSlider.setProperty("value", 300)
        self.clearSlider.setTracking(True)
        self.clearSlider.setOrientation(QtCore.Qt.Horizontal)
        self.clearSlider.setInvertedAppearance(False)
        self.clearSlider.setInvertedControls(False)
        self.clearSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.clearSlider.setTickInterval(50)
        self.clearSlider.setObjectName("clearSlider")
        self.horizontalLayout_4.addWidget(self.clearSlider)
        self.clearLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.clearLabel.setObjectName("clearLabel")
        self.horizontalLayout_4.addWidget(self.clearLabel)
        self.endianComboBox = QtWidgets.QComboBox(self.dataControlGroupBox)
        self.endianComboBox.setGeometry(QtCore.QRect(10, 110, 84, 20))
        self.endianComboBox.setObjectName("endianComboBox")
        self.endianComboBox.addItem("")
        self.endianComboBox.addItem("")
        self.verticalLayout.addWidget(self.dataControlGroupBox)
        self.readerToolBox = QtWidgets.QToolBox(self.layoutWidget)
        self.readerToolBox.setMinimumSize(QtCore.QSize(350, 150))
        self.readerToolBox.setMaximumSize(QtCore.QSize(350, 150))
        self.readerToolBox.setObjectName("readerToolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 350, 96))
        self.page.setObjectName("page")
        self.layoutWidget3 = QtWidgets.QWidget(self.page)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 0, 321, 31))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_5.setMinimumSize(QtCore.QSize(40, 20))
        self.label_5.setMaximumSize(QtCore.QSize(40, 20))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.readFileLineEdit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.readFileLineEdit.setObjectName("readFileLineEdit")
        self.horizontalLayout.addWidget(self.readFileLineEdit)
        self.readFilePushButton = QtWidgets.QPushButton(self.layoutWidget3)
        self.readFilePushButton.setMinimumSize(QtCore.QSize(20, 20))
        self.readFilePushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.readFilePushButton.setObjectName("readFilePushButton")
        self.horizontalLayout.addWidget(self.readFilePushButton)
        self.layoutWidget4 = QtWidgets.QWidget(self.page)
        self.layoutWidget4.setGeometry(QtCore.QRect(160, 70, 168, 27))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RD_startFilePushButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.RD_startFilePushButton.setMinimumSize(QtCore.QSize(80, 25))
        self.RD_startFilePushButton.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.RD_startFilePushButton.setFont(font)
        self.RD_startFilePushButton.setObjectName("RD_startFilePushButton")
        self.horizontalLayout_2.addWidget(self.RD_startFilePushButton)
        self.RD_stopFilePushButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.RD_stopFilePushButton.setMinimumSize(QtCore.QSize(80, 25))
        self.RD_stopFilePushButton.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.RD_stopFilePushButton.setFont(font)
        self.RD_stopFilePushButton.setObjectName("RD_stopFilePushButton")
        self.horizontalLayout_2.addWidget(self.RD_stopFilePushButton)
        self.layoutWidget5 = QtWidgets.QWidget(self.page)
        self.layoutWidget5.setGeometry(QtCore.QRect(10, 40, 203, 22))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.RD_emulateCheckBox = QtWidgets.QCheckBox(self.layoutWidget5)
        self.RD_emulateCheckBox.setChecked(True)
        self.RD_emulateCheckBox.setObjectName("RD_emulateCheckBox")
        self.horizontalLayout_8.addWidget(self.RD_emulateCheckBox)
        self.readerToolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 350, 96))
        self.page_2.setObjectName("page_2")
        self.TR_deltaCheckBox = QtWidgets.QCheckBox(self.page_2)
        self.TR_deltaCheckBox.setGeometry(QtCore.QRect(200, 0, 141, 21))
        self.TR_deltaCheckBox.setObjectName("TR_deltaCheckBox")
        self.layoutWidget_2 = QtWidgets.QWidget(self.page_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(160, 70, 168, 27))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.TR_startFilePushButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.TR_startFilePushButton.setMinimumSize(QtCore.QSize(80, 25))
        self.TR_startFilePushButton.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.TR_startFilePushButton.setFont(font)
        self.TR_startFilePushButton.setObjectName("TR_startFilePushButton")
        self.horizontalLayout_7.addWidget(self.TR_startFilePushButton)
        self.TR_stopFilePushButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.TR_stopFilePushButton.setMinimumSize(QtCore.QSize(80, 25))
        self.TR_stopFilePushButton.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.TR_stopFilePushButton.setFont(font)
        self.TR_stopFilePushButton.setObjectName("TR_stopFilePushButton")
        self.horizontalLayout_7.addWidget(self.TR_stopFilePushButton)
        self.readerToolBox.addItem(self.page_2, "")
        self.verticalLayout.addWidget(self.readerToolBox)
        self.plotControlGroupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.plotControlGroupBox.setMinimumSize(QtCore.QSize(350, 150))
        self.plotControlGroupBox.setMaximumSize(QtCore.QSize(350, 150))
        self.plotControlGroupBox.setObjectName("plotControlGroupBox")
        self.clearPushButton = QtWidgets.QPushButton(self.plotControlGroupBox)
        self.clearPushButton.setGeometry(QtCore.QRect(260, 80, 75, 23))
        self.clearPushButton.setObjectName("clearPushButton")
        self.layoutWidget6 = QtWidgets.QWidget(self.plotControlGroupBox)
        self.layoutWidget6.setGeometry(QtCore.QRect(20, 20, 327, 31))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_6.setMinimumSize(QtCore.QSize(110, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.vieMinLineEdit = QtWidgets.QLineEdit(self.layoutWidget6)
        self.vieMinLineEdit.setObjectName("vieMinLineEdit")
        self.horizontalLayout_6.addWidget(self.vieMinLineEdit)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.vieMaxLineEdit = QtWidgets.QLineEdit(self.layoutWidget6)
        self.vieMaxLineEdit.setObjectName("vieMaxLineEdit")
        self.horizontalLayout_6.addWidget(self.vieMaxLineEdit)
        self.viePushButton = QtWidgets.QPushButton(self.layoutWidget6)
        self.viePushButton.setObjectName("viePushButton")
        self.horizontalLayout_6.addWidget(self.viePushButton)
        self.layoutWidget7 = QtWidgets.QWidget(self.plotControlGroupBox)
        self.layoutWidget7.setGeometry(QtCore.QRect(20, 110, 275, 25))
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget7)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget7)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.colorComboBox = QtWidgets.QComboBox(self.layoutWidget7)
        self.colorComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.colorComboBox.setObjectName("colorComboBox")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.horizontalLayout_9.addWidget(self.colorComboBox)
        self.setColorPushButton = QtWidgets.QPushButton(self.layoutWidget7)
        self.setColorPushButton.setObjectName("setColorPushButton")
        self.horizontalLayout_9.addWidget(self.setColorPushButton)
        self.widget = QtWidgets.QWidget(self.plotControlGroupBox)
        self.widget.setGeometry(QtCore.QRect(20, 60, 201, 51))
        self.widget.setObjectName("widget")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.FR_ampCheckBox = QtWidgets.QCheckBox(self.widget)
        self.FR_ampCheckBox.setObjectName("FR_ampCheckBox")
        self.verticalLayout_20.addWidget(self.FR_ampCheckBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.ampChanComboBox = QtWidgets.QComboBox(self.widget)
        self.ampChanComboBox.setObjectName("ampChanComboBox")
        self.ampChanComboBox.addItem("")
        self.ampChanComboBox.addItem("")
        self.ampChanComboBox.addItem("")
        self.ampChanComboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.ampChanComboBox)
        self.verticalLayout_20.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addWidget(self.plotControlGroupBox)
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(350, 150))
        self.groupBox.setMaximumSize(QtCore.QSize(350, 150))
        self.groupBox.setObjectName("groupBox")
        self.logTextEdit = QtWidgets.QTextEdit(self.groupBox)
        self.logTextEdit.setGeometry(QtCore.QRect(10, 20, 320, 120))
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout.addWidget(self.controlGroupBox, 1, 2, 1, 1)
        self.diag = MPL_Diag(self.cw)
        self.diag.setObjectName("diag")
        self.gridLayout.addWidget(self.diag, 1, 0, 1, 1)
        self.hist = MPL_Hist(self.cw)
        self.hist.setObjectName("hist")
        self.gridLayout.addWidget(self.hist, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1516, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.readerToolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QAM"))
        self.controlGroupBox.setTitle(_translate("MainWindow", "Настройки"))
        self.dataControlGroupBox.setTitle(_translate("MainWindow", "Управление данными"))
        self.clearPointPushButton.setText(_translate("MainWindow", "Применить"))
        self.label.setText(_translate("MainWindow", "Интервал обновления:"))
        self.updateLabel.setText(_translate("MainWindow", "50"))
        self.label_2.setText(_translate("MainWindow", "ms"))
        self.label_3.setText(_translate("MainWindow", "Кол-во точек на графике"))
        self.clearLabel.setText(_translate("MainWindow", "50"))
        self.endianComboBox.setItemText(0, _translate("MainWindow", "Little Endian"))
        self.endianComboBox.setItemText(1, _translate("MainWindow", "Big Endian"))
        self.label_5.setText(_translate("MainWindow", "Путь:"))
        self.readFileLineEdit.setText(_translate("MainWindow", "H:/RF_Test_Tool/QAM/testdata/test_data_0.pcm"))
        self.readFilePushButton.setText(_translate("MainWindow", "..."))
        self.RD_startFilePushButton.setText(_translate("MainWindow", "Старт"))
        self.RD_stopFilePushButton.setText(_translate("MainWindow", "Стоп"))
        self.RD_emulateCheckBox.setText(_translate("MainWindow", "Эмуляция потока"))
        self.readerToolBox.setItemText(self.readerToolBox.indexOf(self.page), _translate("MainWindow", "Файл"))
        self.TR_deltaCheckBox.setText(_translate("MainWindow", "Отображать разницу"))
        self.TR_startFilePushButton.setText(_translate("MainWindow", "Старт"))
        self.TR_stopFilePushButton.setText(_translate("MainWindow", "Стоп"))
        self.readerToolBox.setItemText(self.readerToolBox.indexOf(self.page_2), _translate("MainWindow", "Поток"))
        self.plotControlGroupBox.setTitle(_translate("MainWindow", "Управлнение графиками"))
        self.clearPushButton.setText(_translate("MainWindow", "Очистить"))
        self.label_6.setText(_translate("MainWindow", "Диапазон просмотра:"))
        self.vieMinLineEdit.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "-"))
        self.vieMaxLineEdit.setText(_translate("MainWindow", "360"))
        self.viePushButton.setText(_translate("MainWindow", "Применить"))
        self.label_8.setText(_translate("MainWindow", "Палитра цветов:"))
        self.colorComboBox.setItemText(0, _translate("MainWindow", "gist_rainbow"))
        self.colorComboBox.setItemText(1, _translate("MainWindow", "nipy_spectral"))
        self.colorComboBox.setItemText(2, _translate("MainWindow", "hsv"))
        self.setColorPushButton.setText(_translate("MainWindow", "Применить"))
        self.FR_ampCheckBox.setText(_translate("MainWindow", "Отобр. амплитуды"))
        self.label_4.setText(_translate("MainWindow", "Номер канала:"))
        self.ampChanComboBox.setItemText(0, _translate("MainWindow", "0"))
        self.ampChanComboBox.setItemText(1, _translate("MainWindow", "1"))
        self.ampChanComboBox.setItemText(2, _translate("MainWindow", "2"))
        self.ampChanComboBox.setItemText(3, _translate("MainWindow", "3"))
        self.groupBox.setTitle(_translate("MainWindow", "Лог"))

from MPL_diag import MPL_Diag
from MPL_hist import MPL_Hist
