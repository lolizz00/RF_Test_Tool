from A_Test import A_Test
import time
import numpy as np

class MIRR_Test(A_Test):

    def save3D(self, x, y, z0, z1):

        for i in range(len(x)):
            for j in range(len(x[i])):
                self.resfile.write(str(x[i][j]) + ' ' + str(y[i][j]) + ' ' + str(z0[i][j])  + ' ' + str(z1[i][j]) + '\n')



    def __init__(self):
        super(MIRR_Test, self).__init__()

    def run(self):


        self.pan = False

        if self.dev.type == 'Panorama':
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
        self.writeToLog('Тип устройства:           ' + self.dev.type)
        self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
        self.writeToLog('Амплитуда по входу:       ' + str(self.level))
        self.writeToLog('Уровень сигнала:          ' + str(self.level))
        if self.pan:
           self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
           self.writeToLog('Источник опорной частоты: ' + str((self.dev.getRef())))
           self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))
           pass

        self.writeToLog('\n')

        self.resfile = open(self.name + '.3d', 'w')

        # ----- Анализатор

        self.an.reset()

        self.an.setFreqCent(750, 'MHz')
        self.an.setFreqSpan(450, 'MHz')
        self.an.setRefLvl(-30)
        self.an.setPreamp(True)
        self.an.setTracAver(True)
        self.an.singleSweepMode()
        self.an.setSweep(2.5)



        # ----- Генератор

        self.gen.reset()
        self.gen.setLevel(self.level - self.cal_in[self.beg])
        self.gen.setFreq(self.beg)
        self.gen.RFOutON()

        self.offs = 350

        # ----- Формируем массивы

        self.x = []     #
        self.y = []     #
        self.z0 = []    #   массив значений в точке
        self.z1 = []    #   массив мощности несущей в точке

        try:

            self.sch = 0

            for i in range(500, 2500+1, 50):

                self.dev.setFreqReboot(i)

                p0 = None # эталон

                self.gen.setLevel(self.level - self.cal_in[round(i)], 'dBm')
                self.gen.setFreq(i)

                self.an.setRefLvl(self.level + 45)
                #self.an.beginMeas()
                self.an.averBeginMeas()

                self.an.markerOneSetMax()
                p0 = self.an.getMarkerOne()

                #p0 = np.random.randint(-35, -30)


                p0 = round(p0 - self.cal_out[round(self.an.getMarkerOneFreq() / 1000000)], 2)

                self.x.append([])
                self.y.append([])
                self.z0.append([])
                self.z1.append([])




                for j in range(1700, 1900+1, 10):

                    if self.stop_flg:
                        raise Warning

                    if (j > i - self.offs) and (j < i + self.offs):
                        continue

                    if j > 6000:
                        continue

                    gar_freq2 = 750 + (i - j * 2)
                    gar_freq3 = 750 + (i - j * 3)

                    self.an.setRefLvl(-40)

                    self.gen.setFreq(j)
                    self.gen.setLevel(self.level - self.cal_in[round(j)], 'dBm')

                    #self.an.beginMeas()
                    self.an.averBeginMeas()
                    self.an.markerOneSetMax()

                    val = self.an.getMarkerOne()
                    fr = round(self.an.getMarkerOneFreq() / 1000000)

                    if (fr >  gar_freq2 - 5) and (fr < gar_freq2 + 5):
                        self.an.getNextMax()
                        val = self.an.getMarkerOne()

                    if (fr > gar_freq3 - 5) and (fr < gar_freq3 + 5):
                        self.an.getNextMax()
                        val = self.an.getMarkerOne()

                    val = val - self.cal_out[round(self.an.getMarkerOneFreq() / 1000000)]



                    #val = val - p0

                    val = round(val, 1)

                    self.x[len(self.x) - 1].append(i)
                    self.y[len(self.x) - 1].append(j)
                    self.z0[len(self.x) - 1].append(val)
                    self.z1[len(self.x) - 1].append(p0)


                self.progress_signal.emit(i)


        except:
            raise

        finally:

            try:
                self.gen.RFOutON()
            except:
                pass

            try:
                self.save3D(self.x, self.y, self.z0, self.z1)
                self.resfile.close()
            except:
                pass

            try:
                if self.logfile:
                    self.logfile.close()
            except:
                pass


            self.mpl_plot_3d.emit(self.name + '.3d')



            self.end_signal.emit(False)
            self.progress_signal.emit(self.end)
            self.log_signal.emit('READY!')


