from A_Test import A_Test
import time
import numpy as np

class PN_Test(A_Test):
    def __init__(self):
        super(PN_Test, self).__init__()

    def run(self):

        self.stop_flg = False

        # ----- парсим параметры

        #return




        self._span = self.user[0]
        self.rbw = self.user[1]
        self.arr = self.user[2]

        # ----- запись в лог

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('RBW:                      ' + str(self.rbw))
        self.writeToLog('Тип устройства:           ' + self.dev.type)
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('Амплитуда по входу:       ' + str(self.level))
        self.writeToLog('_type:                    ' + 'PN')

        if self.dev.type == 'Panorama':
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('PN')
        self.writeToLog('\n')

        # ----- инициализация Анализатора

        self.an.reset()
        self.an.setFreqSpan(10)
        if self.dev.type == 'Panorama':
            self.an.setFreqCent(750)
        else:
            pass

        if self.dev.type == 'Panorama':
            if self.dev.getLNA():
                self.an.setRefLvl(self.level + 45, 'dBm')
            else:
                self.an.setRefLvl(self.level + 30, 'dBm')
        else:
            self.an.setRefLvl(self.level + 5)

        self.an.enablePhaseNoise()

        self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setSweep(2.5)

        #self.an.setBandwidth(self.rbw)

        # ----- инициализация Генератора
        self.gen.reset()
        self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')
        self.gen.setFreq(self.beg)
        self.gen.RFOutON()
        # -----

        self.x = []
        self.y = []

        time.sleep(0.5)

        try:
            for i in range(self.beg, self.end + 1, self.step):

                if self.stop_flg:
                    raise Warning

                self.dev.setFreqReboot(i)

                self.gen.setLevel(self.level - self.cal_in[round(i)], 'dBm')
                self.gen.setFreq(i)

                time.sleep(0.03)

                self.an.setFreqSpan(10, 'kHz')  # что бы не сползало
                self.an.setBandwidth(300, 'Hz')
                self.an.averBeginMeas(5)
                self.an.waitEndCmd()
                self.an.markerOneSetMax()
                self.an.setCenterOnMarker()

                self.an.waitEndCmd()

                time.sleep(0.03)

                sch = -1
                for _sp in self._span:
                    sch = sch + 1



                    self.an.setFreqSpan(_sp.span[0], _sp.span[1])
                    self.an.setBandwidth(_sp.rbw[0], _sp.rbw[1])


                    time.sleep(0.03)

                    self.an.averBeginMeas(5)
                    self.an.waitEndCmd()
                    self.an.PhaseNoisePeakSearch()
                    self.an.setDeltaMarker2(_sp.mkr[0], _sp.mkr[1])
                    self.an.waitEndCmd()

                    val = round(float(self.an.getPhaseNoise()), 2)

                    self.arr[sch].x.append(i)
                    self.arr[sch].y[0].append(val)

                self.mpl_plot.emit(self.arr, True, 'Фазовые шумы')
                self.progress_signal.emit(i)

        except:
            raise
        finally:

            self.progress_signal.emit(self.end)

            try:
                self.gen.RFOutOFF()
            except:
                pass

            try: #пишем в лог данные

                self.logfile.write('\n')
                self.logfile.write('\n')

                for i in range(len(self.arr[0].x)):
                    self.logfile.write(str(self.arr[0].x[i]) + ' ')
                    for j in range(len(self.arr)): #бежим по графикам
                        self.logfile.write(str(self.arr[j].y[0][i]) + ' ')
                    self.logfile.write('\n')



                """"
                for plt in self.arr:
                    self.writeToLog('\n')
                    self.writeToLog(plt.title)

                    for i in range(len(plt.x)):
                        self.writeToLog(str(plt.x[i]) + ' ' + str(plt.y[0][i]))
                """

            except:
                raise


            try:
                self.logfile.close()
            except:
                pass


