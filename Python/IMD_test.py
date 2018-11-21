from A_Test import A_Test
import time
import numpy as np

class IMD_Test(A_Test):

    ip3_flg = True
    ip5_flg = False

    def __init__(self):
        super(IMD_Test, self).__init__()

    def run(self):

      #  self.color = 'red'

       # f1 = self.freq - self.user
       # f2 = self.freq + self.user

      #  l_imp5_fr = 3 * f1 - 2 * f2
      #  r_imp5_fr = 3 * f2 - 2 * f1

        while self.beg <= self.end:
            try:

                if self.stop_flg:
                    raise Warning

                self.an.reset()

                self.an.setFreqCent(self.beg, 'MHz')
                self.an.setFreqSpan(self.user + 100, 'MHz')
                self.an.singleSweepMode()
                self.an.setSweep(50, 'ms')
                self.an.setMarkerOne(self.beg)
                self.an.setRefLvl(self.level + 25, 'dBm')

                self.gen.reset()

                if self.cal_flg:
                    self.gen.setLevel(self.level - self.cal_in[round(self.beg)])
                else:
                    self.gen.setLevel(self.level)

                self.gen.setFrequency(self.beg)
                self.gen.setFreqTwoTone(self.user, 'MHz')
                self.gen.enableMod()
                self.gen.enableTwoTone(True)
                self.gen.RFOutON()

                time.sleep(1)
                self.an.beginMeas()

                if self.ip3_flg:
                    self.an.enableTOI(True)
                    res = self.an.getTOI()
                    self.x.append(self.beg)
                    self.y.append(res)

                if self.ip5_flg:
                    pass

                self.beg = self.beg + self.step

                if self.plot_flg:
                    self.plot_signal.emit(self.x, self.y, self.color)
                self.progress_signal.emit(self.beg)
                time.sleep(0.5)

            except:
                if self.stop_flg:
                    pass
                    #  print('PIO stopped')
                else:
                    print('Error in IMD()')
                    raise
            finally:
                self.gen.RFOutOFF()
                self.plot_signal.emit(self.x, self.y, self.color)
                self.progress_signal.emit(self.end)
                self.end_signal.emit(False)
