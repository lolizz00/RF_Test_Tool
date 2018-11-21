from A_Test import A_Test
import time



class BF_Test(A_Test):
    def __init__(self):
        super(BF_Test, self).__init__()

    def run(self):
        if self.user[0] == 'Панорама':
            self.pan = True
        else:
            return

        self.succ_flg = False
        self.end_signal.emit(True)
        self.stop_flg = False

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Тип устройства:           ' + self.user[0])
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))

        if self.pan:
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())

        self.writeToLog('\n')

        self.an.reset()

        if not self.pan:
            self.an.setFreqCent(self.beg, 'MHz')
        else:
            self.an.setFreqCent(750, 'MHz')
            self.an.setMarkerOne(750)

        self.an.setFreqSpan(self.span, 'MHz')
        #self.an.singleSweepMode()
        self.an.setTracAver(True)
        self.an.setSweep(20, 'ms')
        self.an.setRefLvl(-40, 'dBm')

        time.sleep(10)

        try:

            self.an.markerOneSetMax()
            if self.cal_flg:
                self.noise = self.an.getMarkerOne() - self.cal_out[750]
            else:
                self.noise = self.an.getMarkerOne()

            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                if not self.pan:
                    self.an.setFreqCent(self.beg, 'MHz')
                    self.an.setMarkerOne(self.beg)
                else:
                    if not self.dev.setFreqReboot(self.beg):
                        self.writeToLog('Freq: ' + str(self.beg) + ' ----- Cannot set freq')

                #self.an.beginMeas()
                time.sleep(5)
                self.an.markerOneSetMax()
                tmp = self.an.getMarkerOne()

                if self.cal_flg:
                    if not self.pan:
                        tmp = tmp - self.cal_out[round(self.beg)]
                    else:
                        tmp = tmp - self.cal_out[750]
                else:
                   pass

                if tmp - self.noise > self.threshold:
                    self.writeToLog('Freq: ' + str(self.beg) + ' ----- Detected bad freq')
                    self.savescreen_an_signal.emit('BF_' + str(self.beg) + 'MHz.PNG', self.path)
                    time.sleep(3)
                    pass

                self.beg = self.beg + self.step

                self.progress_signal.emit(self.beg)

                # time.sleep(0.1)



        except:
            if self.stop_flg:
                print('BF stopped')
            else:
                print('Error in BF()')
                raise
        finally:

            self.dev.setMode('standby')

            if self.logfile:
                self.logfile.close()

            self.progress_signal.emit(self.end)

            time.sleep(1)

            self.end_signal.emit(False)

            self.log_signal.emit('READY!')
