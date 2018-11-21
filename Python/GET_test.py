from A_Test import A_Test
import time


class GET_Test(A_Test):

    #генератор
    #анализатор
    #устройство

    get1_en = None
    get1_fix = None
    get1_freq = None

    get2_en = None
    get2_fix = None
    get1_freq = None

    delay = 0.1
    laten = 3

    i_o = None

    def __init__(self):
        super(GET_Test, self).__init__()

    def run(self):

         # ----- рутина


        self.pan = False

        if self.dev.type ==  'Panorama':
            self.pan = True

        self.succ_flg = False
        self.end_signal.emit(True)
        self.stop_flg = False

        self.i_0 = self.user[0]

        self.get1_en = True
        self.get1_fix = self.user[1]
        self.get1_freq = self.user[2]

        self.get2_en = self.user[3]
        self.get2_fix = self.user[4]
        self.get2_freq = self.user[5]

        if self.get2_en:
            self.mpl_set_plot_count.emit(2)
            self.mpl_set_graph_title.emit(0, 'Гетеродин #1')
            self.mpl_set_graph_title.emit(1, 'Гетеродин #2')
            self.y1 = []
            self.y2 = []
        else:
            self.mpl_set_plot_count.emit(1)
            self.mpl_set_graph_title.emit(0, 'Гетеродин #1')
            self.y1 = []

        if self.logfile:
            self.name = self.logfile
            self.logfile = open(self.logfile + '.txt', 'w')

            self.writeToLog('Date:                     ' + time.ctime(time.time()))
            self.writeToLog('Analyzer:                 ' + self.an.fullName)
            self.writeToLog('Тип устройства:           ' + self.dev.type)
            self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
            self.writeToLog('Амплитуда по входу:       ' + str(self.level))

            if self.i_0:
                self.writeToLog('Тип:                   По выходу')
            else:
                self.writeToLog('Тип:                   По входу')

            self.writeToLog('\n')

            if self.pan:
                self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
                self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
                self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))
            self.writeToLog('\n')

            if self.get1_en:
                if self.get1_fix:
                    self.writeToLog('Гетеродин #1, Фиксированная частота: ' + str(self.get1_freq))
                else:
                    self.writeToLog('Гетеродин #1, Динамичная подстройка')
            if self.get2_en:
                if self.get2_fix:
                    self.writeToLog('Гетеродин #2, Фиксированная частота: ' + str(self.get2_freq))
                else:
                    self.writeToLog('Гетеродин #2, Динамичная подстройка')

        self.writeToLog('\n\n\n')




        # --- Анализатор


        #self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setSweep(25, 'ms')
        self.an.setFreqSpan(1, 'KHz')
        self.an.setRef('EXT')
        self.an.setRefLvl(-70)
        self.an.setPreamp(True)

        # -----




        # -----

        try:

            for i in range(self.beg, self.end+1, self.step):

                if self.stop_flg:
                    raise Warning

                self.x.append(i) # частота отстройки

                if self.pan:  # работаем с панорамой
                    self.dev.setFreqReboot(i)
                else:
                    pass

                if self.get1_en: # На самом деле херня, но мало ли гетеродинов будет 5
                    val = 0
                    if self.get1_fix: # если фиксированная частота
                        if self.pan: # работаем с панорамой

                            self.an.setFreqCent(self.get1_freq)
                            self.an.beginMeas()
                            self.an.markerOneSetMax()
                            tmp = self.an.getMarkerOne()

                            if self.cal_flg:        #калибруем если надо
                                tmp = tmp - self.cal_out[round(self.get1_freq)]
                                tmp = round(tmp, 2)
                            else:
                                pass

                            self.y1.append(tmp)

                        else:
                            pass
                    else: #частота не фиксированная, пляшем от устройства
                        if self.pan:
                            freq = self.dev.getLmxFreq()

                            if freq > 6000:  # приборы не позволят
                                continue

                            self.an.setFreqCent(freq)
                            self.an.beginMeas()
                            self.an.markerOneSetMax()
                            tmp = self.an.getMarkerOne()

                            if self.cal_flg:  # калибруем если надо
                                tmp = tmp - self.cal_out[round(freq)]
                                tmp = round(tmp, 2)
                            else:
                                pass

                            self.y1.append(tmp)

                    if not (i % self.laten):
                        self.mpl_plot_signal.emit(0, self.x, self.y1, 'g')

                if self.get2_en: # На самом деле херня, но мало ли гетеродинов будет 5
                    val = 0
                    if self.get2_fix:  # если фиксированная частота
                        if self.pan:  # работаем с панорамой

                            self.an.setFreqCent(self.get2_freq)
                            self.an.beginMeas()
                            self.an.markerOneSetMax()
                            tmp = self.an.getMarkerOne()

                            if self.cal_flg:  # калибруем если надо
                                tmp = tmp - self.cal_out[round(self.get1_freq)]
                                tmp = round(tmp, 2)
                            else:
                                pass

                            self.y2.append(tmp)

                        else:
                            pass
                    else:  # частота не фиксированная, пляшем от устройства
                        if self.pan:
                            freq = self.dev.getLmxFreq()

                            if freq > 6000:  # приборы не позволят
                                continue

                            self.an.setFreqCent(freq)
                            self.an.beginMeas()
                            self.an.markerOneSetMax()
                            tmp = self.an.getMarkerOne()

                            if self.cal_flg:  # калибруем если надо
                                tmp = tmp - self.cal_out[round(freq)]
                                tmp = round(tmp, 2)
                            else:
                                pass

                            self.y2.append(tmp)

                    if not (i % self.laten):
                        self.mpl_plot_signal.emit(1, self.x, self.y2, 'r')

                self.progress_signal.emit(i)
        except:
            if self.stop_flg:
                print('GET() stopped')
            else:
                print('Error in GET()')
                raise
        finally:
            if not self.get2_en: # один гетеродин
                self.mpl_plot_signal.emit(0, self.x, self.y1, 'g')
            else:
                self.mpl_plot_signal.emit(0, self.x, self.y1, 'g')
                self.mpl_plot_signal.emit(1, self.x, self.y2, 'r')


            self.mpl_save_add_graph.emit(self.name)

            if self.get2_en:
                self.writeToLog('Частота подстройки\tУровень сигнала гетеродина #1\tУровень сигнала гетеродина #2')



                for i in range(len(self.x)):

                        if i >= len(self.y1):
                            self.writeToLog(str(self.x[i]) + '\t' + 'N/A' + '\t' + str(self.y2[i]))
                        elif i >= len(self.y2):
                            self.writeToLog(str(self.x[i]) + '\t' + str(self.y1[i]) + '\t' +  'N/A')
                        else:
                            self.writeToLog(str(self.x[i]) + '\t' + str(self.y1[i]) + '\t' + str(self.y2[i]))
            else:
                self.writeToLog('Частота подстройки\tУровень сигнала гетеродина #1')

                for i in range(len(self.x)):
                    if i >= len(self.y1):
                        self.writeToLog(str(self.x[i]) + '\t' + 'N/A')
                    else:
                        self.writeToLog(str(self.x[i]) + '\t' + str(self.y1[i]))


            self.logfile.close()





