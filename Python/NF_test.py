from A_Test import A_Test
import time


class NF_Test(A_Test):
    def __init__(self):
        super(NF_Test, self).__init__()

    def run(self):

        self.stop_flg = False

        self.plot = self.user[1]
        self.gain = self.user[0]

        # -----

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

        self.writeToLog('Date:                     ' + time.ctime(time.time()))
#        self.writeToLog('Generator:                ' + self.gen.fullName)
        self.writeToLog('Analyzer:                 ' + self.an.fullName)
        self.writeToLog('Span:                      ' + str(self.span))
        self.writeToLog('Тип устройства:           ' + self.dev.type)
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('_type:                    ' + 'NF')

        if self.dev.type == 'Panorama':
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('NF')
        self.writeToLog('\n')

        # ----- инициализация Анализатора

        self.an.reset()

        if self.dev.type == 'Panorama':
            self.an.setFreqCent(750)
        else:
            pass

        self.an.setPreamp(True)

        self.an.setRefLvl(-60, 'dBm')
        self.an.traceClearWrite()
        self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setSweep(5)
        self.an.setFreqSpan(5, 'MHz')
        self.an.setBandwidth(1, 'MHz')
        self.an.enableNoiseMeasMarkX(1)
        self.an.enableDetectorRMS()

        #self.an.getNoiseMarkX()

        time.sleep(0.5)

        try:
            for i in range(self.beg, self.end + 1, self.step):

                if self.stop_flg:
                    raise Warning

                self.dev.setFreqReboot(i)

                # --- замеры

                self.an.averBeginMeas(5)
                self.an.waitEndCmd()

                #self.an.markerOneSetMax()
                self.an.setMarker1PeakMIN()
                val = self.an.getNoiseMarkX(1)

                nf = 174 + val - self.gain[i]

                #nf = (-174 + self.gain[i] - val)*-1

                #(-174 + float(gain) - float(readStr)) * -1

                self.plot.x.append(i)
                self.plot.y[0].append(round(nf, 2))


                # --- рутина

                self.mpl_plot.emit([self.plot], True, 'Коэффициент шума')
                self.progress_signal.emit(i)

        except:
            raise
        finally:
            self.progress_signal.emit(self.end)

            try:  # пишем в лог данные
                self.logfile.write('\n')
                self.logfile.write('\n')

                for i in range(len(self.plot.x)):
                   self.logfile.write(str(self.plot.x[i]) + ' ' + str(self.plot.y[0][i]) + '\n')
            except:
                pass

            try:
                self.logfile.close()
            except:
                pass


