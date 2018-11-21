import time
from A_Test import A_Test

# 30 + 10 * 2 = 50 --- atten
# -40 = x - 50, x = 10

# 790 - 960

class CAL_Test(A_Test):

    def __init__(self):
        super(CAL_Test, self).__init__()
       # calibr_file = open('calibr.txt', 'w')

    def run(self):

        self.gen.reset()
        self.an.reset()

        if self.gen.type == 'SMA100A':
            self.gen.setFreqSweep(self.beg, self.end, 'MHz')
            self.gen.setSweeepStep(self.step, 'MHz')
            self.gen.setLevel(self.level, 'dBm')
            self.gen.freqSweepMode()
        elif self.gen.type == 'Agilent N5182A':
            self.gen.setLevel(self.level)
            self.gen.setFrequency(self.beg)

        self.an.setSweep(50, 'ms')
        self.an.setFreqCent(self.beg, 'MHz')
        self.an.setFreqSpan(1, 'MHz')
        self.an.singleSweepMode()
        self.an.traceClearWrite()
        self.an.setTracAver(True)

        self.log_signal.emit('Начало калибровки...')

        if self.type == 'Входной тракт':
            self.calibr_file = open(self.logfile + '\\' + 'in_calibr.txt', 'w')
            self.an.setRefLvl(self.level + 5, 'dBm')
        elif self.type == 'Выходной тракт':
            self.calibr_file = open(self.logfile + '\\' + 'out_calibr.txt', 'w')
            self.an.setRefLvl(self.level + 5, 'dBm')

        self.log_signal.emit('Тип:\t' + self.type)

        try:
            self.gen.RFOutON()
            time.sleep(1)

            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                self.an.setFreqCent(self.beg, 'MHz')

                self.an.averBeginMeas(5)
                time.sleep(0.05)
#                self.an.waitEndCmd()
                self.an.markerOneSetMax()

                tmp1 = '{:10.0f}'.format(self.beg)
                tmp2 = '{:10.2f}'.format(self.an.getMarkerOne() - self.level)

                self.calibr_file.write(tmp1 + ' ' + tmp2 + '\n')
                self.beg = self.beg + self.step
                self.progress_signal.emit(self.beg)

                if self.gen.type == 'SMA100A':
                    self.gen.nextStep()
                elif self.gen.type == 'Agilent N5182A':
                    self.gen.setFrequency(self.beg)
               # time.sleep(0.1)

        except:
            if self.stop_flg:
                self.log_signal.emit('CAL_test остановлен!')
            else:
                self.log_signal.emit('Ошибка в CAL_test::run()')
                raise
        finally:
            self.calibr_file.close()
            self.gen.RFOutOFF()
            self.end_signal.emit(False)
            self.log_signal.emit('CAL_test завершен!')