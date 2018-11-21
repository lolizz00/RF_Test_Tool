from A_Test import A_Test
import time
import numpy as np
import shutil

# ------------
from matplotlib import ticker, cm
import matplotlib.pyplot as plt
from start import MPL_Plot
# ------------



def toInt(val):
    if int(val) != val:
        val = int(val) + 1
        return val
    else:
        return int(val)



class BW_Test(A_Test):


    def __init__(self):
        super(BW_Test, self).__init__()

    def saveSpec(self, X, Y, Z):
        self.addAray(X)
        self.resfile.write('\n\n---\n\n')
        self.addAray(Y)
        self.resfile.write('\n\n---\n\n')
        self.addAray(Z)

    def calcBW(self,n ,x, y):

        maax = max(y)

        # -------

        val = maax - n

        val_l = min(y[0:y.index(maax)], key=lambda t: abs(t - val))
        val_l = y.index(val_l)
        val_l = x[val_l]

        val_r = min(y[y.index(maax):len(y)], key=lambda t: abs(t - val))
        val_r = y.index(val_r)
        val_r = x[val_r]

        res = round(val_r - val_l, 2)

        return [val_l, val_r, res]

    def addAray(self, arr):

        rows = arr.shape[0]
        cols = arr.shape[1]

        for i in range(rows):
            for j in range(cols):
                self.resfile.write( str(arr[i, j]) + ' ')
            self.resfile.write('\n')


    def run(self):

        self.specFlg = self.user[2][0]


        # ---- дополнительные графики

        self.bias = MPL_Plot() # нижняя граница
        self.bias.title = 'Смещение центра полосы пропускания'
        self.bias.col = 'g'
        self.bias.y.append([])

        self.bw6 = MPL_Plot()
        self.bw6.title = 'Полоса пропускания по уровню -6 dB'
        self.bw6.col = 'y'
        self.bw6.y.append([])
        self.bw6.y.append([])

        self.bw3 = MPL_Plot()
        self.bw3.title = 'Полоса пропускания по уровню -3 dB'
        self.bw3.col = 'b'
        self.bw3.y.append([])
        self.bw3.y.append([])

        # ---- пошла оч сложная математика для моего моска

        self.space_step = self.user[1]

        self.space = self.user[0] / 2

        x = np.arange(self.beg, self.end + 1, self.step)
        y = np.arange(-self.space, self.space + 1, self.space_step)

        self._Y, self._X = np.meshgrid(y, x)

        self._Z = np.zeros((toInt((self.end - self.beg) / self.step) + 1,  toInt(self.space * 2 / self.space_step) + 1))

        # ----- Ицициализация всякой фигни

        self.succ_flg = False
        self.end_signal.emit(True)
        self.stop_flg = False



        try:

            if self.logfile:
                self.name = self.logfile
                self.logfile = open(self.logfile + '.txt', 'w')


                self.writeToLog('Date:                     ' + time.ctime(time.time()))
                self.writeToLog('Generator:                ' + self.gen.fullName)
                self.writeToLog('Analyzer:                 ' + self.an.fullName)
                self.writeToLog('Тип устройства:           ' + self.dev.type)
                self.writeToLog('Тип теста:                ' +  'Полоса пропускания')
                self.writeToLog('Использование калибровки: ' + str(self.cal_flg))
                self.writeToLog('Амплитуда по входу:       ' + str(self.level))
                self.writeToLog('Диапазон частот:          ' + str(self.beg) + ' - ' + str(self.end))
                self.writeToLog('Шаг:                      ' + str(self.step))
                self.writeToLog('Разнос частот:            ' + str(self.space))
                self.writeToLog('Шаг разноса частот:       ' + str(self.space_step))
                self.writeToLog('_type:                    ' + 'plotOverSpec'  )

                if self.dev.type:
                    self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
                    self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
                    self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))

                self.writeToLog('\n')

                if self.specFlg:
                    self.resfile = open(self.name + '.spec', 'w')
                # --------------- Анализатор

                self.an.reset()

                if self.dev.type == 'Panorama':
                    self.an.setFreqCent(750, 'MHz')
                    self.an.setFreqSpan(800, 'MHz')
                    pass
                else:
                    pass

                self.an.setSweep(25, 'ms')
                self.an.singleSweepMode()

                if self.dev.type == 'Panorama':
                    if self.dev.getLNA():
                        self.an.setRefLvl(self.level + 45, 'dBm')
                    else:
                        self.an.setRefLvl(self.level + 30, 'dBm')

                else:
                    self.an.setRefLvl(self.level + 15, 'dBm')
                    pass

                #self.an.setTracAver(True)

                # ----------------- Генератор

                self.gen.reset()

                if self.cal_flg:
                    self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')
                else:
                    self.gen.setLevel(self.level)

                self.gen.setFreq(self.beg)

                self.gen.RFOutON()

                time.sleep(3)


        except:
            pass  # ------- сюда обработка ошибки при инициализации
            raise
            return

        sch = 0



        if self.specFlg:
            self.mpl_set_spec_count.emit()

        self.mpl_set_spec_title.emit('Полоса пропускания')

        # ------- Пошло веселье

        self.x = []
        self.y1 = []
        self.y2 = []
        self.y3 = []

        plt_sch = 0

        try:
            for ind_x, i in np.ndenumerate(self._X[:,0]):

                if self.stop_flg:
                    raise Warning

                #self.x.append(i)

                if self.dev.type == 'Panorama':
                    self.dev.setFreqReboot(i)

                _x = []
                _y = []

                for ind_y, j in np.ndenumerate(self._Y[0]):

                    freq = i + j

                    self.gen.setFreq(freq)

                    if self.cal_flg:
                        self.gen.setLevel(self.level - self.cal_in[freq], 'dBm')
                    else:
                        self.gen.setLevel(self.level)

                        # ----- замеры

                    #time.sleep(0.05)

                    self.an.beginMeas()

                    #time.sleep(0.05)

#                    self.an.averBeginMeas()
                    self.an.markerOneSetMax()
                    tmp = self.an.getMarkerOne()

                    _x.append(freq)

                    if self.cal_flg:
                        if self.dev.type == 'Panorama':
                            _y.append(tmp - self.cal_out[750])
                            if self.specFlg:
                                self._Z[ind_x, ind_y] = tmp - self.cal_out[750]
                        else:
                            _y.append(tmp - self.cal_out[freq])
                            if self.specFlg:
                                self._Z[ind_x, ind_y] =  tmp - self.cal_out[freq]
                    else:
                        _y.append(tmp)
                        self._Z[ind_x, ind_y] = tmp



                # --- вычисление смещения центра полосы
                tmp = max(_y)
                tmp = _y.index(tmp)
                tmp = _x[tmp]
                tmp = tmp - i

                # -----

                self.bias.x.append(i)
                self.bw3.x.append(i)
                self.bw6.x.append(i)


                self.bias.y[0].append(tmp)

                tmp3 = self.calcBW(3, _x, _y)
                tmp6 = self.calcBW(6, _x, _y)

                self.bw3.y[0].append(tmp3[0] - i)
                self.bw3.y[1].append(tmp3[1] - i)

                self.bw6.y[0].append(tmp6[0] - i)
                self.bw6.y[1].append(tmp6[1] - i)



                plt_sch = plt_sch + 1

                if plt_sch == 1:
                    plt_sch = 0

                    self.mpl_plot_over_spec.emit([self.bias, self.bw3, self.bw6])


                self.progress_signal.emit(i)





        except:
            if self.stop_flg:
                print('BW stopped')
            else:
                print('Error in BW()')
                raise
        finally:


                if self.gen:
                    self.gen.RFOutOFF()



                if self.specFlg:
                    self.saveSpec(self._X, self._Y, self._Z)
                    self.spec_signal.emit(self._X, self._Y, self._Z)


                self.writeToLog('\n')
                self.writeToLog('BIAS_CENT')
                for  i in range(len(self.bias.x)):
                    self.writeToLog('Freq:' + str(self.bias.x[i]) + ' Bias: ' + str(self.bias.y[0][i]))

                self.writeToLog('\n')
                self.writeToLog('BW_3')
                for i in range(len(self.bw3.x)):
                    self.writeToLog('Freq:' + str(self.bw3.x[i]) +
                                    '  Bw_3_freq_vals: ' + str(self.bw3.y[0][i]) + '  '+  str(self.bw3.y[1][i]) )
                self.writeToLog('\n')
                self.writeToLog('BW_6')
                for i in range(len(self.bw6.x)):
                    self.writeToLog('Freq:' + str(self.bw6.x[i]) +
                                    '  Bw_3_freq_vals: ' + str(self.bw6.y[0][i]) + '  ' + str(self.bw6.y[1][i]))


                self.logfile.close()

                if self.specFlg:
                    self.mpl_save_spec.emit(self.name)
                    self.resfile.close()
























