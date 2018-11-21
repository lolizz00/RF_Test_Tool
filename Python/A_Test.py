from PyQt5.QtCore import *
import time
import numpy as np
from start import MPL_Plot

class A_Test(QThread):

    #  ----- Сигналы для вз/д с MW

    plot_signal = pyqtSignal(list, list, str, bool)  # сигнал построения графика

    mpl_plot_over_spec = pyqtSignal(list)
    mpl_plot_signal = pyqtSignal(int, list, list, str)
    mpl_set_plot_count = pyqtSignal(int)
    mpl_set_spec_count = pyqtSignal()
    spec_signal = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)  # сигнал построения графика
    mpl_set_graph_title = pyqtSignal(int, str)
    mpl_set_spec_title = pyqtSignal(str)
    mpl_save_add_graph = pyqtSignal(str)
    mpl_save_spec = pyqtSignal(str)
    mpl_plot_3d = pyqtSignal(str)
    mpl_plot = pyqtSignal(list, bool, str)

    progress_signal = pyqtSignal(int)  # сигнал текущего прогресса( progress bar)
    log_signal  = pyqtSignal(str)   # сигнал отчета для окна лога
    end_signal = pyqtSignal(bool)  # сигнал окончания работы
    savescreen_signal = pyqtSignal(str)
    savescreen_an_signal = pyqtSignal(str, str)
    tray_signal = pyqtSignal(str, str)
    addline_signal = pyqtSignal(bool, float, str)
    # ----- Разное

    logfile = None  # файл ведения отчета
    acc = 3  # через сколько итерация отправляется сигнал графика
    res = ''  # строка результата
    x = []  # массивы для хранения резульатов
    y = []

    # --- Принимаемые параметры

    beg = None  # начало диапазона
    end = None  # конец диапазона
    freq = None  # рабочая частота
    level = None  # рабочий уровень
    step = None  # шаг диапазона
    type = None
    sweep_time = None
    user = None
    name = None

    cal_in = None  # файл калибровки
    cal_out = None

    gen = None  # используемый генератор
    an = None  # используемый анализатор
    dev = None  # устройство для вз/д
    pb = None

    color = None  # цвет отстройки графика

    # gain_file = None  #  Хм.

    # ----- Флаги

    succ_flg = False  # однажды выполнялся, результаты сохранены
    stop_flg = False  # флаг для отсановки работы
    cal_flg = False  # используется файл калибровки
    init_flg = False  # параметры теста заданы
    plot_flg = False
        
    def __init__(self):
        super(A_Test, self).__init__()

    def writeToLog(self, text):
        if self.logfile:
            self.logfile.write(text + '\n')

    def getResults(self):
        if self.succ_flg:
            return [self.x, self.y, self.res]

    def setParams(self, beg, end, step, freq, level, gen, an, dev, color,  sweep_time=None, acc=1,
                  logfile=None, cal_flg=False, cal_in=None, cal_out=None, type=None, pb=None, user=None,
                  plot_flg=False, span=None, threshold=None, path=None):

        self.beg = beg
        self.end = end
        self.step = step
        self.freq = freq
        self.level = level
        self.cal_in = cal_in
        self.cal_out = cal_out
        self.gen = gen
        self.an = an
        self.dev = dev
        self.color = color
        self.acc = acc
        self.logfile = logfile
        self.type = type
        self.cal_flg = cal_flg
        self.sweep_time = sweep_time
        self.pb = pb
        self.user = user
        self.plot_flg = plot_flg
        self.span = span
        self.threshold = threshold
        self.path = path

        self.end_flg = False
        self.stop_flg = False
        self.init_flg = True

        self.x = []
        self.y = []



    def stop(self):
        self.stop_flg = True
        pass