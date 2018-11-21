import visa
import math

class PB:
    fullName = None
    ip = None
    hPB = None
    rm = visa.ResourceManager()
    type = None

    def __init__(self):
        self.pb2_pow = 10 * math.log(0.9 * 5 * 1000, 10)

    def connect(self):
        try:
            if not self.ip:
                print('IP is None')
                self.fullName = 'Error'
                return
            self.hPB = self.rm.open_resource(self.ip, open_timeout=1000)
            print('PB connected...')
            self.fullName = self.hPB.query('*IDN?')
            if self.fullName.find('6702') != -1:
                self.type = '6702'
            elif self.fullName.find('5767') != -1:
                self.type = '5767'
        except:
            print('Error in PB_5::connect()')
            self.hPB = None
            raise

    def setOut(self, state, chanel=0):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            if self.type == '6702':
                if state:
                    self.hPB.write('OUTP ON,(@%d)' % chanel)
                else:
                    self.hPB.write('OUTP OFF,(@%d)' % chanel)
            if self.type == '5767':
                if state:
                    self.hPB.write('OUTP:STAT ON')
                else:
                    self.hPB.write('OUTP:STAT OFF')
        except:
            print('Error in PB_5::setOut()')
            raise

    def getVolt(self,chanel=0):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            if self.type == '5767':
                readStr = self.hPB.query('MEAS:VOLT?')
                return float(readStr)
            elif self.type == '6702':
                readStr = float(self.hPB.query('VOLT? (@%d)' % chanel))
                return readStr
        except:
            print('Error in PB_5::getVolt()')
            raise

    def setVolt(self, val, chanel=0):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            val = float(val)
            if self.type == '6702':
                self.hPB.write('VOLT %f,(@%d)' % (val, chanel))
            elif self.type == '5767':
              pass
        except:
            print('Error in PB_5::setVolt()')
            raise

    def setAmp(self, val, chanel=0):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            val = float(val)
            if self.type == '6702':
                self.hPB.write('CURR %f,(@%d)' % (val, chanel))
            elif self.type == '5767':
                pass
        except:
            print('Error in PB_5::setAmp()')
            raise

    def getAmp(self,chanel=0):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            if self.type == '5767':
                readStr = self.hPB.query('MEAS:CURR?')
                return float(readStr)
            elif self.type == '6702':
                readStr = self.hPB.query('CURR? (@%d)' % chanel)
                return float(readStr)
        except:
            print('Error in PB_5::getAmp()')
            raise

    def setPowLimit(self, val):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            self.hPB.write('POW:LIM %f' % val)
        except:
            print('Error in PB_5::setPowLimit()')
            raise

    def getPowLimit(self):
        if not self.hPB:
            print('hPB is None')
            return
        try:
            readStr = self.hPB.query('POW:LIM?')
            return int(readStr)
        except:
            print('Error in PB_5::getPowLimit()')
            raise

    def getCurrPow(self):
        if not self.hPB:
            print('hPB is None')
            return
        try:
          #  return 10
            i = self.getVolt()
            v = self.getAmp()
            res = i * v + 0.91 * 5.0
            return res
        except:
            print('Error in PB_5::getPowLimit()')
            raise
