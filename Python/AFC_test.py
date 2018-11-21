from A_Test import A_Test
import time
import subprocess
# 70 - 50 = +20, -40+
import os
import signal
from subprocess import PIPE
from ctypes import *

class AFC_Test(A_Test):
    def __init__(self):
        super(AFC_Test, self).__init__()

    def run(self):

        self.bw = self.user[2]
        self.bf = self.user[3]
        self.sdr = False
        self.pan = False

        if self.user[0] == 'USRP':
            self.sdr = True
        elif self.user[0] == 'Панорама':
            self.pan = True

        if self.sdr:

            try:
                process = subprocess.Popen('C:\\Program Files\\UHD\\bin\\uhd_find_devices', stdout=subprocess.PIPE)
                data = process.communicate()
                sn_str = str(data[0])
                sn = sn_str.rindex('serial: ')
                sn = sn_str[sn + 8:sn + 15]

                self.dll = cdll.LoadLibrary('uhd_dll.dll')
                self.dll.set.argtypes = [c_double]
                self.dll.init()
                time.sleep(7)
                self.logfile = open(self.user[1] + '/SN_' + sn + '_FR_' + str(int(self.beg)) + '_' + str(int(self.end)) + 'MHz_90dB.txt', 'w')

            except:
                raise

            self.an.reset()
            self.an.setRefLvl(self.level + 35, 'dBm')
            self.an.setFreqSpan(450, 'MHz')
            self.an.singleSweepMode()
            self.an.setSweep(15, 'ms')

            try:
                while self.beg <= self.end:

                    if self.stop_flg:
                        raise Warning

                    self.dll.set(c_double(self.beg * 1000000))
                    time.sleep(0.1)
                    self.dll.run()
                   # time.sleep(0.2)
                    self.an.setFreqCent(self.beg, 'MHz')
                    self.an.beginMeas()
                   # self.an.setMarkerOne(self.beg)
                    self.an.markerOneSetMax()
                    time.sleep(0.1)

                    tmp = self.an.getMarkerOne()
                    tmp = tmp - self.cal_out[round(self.beg)]

                    #if tmp <-50:
                     #  continue

                    self.x.append(self.beg)
                    self.y.append(tmp)

                    self.progress_signal.emit(self.beg)

                    self.beg = self.beg + self.step
                    if self.plot_flg:
                        self.plot_signal.emit(self.x, self.y, self.color)
            except:
                pass
            finally:
                for i in range(len(self.x)):
                    self.writeToLog('Freq: ' + str(self.x[i]) + ' Amp:' + str(round(self.y[i], 2)))


                self.logfile.close()
                self.progress_signal.emit(self.end)
                self.plot_signal.emit(self.x, self.y, self.color)

                return

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

        if self.pan:
            self.writeToLog('Аттенюатор:               ' + str(self.dev.getAtt()))
            self.writeToLog('Источник опорной частоты: ' + self.dev.getRef())
            self.writeToLog('МШУ:                      ' + str(self.dev.getLNA()))
        self.writeToLog('_type:                        ' + 'AFC')
        self.writeToLog('\n')
        self.writeToLog('AFC')
        self.writeToLog('\n')
       # self.color = 'red'

        self.an.reset()

        if not self.pan:
            self.an.setFreqCent(self.beg, 'MHz')
        else:
            self.an.setFreqCent(750, 'MHz')
            self.an.setMarkerOne(750)

            if self.bw:
                self.dev.setFreqReboot((self.end + self.beg) / 2 )
                self.writeToLog('Частота настройки: ' + str((self.end + self.beg) / 2))
                self.plot_flg = False

        if not self.bf:
         self.an.setFreqSpan(10, 'MHz')
         self.an.singleSweepMode()

        else:
            self.an.setFreqSpan(int(self.user[4]), 'kHz')
            self.an.setTracAver(True)
            self.plot_flg = False



        self.an.setSweep(50, 'ms')

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
            self.gen.freqSweepMode()
        elif self.gen.type == 'N5182A':
            self.gen.setFrequency(self.beg)

        if self.cal_flg:
            self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')
        else:
            self.gen.setLevel(self.level)

        self.gen.RFOutON()

        time.sleep(3)

        try:
            while self.beg <= self.end:

               # time.sleep(1)

                if self.stop_flg:
                    raise Warning

                if self.cal_flg:
                    self.gen.setLevel(self.level - self.cal_in[round(self.beg)], 'dBm')
                else:
                    self.gen.setLevel(self.level)

                if not self.pan:
                    self.an.setFreqCent(self.beg, 'MHz')
                    self.an.setMarkerOne(self.beg)
                else:
                    if not self.bw:
                        self.dev.setFreqReboot(self.beg)

                if not self.bf:
                    self.an.beginMeas()
                else:
                    time.sleep(8)

                self.an.markerOneSetMax()
                tmp = self.an.getMarkerOne()
                self.x.append(self.beg)

                if self.bf:
                    tmp = self.an.getAllMax()
                    tmp = sum(1 for x in tmp if x > (self.level - int(self.user[5])))

                    if tmp > 1:
                        self.savescreen_an_signal.emit(str(self.beg) + 'MHz.PNG', self.path)
                        self.writeToLog('Detect: ' + str(self.beg))
                        time.sleep(8)

                if self.cal_flg:
                    if not self.pan:
                        self.y.append(tmp - self.cal_out[round(self.beg)])
                    else:
                        self.y.append(tmp - self.cal_out[750])
                else:
                    self.y.append(tmp)

                self.beg = self.beg + self.step

                if self.gen.type == 'SMA100A':
                    self.gen.nextStep()
                elif self.gen.type == 'N5182A':
                    self.gen.setFrequency(self.beg)

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color, True)

                self.progress_signal.emit(self.beg)

                #time.sleep(0.1)



        except:
            if self.stop_flg:
                print('AFC stopped')
            else:
                print('Error in AFC()')
        finally:
            self.gen.RFOutOFF()

            if self.bw:
                maax = max(self.y)

                # -------

                val_6 = maax - 6

                val_6_l = min(self.y[0:self.y.index(maax)], key=lambda x:abs(x - val_6))
                val_6_l = self.y.index(val_6_l)
                val_6_l = self.x[val_6_l]

                val_6_r = min(self.y[self.y.index(maax):len(self.y)], key=lambda x: abs(x - val_6))
                val_6_r = self.y.index(val_6_r)
                val_6_r = self.x[val_6_r]


                self.plot_signal.emit(self.x, self.y, 'blue', True)

                self.addline_signal.emit(True,  maax,    'red')
                self.addline_signal.emit(False, val_6_l, 'red')
                self.addline_signal.emit(False, val_6_r, 'red')

                self.log_signal.emit('Полоса пропускания по уровням -6 дБ: ' + str(round( val_6_r - val_6_l, 2)))
                self.writeToLog('Полоса пропускания по уровням -6 дБ: ' + str(round(val_6_r - val_6_l, 2)))

                self.savescreen_signal.emit(self.name + "_-6")

                # -----------------


                val_3 = maax - 3

                val_3_l = min(self.y[0:self.y.index(maax)], key=lambda x: abs(x - val_3))
                val_3_l = self.y.index(val_3_l)
                val_3_l = self.x[val_3_l]

                val_3_r = min(self.y[self.y.index(maax):len(self.y)], key=lambda x: abs(x - val_3))
                val_3_r = self.y.index(val_3_r)
                val_3_r = self.x[val_3_r]

                self.plot_signal.emit(self.x, self.y, 'blue', True)

                self.addline_signal.emit(True, maax, 'red')
                self.addline_signal.emit(False, val_3_l, 'red')
                self.addline_signal.emit(False, val_3_r, 'red')

                self.log_signal.emit('Полоса пропускания по уровням -3 дБ: ' + str(round(val_3_r - val_3_l, 2)))
                self.writeToLog('Полоса пропускания по уровням -3 дБ: ' + str(round(val_3_r - val_3_l, 2)))

                self.savescreen_signal.emit(self.name + "_-3")

            elif self.bf:
                pass
            else:
                for i in range(len(self.x)):
                    self.writeToLog('Freq: ' + str(self.x[i]) + ' Amp:' + str(round(self.y[i], 2)))

                self.plot_signal.emit(self.x, self.y, self.color, True)

                self.savescreen_signal.emit(self.name)

            time.sleep(1)
            if self.logfile:
                self.logfile.close()
            self.end_signal.emit(False)
            self.progress_signal.emit(self.end)
            self.log_signal.emit('READY!')