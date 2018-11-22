# как же не хватает структур из си
import numpy as np
from ctypes import *

# рутина в отдельный класс
class IQData_arr:
    def __init__(self, _size=50):
        self.points = []
        self.size = _size

        self.updateLen()

    def __len__(self):
        return self.len


    # получаем номера доступных каналов
    def getChans(self):

        chans  = []

        chans = [val.chan for val in self.points]

        chans = np.unique(np.array(chans))

        return chans

    #количество одинаковых точек по градусам
    def countbyDEG(self, _chan):

        deg_arr = self.getArr('DEG', _chan,_np=True)

        x, y = np.unique(deg_arr, return_counts=True)

    # получение класс с только уникальными точками
    # по градусам+амлитудам и каналам
    def getUniqDEGAMP(self):
        tmp = IQData_arr()


        return tmp


    # получение класс с только уникальными точками
    # по градусам и каналам
    def getUniqDEG(self, ):
        tmp = IQData_arr()

        return tmp

    # получение массивов для графиков
    def getArr(self, type, _chan, _np=False):

        res = []

        if type == 'I':
            res = [val.I for val in self.points if val.chan == _chan]
        elif type == 'Q':
            res = [val.Q for val in self.points if val.chan == _chan]
        elif type == 'DEG':
            res = [val.DEG for val in self.points if val.chan == _chan]
        elif type == 'RAD':
            res = [val.RAD for val in self.points if val.chan == _chan]
        elif type == 'AMP':
            res = [val.AMP for val in self.points if val.chan == _chan]

        if _np:
            res = np.array(res)

        return res

    def updateLen(self):
        self.len = len(self.points)

    # --- размер очереди
    def setSize(self, _size):
        self.size = _size

    # --- удаление точек
    def clearPoints(self):
        self.points = []
        self.updateLen()


    #у нас тут вообще то очередь, молодой человек!
    def changeLen(self):
        while len(self.points) > self.size:
            self.points.pop(0)

    def addPoints(self, pts):
        self.points = self.points + pts

        self.changeLen()
        self.updateLen()

    # --- добавление точки с учетом очереди
    def addPoint(self, pt):

        self.points.append(pt)

        self.changeLen()
        self.updateLen()

# почему бы не считать все сразу, почти структура
class IQData:
    def __init__(self):
        self.I = None
        self.Q = None

        self.DEG = None
        self.RAD = None

        self.AMP = None

        self.chan = None

    def __str__(self):
        ret = ''

        ret = ret + 'I: ' +  str(self.I) + '\n'
        ret = ret + 'Q: ' +  str(self.Q) + '\n'

        ret = ret + 'DEG: ' + str(self.DEG) + '\n'
        ret = ret + 'RAD: ' + str(self.RAD) + '\n'

        ret = ret + 'AMP: ' + str(self.AMP) + '\n'

        ret = ret + 'chan: ' + str(self.chan)

        return ret



