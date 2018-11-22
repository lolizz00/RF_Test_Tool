from A_Test import A_Test
import time

class ATT_Test(A_Test):
    def __init__(self):
        super(ATT_Test, self).__init__()

    def run(self):


        # -----

        #return

        # ------

        self.stop_flg = False

        # пошел парсинг

        self.att_beg = self.user[0]
        self.att_end = self.user[1]
        self.att_step = self.user[2]
        self.gain= self.user[3]
        self.plot = self.user[4]
        self.nominal_gain = self.user[5]

        # ---- настройка анализатора

        self.an.reset()

        if self.dev.type == 'Panorama':
            self.an.setFreqCent(750)
        else:
            pass

        self.an.traceClearWrite()
        self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setFreqSpan(1, 'MHz')
        self.an.setRefLvl(self.level + 30)

        # ---- настройка генератора

        self.gen.reset()
        self.gen.setFreq(self.beg)
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
        self.writeToLog('Номинальное усиление:      ' + str(self.nominal_gain))
        self.writeToLog('_type:                    ' + 'ATT')

        if self.dev.type == 'Panorama':
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

        self.writeToLog('\n')
        self.writeToLog('ATT')
        self.writeToLog('\n')

        time.sleep(0.5)

        try:
            for freq in range(self.beg, self.end + 1, self.step):

                if self.stop_flg:
                    raise Warning

                self.dev.setFreqReboot(freq)
                self.gen.setFreq(freq)
                self.gen.setLevel(self.level - self.cal_in[freq], 'dBm')
                time.sleep(0.1)


                # работа с эталоном

                sch = -1

                """""
                if self.et_enabled:
                    sch = sch + 1

                    self.dev.setAtt(0)
                    self.an.averBeginMeas(10)
                    self.an.waitEndCmd()
                    self.an.markerOneSetMax()

                    val = round(self.an.getMarkerOne(), 2)
                    val = val - self.cal_out[750]

                    self.plot[sch].x.append(freq)
                    self.plot[sch].y[0].append(val)
                """""


                for att in range(self.att_beg, self.att_end + 1, self.att_step):
                    sch = sch + 1

                    self.dev.setAtt(att)

                    self.an.averBeginMeas(30)
                    self.an.waitEndCmd()
                    self.an.markerOneSetMax()

                    val = round(self.an.getMarkerOne(), 2)
                    val = val - self.cal_out[750]

                    #val = abs((self.level + self.gain[freq]) - val )
                    #val = abs((self.level + 27) - val)

                    if self.nominal_gain:
                        val = (self.level + 25) - val
                    else:
                        val = (self.level + + self.gain[freq]) - val

                    val = round(val , 2)
                    self.plot[sch].x.append(freq)
                    self.plot[sch].y[0].append(val)

                self.mpl_plot.emit(self.plot, True, 'Глубина регулировки коэффициента передачи и шаг регулировки коэффициента передачи конвертера')
                self.progress_signal.emit(freq)



        except:
            raise
        finally:
            self.progress_signal.emit(self.end)

            try:  # пишем в лог данные

                self.logfile.write('\n')
                self.logfile.write('\n')

                for i in range(len(self.plot[0].x)):
                    self.logfile.write(str(self.plot[0].x[i]) + ' ')
                    for j in range(len(self.plot)):  # бежим по графикам
                        self.logfile.write(str(self.plot[j].y[0][i]) + ' ')
                    self.logfile.write('\n')



            except:
                raise

            try:
                self.logfile.close()
            except:
                pass

            try:
                self.gen.RFOutOFF()
            except:
                pass



