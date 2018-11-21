from ctypes import *


class DEV_HMC:

    type = 'HMC'
    n_chanel = 1
    status = 'Disconn'
    #  'Disconn', 'Conn', 'Err'

    def __init__(self):
        try:
            self.dll = cdll.LoadLibrary('HMC_DLL.dll')
            self.dll.getATT.restype = c_float
            self.dll.getTemp.restype = c_float
            # self.dll.getPowStatus.restype = ...   # TODO HMC DLL
        except:
            print('Error in HMC::__init()__')
            self.status = 'Err'

    def connect(self):
        try:
            self.dll.setChanel(self.n_chanel)
            self.dll.initFTDI()
            self.status = 'Conn'
        except:
            print('Error in HMC::connect()')
            self.status = 'Err'

    def __del__(self):
      self.disconnect()

    def disconnect(self):
        try:
            if self.status == 'Conn':
                self.dll.deinitFTDI()
                self.status = 'Disconn'
        except:
            print('Error in HMC::disconnect()')
            self.status = 'Err'

    def getATT(self):
        res = None
        try:
            res = self.dll.getATT()
        except:
            print('Error in HMC::getATT()')
            self.status = 'Err'
            raise
        finally:
            return res

    def setATT(self, val):
        try:
          self.dll.setATT()
        except:
            print('Error in HMC::setATT()')
            self.status = 'Err'
            raise

    def setChanel(self, chanel):
        self.n_chanel = chanel

    def getTemp(self):
        res = None
        try:
            res = None  # TODO HMC DLL
        except:
            print('Error in HMC::getTemp()')
            self.status = 'Err'
        finally:
            return res

    def getPowStatus(self):
        res = None
        try:
            res = None  # TODO HMC DLL
        except:
            print('Error in HMC::getPowStatus()')
            self.status = 'Err'
        finally:
            return res


