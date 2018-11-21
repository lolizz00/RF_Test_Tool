from structs import IQData
from PyQt5.QtCore import *
import time
from structs import IQData
import bitstring
import numpy as np
import math
import random

from  bitstring import ConstBitStream

class FileReader(QThread):

    # сигналы-слоты

    plot_signal = pyqtSignal(IQData)  # сигнал построения графика, с углом
    end_signal = pyqtSignal(int)     # сигнал окончания чтения, с кол-вом считанным точек

    # -----


    def __init__(self):
        super(FileReader, self).__init__()

        self.stop_flg = False



        self.file = None  # файл с данными
        self.endian = None
        self.tout = None

    def setParams(self, _file, _endian, _tout=None):
        self.file = _file
        self.endian = _endian
        self.tout = _tout

    def stop(self):
        self.stop_flg = True

    def setUpdateTime(self, val):
        self.tout = val

    def run(self):




        self.stop_flg = False
        sch = 0

        try:

            stream = ConstBitStream(filename=self.file)

            while True and not self.stop_flg:

                I = None
                Q = None

                # ----- читаем I
                packet = stream.read(16)

                if self.endian == 'Big Endian':
                    I = packet.unpack('intbe:16')[0]
                elif self.endian == 'Little Endian':
                    I = packet.unpack('intle:16')[0]

                # ----- читаем Q

                packet = stream.read(16)

                if self.endian == 'Big Endian':
                    Q = packet.unpack('intbe:16')[0]
                elif self.endian == 'Little Endian':
                    Q = packet.unpack('intle:16')[0]

                # ----- вычисляем

                val = math.atan2(Q, I)

                val = val * 180 / np.pi


                val = (val + 360) % 360


                val = round(val)

                struct = IQData()


                struct.I = I
                struct.Q = Q
                struct.DEG = val


                if 0:
                    self.plot_signal.emit(struct)
                else:
                    for i in range(random.randint(1,5)):
                        self.plot_signal.emit(struct)
                        time.sleep(self.tout / 1000)

                if self.tout:
                    time.sleep(self.tout / 1000)

                sch = sch + 1

        except:
            raise
            pass
        finally:
            self.end_signal.emit(sch)


