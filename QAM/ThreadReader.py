from structs import IQData
from PyQt5.QtCore import *
import time
from structs import IQData
import bitstring
import numpy as np
import math
import random
from ctypes import *
import os

from  bitstring import ConstBitStream
from  bitstring import BitArray
from  bitstring import Bits
from  bitstring import BitStream

from  structs import IQData_arr

class ThreadReader(QThread):

    plot_signal = pyqtSignal(list)  # сигнал построения графика, с углом
    end_signal = pyqtSignal(int)     # сигнал окончания чтения, с кол-вом считанным точек
    log_signal = pyqtSignal(str)

    # --- Параметры

    INFINITE                    = int('0xFFFF', 16)
    PSHOW_MAX_CHANNEL_NUM       = 32
    IQ_MAX_NUM                  = 1024 * 1024

    # ---


    def __init__(self):
        super(ThreadReader, self).__init__()

        self.stop_flg = False

        self.file = None  # файл с данными
        self.endian = None
        self.tout = None




        self.dll = None


        # --- для dll
        self.channels_num = c_uint32(0)

        self.iq_buffer = (c_uint16 * self.IQ_MAX_NUM * 2)()
        self.phase_add = (c_int16  * self.PSHOW_MAX_CHANNEL_NUM)()

        self.iq_max_num = c_uint32(self.IQ_MAX_NUM)
        self.timeout_ms = c_uint32(self.INFINITE)

        self.dll_ret_vals = {}

        self.dll_ret_vals[-1] = 'PSHOW_ERR_TIMEOUT'
        self.dll_ret_vals[-2] = 'PSHOW_ERR_VER'
        self.dll_ret_vals[-3] = 'PSHOW_ERR_NEW_SESSION'
        self.dll_ret_vals[-4] = 'PSHOW_ERR_BUFFER_TO_SMALL'

    def setUpdateTime(self, val):
        self.tout = val

    def setParams(self, _dll, _endian, _tout=None):
        self.file = _dll
        self.endian = _endian
        self.tout = _tout

    def stop(self):
        self.stop_flg = True

    def discDll(self):
        pass

    def connectDLL(self):

        try:
            self.dll = cdll.LoadLibrary(self.file)



            # --- настрока типов

            self.dll.pshow_get.restype = c_int

            self.dll.pshow_get.argtypes = \
            [
                POINTER(c_uint32), # channels_num

                POINTER(c_int32),  # phase_add
                POINTER(c_uint16), # data

                c_uint32,          # iq_max_num
                c_uint32           # timeout_ms
            ]


            # ---


        except Exception as e:
            #print(str(e))
            self.log_signal.emit('DLL exit with err: ' + str(e))
            return -1

        return 0

    def arrToStream(self, arr, size):
        stream = bytearray(arr)
        stream = stream[:size]
        stream = BitStream(stream)

        return stream

    def run(self):
        self.stop_flg = False
        sch = 0

        try:
            while True and not self.stop_flg:

                I = None
                Q = None
                DEG = None


                # ---

                ret = c_int(0)
                count = 0


                ret = self.dll.pshow_get(
                                         POINTER(c_uint32)(self.channels_num),
                                         POINTER(c_int32)(self.phase_add),
                                         POINTER(c_uint16)(self.iq_buffer),
                                         self.iq_max_num,
                                         self.timeout_ms
                )




                count = ret                     # количество точек по каналам
                chan = self.channels_num.value  # количество каналов

                #print('Count:' + str(count))
                #print('Chan:' + str(chan))

                if count > 0: # все окей

                    # --- конвертируем в поток битов





                    vals_stream = self.arrToStream(self.iq_buffer, (count * 2 * 2) * chan) #два значения по два байта


                    vals = bytearray(self.iq_buffer)

                    sch = 0


                    points = []


                    for i in range(count): # бежим по выданным точка
                        for j in range(chan): # бежим по выданным каналам

                            if self.endian == 'Big Endian':
                                I, Q = vals_stream.read('intbe:16, intbe:16')
                            elif self.endian == 'Little Endian':
                                I, Q = vals_stream.readlist('intle:16, intle:16')

                            deg = math.atan2(Q, I)
                            deg =  deg * 180 / np.pi
                            deg = (deg + 360) % 360
                            deg = round(deg)



                            points.append(IQData())

                            points[-1].chan = j

                            points[-1].I = I
                            points[-1].Q = Q

                            points[-1].DEG = deg
                            points[-1].RAD = round(math.radians(deg), 2)

                            points[-1].AMP =  round(\
                            math.sqrt( (points[-1].Q * points[-1].Q) +(points[-1].I * points[-1].I)) \
                                )

                    if 1:  # отладка, что бы повторялась
                        for i in range(random.randint(1, 5)):
                            self.plot_signal.emit(points)
                    else:
                        self.plot_signal.emit(points)

                    if self.tout:
                        time.sleep(self.tout / 1000)

                    #sch = sch + 1

                elif 0 == ret: #хзхзхз
                    pass
                    continue
                else:  # dll кинула ошибку
                    self.log_signal.emit(self.dll_ret_vals[ret])
                    time.sleep(1) # что бы не заваливать буфер лога
                    continue

                # ---



        except:
            raise
            pass
        finally:
            self.end_signal.emit(0)
