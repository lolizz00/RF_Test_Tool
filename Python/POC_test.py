from A_Test import A_Test
from PIO import PIO_Test
import time
from PyQt5.QtGui import *
from PyQt5.QtCore  import *


class POC_test(A_Test):

    ready_flag = False
    fix_flag = False

    fix_signal = pyqtSignal()

    def __init__(self):
        super(POC_test, self).__init__()
        self.pio = PIO_Test()
        self.pio.end_signal.connect(self.readySlot)



    def run(self):

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        if self.user[4] == 'USRP':
            self.sdr = True
        elif self.user[4] == 'Панорама':
            self.pan = True

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Тип устройства:           ' + self.user[4])
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        if self.pan:
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))
            pass

        self.writeToLog('\n\n')

        self.pio.fix_signal.connect(self.readySlot)

        self.x = []
        self.y = []

        self.x2 = []
        self.y2 = []

        self.color2 = 'blue'

        try:

            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                self.ready_flag = False
                self.find_flag = False

                if self.pan:
                    self.dev.setFreqReboot(self.beg)

                self.pio.setParams(self.user[0], self.user[1], self.user[2], self.beg, None, self.gen, self.an, self.dev,
                                   self.color,
                                   cal_flg=self.cal_flg, cal_in=self.cal_in, cal_out=self.cal_out,
                                   user=[self.user[3], True, self.pan, self.user[4]],
                                   plot_flg=self.plot_flg,
                                   logfile=self.logfile)

                self.pio.run()

                while not self.ready_flag:
                    pass

               # if self.pio.result < -23:  # TODO
                  #  self.fix_signal.emit()
                   # continue
                #     pass

                self.x.append(self.beg)
                self.y.append(self.pio.res_out)

                self.x2.append(self.beg)
                self.y2.append(self.pio.res_in)

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color, True)
                    self.plot_signal.emit(self.x2, self.y2, self.color2, False)

                self.progress_signal.emit(self.beg)

                self.beg = self.beg + self.step

               # time.sleep(1)

        except:
            if self.stop_flg:
                print('POC stopped')
            else:
                print('Error in POC()')
                raise
        finally:
            self.plot_signal.emit(self.x, self.y, self.color, True)
            self.savescreen_signal.emit(self.name + '_IN')

            self.plot_signal.emit(self.x2, self.y2, self.color2, True)
            self.savescreen_signal.emit(self.name + '_OUT')

            self.progress_signal.emit(self.end)

            for i in range(len(self.x)):
                self.writeToLog('Freq: ' + str(self.x[i]) + '\tIP3: ' + str(round(self.y[i], 2)) + '\tOP3: '
                                + str(round(self.y2[i], 2)))

           # self.savescreen_signal.emit(self.name)

            if self.logfile:
                self.logfile.close()

           # time.sleep(1)

            self.end_signal.emit(False)

            self.log_signal.emit('READY!')

    def readySlot(self):
        self.ready_flag = True

