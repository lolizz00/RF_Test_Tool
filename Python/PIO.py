from A_Test import A_Test
import time
from PyQt5.QtCore import *

# усиление +70
# ослабление -50
# суммарное усиление +20
# максимум на анализатор +10
# максимальный уровень на выходе генератора -10

class PIO_Test(A_Test):

    gain_file = None

    res_in = None

    find_flag = False

    result = None

    plot_flag = False

    fix_signal = pyqtSignal(bool)

    gain_arr = {}  # TODO Делать  в основной программе

    def __init__(self):
        super(PIO_Test, self).__init__()

    def run(self):

        up_flg = self.user[1]

        self.pan = self.user[2]


        self.gain_file = open(self.user[0], 'r')

        if self.logfile and not up_flg:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

            self.writeToLog('Date:                     ' + time.ctime(time.time()))
            self.writeToLog('Generator:                ' + self.gen.fullName)
            self.writeToLog('Analyzer:                 ' + self.an.fullName)
            self.writeToLog('Тип устройства:           ' + self.user[3])
            self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
            if self.pan:
                self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
                self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
                self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

            self.writeToLog('\n')

        for line in self.gain_file:
            if line.find('Freq') == -1:
                continue
            line = line.replace('Freq: ', '')
            line = line.replace('Gain:', '')
            key, val = line.split()
            self.gain_arr[float(key)] = float(val)

        self.x = []
        self.y = []

        gain = self.gain_arr[self.freq]
        out = None

        self.stop_flg = False
        self.find_flag = False

        self.an.reset()

        if not self.pan:
            self.an.setFreqCent(self.freq, 'MHz')
        else:
            self.an.setFreqCent(750, 'MHz')
            self.dev.setFreqReboot(self.freq)
        self.an.setFreqSpan(100, 'KHz')
        self.an.singleSweepMode()
        self.an.setSweep(50, 'ms')
        self.an.setMarkerOne(self.freq)

        self.gen.reset()

        if self.cal_flg:
            self.gen.setLevel(self.beg - self.cal_in[round(self.freq)], 'dBm')
        else:
            self.gen.setLevel(self.beg, 'dBm')

        if self.gen.type == 'SMA100A':
            self.gen.setFreq(self.freq)
        elif self.gen.type == 'N5182A':
            self.gen.setFrequency(self.freq)

        self.gen.RFOutON()

        try:
            while self.beg <= self.end:

                if self.find_flag:
                    self.stop_flg = True
                    #raise Warning

                if self.stop_flg:
                    raise Warning

               # time.sleep(0.1)

                if self.cal_flg:
                    tmp = self.gen.setLevel(self.beg - self.cal_in[round(self.freq)], 'dBm')
                    if tmp and tmp == 'MAX':
                        self.writeToLog('Достигнут максимальный уровень сигнала --- '
                                        + str(self.beg - self.cal_in[round(self.freq)]) + ' dBm')

                else:
                    self.gen.setLevel(self.beg, 'dBm')

                self.an.setRefLvl(self.beg + 10, 'dBm')

                self.an.beginMeas()

                self.an.markerOneSetMax()
                tmp = self.an.getMarkerOne()

                self.x.append(self.beg)

                if self.cal_flg:
                    self.y.append(tmp - self.cal_out[round(self.freq)])
                else:
                    self.y.append(tmp)

                if self.cal_flg:
                    out = tmp - self.cal_out[round(self.freq)]
                else:
                    out = tmp

                id = self.beg + gain

                if (id - out) > 1.1:

                    self.log_signal.emit('P1dB по входу: ' + str(round(self.beg, 2)))
                    self.log_signal.emit('P1dB по выходу: ' + str(round(out, 2)))

                    if not up_flg:
                        self.writeToLog('IP3:\t' + str(round(self.beg, 2)))
                        self.writeToLog('OP3:\t' + str(round(out, 2)))

                        self.writeToLog('\n\n')

                    self.res_out = self.beg
                    self.res_in = round(out, 2)

                    self.find_flag = True

                self.beg = self.beg + self.step

                time.sleep(0.1)

                if self.plot_flg and not up_flg:
                    self.plot_signal.emit(self.x, self.y, self.color, True)
                    self.progress_signal.emit(self.beg)


               # time.sleep(1)

        except:
            if self.stop_flg:
                pass
                print('PIO stopped')
            else:
                print('Error in PIO()')
                raise
        finally:
            self.gen.RFOutOFF()

            self.plot_signal.emit(self.x, self.y, self.color, True)
            self.progress_signal.emit(self.end)

            if not up_flg:
                for i in range(len(self.x)):
                    self.writeToLog('Pin: ' + str(round(self.x[i], 2)) + ' Pout:' + str(round(self.y[i], 2)))

            if self.logfile and not up_flg:
                self.logfile.close()

            self.fix_signal.emit(False)

            #time.sleep(1)

            if not up_flg:
                self.end_signal.emit(False)
                self.savescreen_signal.emit(self.name)
                self.log_signal.emit('READY!')
                self.fix_signal.emit(False)

                self.find_flag = True



