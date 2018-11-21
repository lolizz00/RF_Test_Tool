from A_Test import A_Test
import time

class ACC_Test(A_Test):
    def __init__(self):
        super(ACC_Test, self).__init__()

    def run(self):

        self.sdr = False
        self.pan = False

        self.step = 1

        if self.dev.type == 'USRP':
            self.sdr = True
        elif self.dev.type == 'Панорама':
            self.pan = True

        self.succ_flg = False
        self.end_signal.emit(True)
        self.stop_flg = False

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Тип устройства:           ' + self.user[0])
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('Амплитуда по входу:       ' + str(self.level))
        self.writeToLog('_type:                    ' + 'ACC')

        if self.pan:
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('ACC')
        self.writeToLog('\n')


        self.an.reset()

        if not self.pan:
            self.an.setFreqCent(self.beg, 'MHz')
        else:
            self.an.setFreqCent(750, 'MHz')
            self.an.setMarkerOne(750)

        self.an.setTracAver(False)
        self.an.setSweep(50, 'ms')
        self.an.setFreqSpan(self.span, 'KHz')
        self.an.singleSweepMode()
        self.an.setRefLvl(self.level + 30, 'dBm')
        self.an.setRef('EXT')


        self.gen.reset()

        if self.gen.type == 'SMA100A':
            self.gen.setFreqSweep(self.beg, self.end, 'MHz')
            self.gen.setSweeepStep(self.step, 'MHz')
            self.gen.freqSweepMode()
        elif self.gen.type == 'N5182A':
            self.gen.setFrequency(self.beg)

        self.gen.setLevel(self.level)

        self.gen.RFOutON()
        time.sleep(1)

        try:
            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                if not self.pan:
                    self.an.setFreqCent(self.beg, 'MHz')
                else:
                    self.dev.setFreqReboot(self.beg)

                # ------

                self.an.beginMeas()
                self.an.markerOneSetMax()

                tmp = self.an.getMarkerOneFreq()

                self.x.append(self.beg)

                if self.pan:

                    _freq_val = 750 * 1000000 # эталоннная


                    tmp = ( abs(_freq_val - tmp) / (self.beg * 1000000)) * 1000000000



                    #tmp = abs(tmp - 750 * 1000000)

                    #tmp = (tmp / _freq_val) * 1000000000 # ppd

                    #tmp = abs(tmp - 750 * 1000000) # дельта
                    self.y.append(tmp)

                # ------

                self.beg = self.beg + self.step

                if self.gen.type == 'SMA100A':
                    self.gen.nextStep()
                elif self.gen.type == 'N5182A':
                    self.gen.setFrequency(self.beg)

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color, True)

                self.progress_signal.emit(self.beg)


        except:
            if self.stop_flg:
                print('ACC stopped')
            else:
                print('Error in ACC()')
        finally:
            self.gen.RFOutOFF()

            for i in range(len(self.x)):
                self.writeToLog('Freq: ' + str(self.x[i]) + ' Delta:' + str(round(self.y[i], 2)) + ' ppb')

            if self.logfile:
                self.logfile.close()

            self.plot_signal.emit(self.x, self.y, self.color, False)
            self.progress_signal.emit(self.end)
            self.savescreen_signal.emit(self.name)
            time.sleep(1)
            self.end_signal.emit(False)
            self.log_signal.emit('READY!')

