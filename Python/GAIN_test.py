from A_Test import A_Test
import time

class GAIN_Test(A_Test):


    def __init__(self):
        super(GAIN_Test, self).__init__()

    def run(self):

        self.gen_flg = self.user[0]

        if self.user[2] == 'USRP':
            self.sdr = True
        elif self.user[2] == 'Панорама':
            self.pan = True

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Тип устройства:           ' + self.user[2])
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('Амплитуда по входу:       ' + str(self.level))
        self.writeToLog('_type:                    ' + 'GAIN')
        if self.pan:
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('GAIN')
        self.writeToLog('\n')
        self.an.reset()

        self.an.setFreqCent(self.beg, 'MHz')

        self.an.setFreqSpan(1, 'MHz')
        self.an.singleSweepMode()
        self.an.traceClearWrite()
        self.an.setTracAver(True)

        if self.pan:
            if self.dev.getLNA():
                self.an.setRefLvl(self.level + 45, 'dBm')
            else:
                self.an.setRefLvl(self.level + 30, 'dBm')

        else:
            self.an.setRefLvl(self.level + 15, 'dBm')


        self.gen.reset()
        if self.gen.type == 'SMA100A':
            self.gen.setFreqSweep(self.beg, self.end, 'MHz')
            self.gen.setSweeepStep(self.step, 'MHz')
            self.gen.setLevel(self.level, 'dBm')
            self.gen.freqSweepMode()
        elif self.gen.type == 'N5182A':
            self.gen.setLevel(self.level)
            self.gen.setFrequency(self.beg)

        self.gen.RFOutON()

        gain = None

        time.sleep(1)

        try:
            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                if self.cal_flg:
                    self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')

                if not self.pan:
                    self.an.setFreqCent(self.beg, 'MHz')
                else:
                    self.an.setFreqCent(750, 'MHz')
                    self.dev.setFreqReboot(self.beg)

                self.an.averBeginMeas(5)
                time.sleep(0.05)
                self.an.markerOneSetMax()

                tmp = self.an.getMarkerOne()

                self.x.append(self.beg)

                if self.cal_flg:
                    if self.pan:
                        gain = (tmp - self.cal_out[750]) - self.level
                    else:
                        gain = (tmp - self.cal_out[round(self.beg)]) - self.level
                else:
                    gain = tmp - self.level

                self.y.append(gain)

                self.beg = self.beg + self.step

                if self.gen.type == 'SMA100A':
                    self.gen.nextStep()
                elif self.gen.type == 'N5182A':
                    self.gen.setFrequency(self.beg)

                #time.sleep(0.1)

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color, True)

                self.progress_signal.emit(self.beg)

                #time.sleep(0.1)

        except:
            if self.stop_flg:
                print('GAIN stopped')
            else:
                print('Error in GAIN()')
        finally:
            self.gen.RFOutOFF()

            for i in range(len(self.x)):
                self.writeToLog('Freq: ' + str(self.x[i]) + ' Gain:' + str(round(self.y[i], 2)))


            if self.logfile:
                self.logfile.close()

            self.plot_signal.emit(self.x, self.y, self.color, True)
            self.progress_signal.emit(self.end)

            time.sleep(1)

            self.end_signal.emit(False)

            self.savescreen_signal.emit(self.name)

            self.log_signal.emit('READY!')

