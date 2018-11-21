from A_Test import A_Test
from PyQt5.QtCore import *
import time
import math


class EFF_Test(A_Test):

    def __init__(self):
        super(EFF_Test, self).__init__()

    def run(self):

        self.x = []
        self.y = []

        if self.logfile:
            self.logfile = open(self.logfile, 'w')

        self.writeToLog('Date:\t' + time.ctime(time.time()))
        self.writeToLog('\n\n')
        self.writeToLog('Generator:\t' + self.gen.fullName)
        self.writeToLog('Analyzer:\t' + self.an.fullName)
        self.writeToLog('\n')
        self.writeToLog('Использование калибровки:\t' + str(self.cal_flg))
        self.writeToLog('\n')

        self.gain = None
        pout = None
        result = None


        #self.color = 'yellow'

        self.an.reset()

        self.an.setFreqCent(self.freq, 'MHz')
        self.an.setFreqSpan(100, 'KHz')
        self.an.singleSweepMode()
        self.an.setSweep(50, 'ms')
        self.an.setMarkerOne(self.freq)

        self.gen.reset()

        if self.gen.type == 'SMA100A':
            if self.cal_flg:
                self.gen.setLevel(self.beg - self.cal_in[round(self.freq)], 'dBm')
            else:
                self.gen.setLevel(self.beg, 'dBm')
            self.gen.setFreq(self.freq)
        elif self.gen.type == 'Agilent N5182A':
            if self.cal_flg:
                self.gen.setLevel(self.beg - self.cal_in[round(self.freq)])
            else:
                self.gen.setLevel(self.beg)
            self.gen.setFrequency(self.freq)

        self.gen.RFOutON()

        try:
            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                time.sleep(0.5)

                if self.gen.type == 'SMA100A':
                    if self.cal_flg:
                        self.gen.setLevel(self.beg - self.cal_in[round(self.freq)], 'dBm')
                    else:
                        self.gen.setLevel(self.beg, 'dBm')
                elif self.gen.type == 'N5182A':
                    if self.cal_flg:
                        self.gen.setLevel(self.beg - self.cal_in[round(self.freq)])
                    else:
                        self.gen.setLevel(self.beg)

                self.an.setRefLvl(self.beg + 22, 'dBm')

                self.an.beginMeas()

                tmp = self.an.getMarkerOne()

                if self.cal_flg:
                    pout = tmp - self.cal_out[round(self.freq)]
                else:
                    pout = tmp

                gain = math.pow(10, pout / 10) * 0.001 - math.pow(10, self.beg / 10) * 0.001

                result = (gain / self.pb.getCurrPow()) * 100

                self.x.append(self.beg)
                self.y.append(result)

                self.beg = self.beg + self.step

                #self.gen.setLevel(self.beg, 'dDm')

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color)

                self.progress_signal.emit(self.beg)

        except:
            if self.stop_flg:
                pass
            else:
                print('Error in EFF()')
                raise
        finally:
            self.gen.RFOutOFF()



            self.plot_signal.emit(self.x, self.y, self.color)
            self.progress_signal.emit(self.end)

            for i in range(len(self.x)):
                self.writeToLog('Pin: ' + str(self.x[i]) + ' EFF:' + str(round(self.y[i], 2)))
            time.sleep(1)

            if self.logfile:
                self.logfile.close()

            self.end_signal.emit(False)

            self.log_signal.emit('READY!')