import visa
import time

class Generator:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.ip = None
        self.name = None
        self.fullName = None
        self.hGenerator = None
        self.freq = None
        self.level = None
        self.beg_freq_sweep = None
        self.end_freq_sweep = None
        self.dwell = None
        self.sweep = None
        self.type = 'SMA100A'

    def setSweeepStep(self, sweep, unit):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':SOUR:SWE:FREQ:STEP:LIN %f ' % sweep + unit)
            self.sweep = str(sweep) + ' ' + unit
        except:
            print('Error in Generator::setSweepStep()')
            raise

    def setDwell(self, dwell, unit):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':SOUR:SWE:FREQ:DWEL %f ' % dwell + unit)
            self.dwell = str(dwell) + ' ' + unit
        except:
            print('Error in Generator::setDwell()')
            raise

    def setFreqSweep(self, beg_freq_sweep, end_freq_sweep, unit):  # OK
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':SOUR:FREQ:START %f ' % beg_freq_sweep + unit)
            self.hGenerator.write(':SOUR:FREQ:STOP %f ' % end_freq_sweep, unit)

            self.beg_freq_sweep = str(beg_freq_sweep) + ' ' + unit
            self.end_freq_sweep = str(end_freq_sweep) + ' ' + unit
        except:
            print('Error in Generator::setFreqSweep()')
            raise

    def freqSweepMode(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return

            #self.setFrequency(10)

            self.hGenerator.write('TRIG:FSW:SOUR SING')
            self.hGenerator.write('SOUR:FREQ:MODE SWE')
            self.hGenerator.write('SOUR:SWE:FREQ:MODE STEP')

        except:
            print('Error in Generator::freqSweepMode()')
            raise

    def setLevel(self, level, unit='dBm'):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            if level >= -15:
                return 'MAX'

            self.hGenerator.write(':POW %f ' % level + unit)
            self.level = str(level) + ' ' + unit
            return None
        except:
            print('Error in Generator::setLevel()')
            raise

    def setFreq(self, freq):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':FREQ %f MHz' % freq)
        except:
            print('Error in Generator::setFrequency()')
            raise

    def RFOutOFF(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':OUTP:STAT OFF')
        except:
            print('Error in Generator::RFOutON()')
            raise

    def RFOutON(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':OUTP:STAT ON')
        except:
            print('Error in Generator::RFOutOFF()')
            raise

    def connect(self):
        try:
            if not self.ip:
                print('IP is None')
                self.fullName = 'Error'
                return
            self.hGenerator = self.rm.open_resource(self.ip, open_timeout=1000)
            print('Generator connected...')
            self.fullName = self.hGenerator.query('*IDN?').replace('\n', '')
        except:
            print('Error in Generator::connect()')
            self.fullName = 'Error'
            self.hGenerator = None
            raise


    def getFreq(self):
        try:
            if self.hGenerator :
                readStr = self.hGenerator.query(':FREQ?')
                return readStr
            else:
                print('hGenerator is None')
        except:
            print('Error in Generator::getFreq()')

    def reset(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write('*RST')
            self.hGenerator.write('*CLS')
        except:
            print('Error in Generator::reset()')
            raise

    def nextStep(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write('SOUR:FREQ:MAN UP')
        except:
            print('Error in Generator::reset()')
            raise

    def waitSweepOperation(self):
        try:
            if not self.hGenerator :
                print('hGenerator is None')
                return
            while int(self.hGenerator.query('STAT:OPER:COND?')) != 0:
                time.sleep(1 / 100)
        except:
            print('Error in Generator::waitSweepOperation()')
            raise

    def setRefOut(self, state):
        if self.hGenerator:
            try:
                if state:
                    self.hGenerator.write('CSYN:STAT ON')
                else:
                    self.hGenerator.write('CSYN:STAT OFF')
            except:
                print('Exception in Generator::setRefOut()')