from A_Test import A_Test
import time

class SIF_Test(A_Test):
    def __init__(self):
        super(SIF_Test, self).__init__()

    def run(self):

        self.stop_flg = False

        # пошел парсинг

        self._if = self.user[0]
        self.plot = self.user[1]
        self.gain = self.user[2]

        # ---- настройка анализатора
        self.an.reset()

        if self.dev.type == 'Panorama':
            self.an.setFreqCent(750)
        else:
            pass

        self.an.setRefLvl(-30, 'dBm')
        self.an.setPreamp(True)
        self.an.traceClearWrite()
        self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setFreqSpan(10, 'kHz')

        # ---- настройка генератора

        self.gen.reset()
        self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')
        self.gen.RFOutON()

        # ---- запись в лог

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Span:                      ' + str(self.span))
        self.writeToLog('Тип устройства:           ' + self.dev.type)
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('_type:                    ' + 'SIF')

        if self.dev.type == 'Panorama':
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('SIF')
        self.writeToLog('\n')

        self.last = []

        for i in range(len(self._if)):
            self.last.append(0)



        # ------

        try:
            for i in range(self.beg, self.end + 1, self.step):

                if self.stop_flg:
                    raise Warning

                self.dev.setFreqReboot(i)

                # читаем ПЧ

                sch = -1
                for freq in self._if:
                    sch = sch + 1

                    self.gen.setLevel(self.level - self.cal_in[freq], 'dBm')
                    self.gen.setFreq(freq)

                    self.an.setFreqCent(freq, 'MHz')

                    self.an.averBeginMeas(10)
                    self.an.waitEndCmd()

                    self.an.markerOneSetMax()

                    __val = round(self.an.getMarkerOne(), 2)
                    __val = __val - self.cal_out[freq]

                    res = self.level + self.gain[i] - __val

                    if (freq * 2 == i) or (freq * 3 == i) or (freq == i):
                        res = self.last[sch]

                    res = round(res, 2)

                    self.last[sch] = res

                    self.plot[sch].x.append(i)
                    self.plot[sch].y[0].append(res)

                # рутина

                self.mpl_plot.emit(self.plot, True, 'Подавление сигнала ПЧ')
                self.progress_signal.emit(i)

        except:
            pass
        finally:
            self.progress_signal.emit(self.end)

            try:
                self.gen.RFOutOFF()
            except:
                pass

            try:  # пишем в лог данные

                self.logfile.write('\n')
                self.logfile.write('\n')

                for i in range(len(self.plot[0].x)):
                    self.logfile.write(str(self.plot[0].x[i]) + ' ')
                    for j in range(len(self.plot)):  # бежим по графикам
                        self.logfile.write(str(self.plot[j].y[0][i]) + ' ')
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

