import visa
import time
from PyQt5.QtCore import *


class CALIBR(QThread):
    status_signal = pyqtSignal(int)
    end_signal = pyqtSignal(bool)

    calibr_arr = None
    level = None
    beg = None
    end = None
    step = None
    gen = None
    an = None

    stop_flg = False

    def __init__(self):
        super(CALIBR, self).__init__()

    def run(self):

        calibr_file = open('out_calibr.txt', 'w')

        try:
            self.gen.RFOutON()
            time.sleep(1)

            while self.beg <= self.end:

                if self.stop_flg:
                    raise Warning

                self.an.beginMeas()
                self.an.setMarkerOne(self.beg)

                tmp1 = '{:10.1f}'.format(self.beg)
                tmp2 = '{:10.2f}'.format(self.an.getMarkerOne() - self.level)

                calibr_file.write(tmp1 + ' ' + tmp2 + '\n')
                self.beg = self.beg + self.step
                self.status_signal.emit(self.beg)

                #self.gen.nextStep()

        except:
            if self.stop_flg:
                print('CALIBR stopped')
            else:
                print('Error in CALIBR()')
        finally:
            calibr_file.close()
            self.gen.RFOutOFF()
            self.end_signal.emit(False)
            self.status_signal.emit(self.end)


    def set_params(self, level, beg, end, step, gen, an):
        self.level = level
        self.beg = beg
        self.end = end
        self.step = step
        self.gen = gen
        self.an = an

    def stop(self):
        self.stop_flg = True

