import visa

# x4 такт 1 - 5 ггц
# пч  - выход анализатор
# 12 v 0.5 A

class helpGenerator:
    ip =  None
    fullName = None
    name = None
    rm = visa.ResourceManager()
    hGenerator = None
    connected = False
    beg_freq_sweep = None
    end_freq_sweep = None
    sweep = None
    type = 'N5182A'

    def __init__(self):
        pass


    def __del__(self):
        pass

    def reset(self):
        pass

    def connect(self):
        try:
            if not self.ip:
                print('IP is None')
                self.fullName = 'Error'
                return
            self.hGenerator = self.rm.open_resource(self.ip, open_timeout=1000)
            print('Help Generator connected...')
            self.fullName = self.hGenerator.query('*IDN?')
        except:
            print('Error in Help Generator::connect()')
            self.hGenerator = None
            raise

    def getFrequency(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            readStr = int(self.hGenerator.query(':FREQ?'))
            return readStr
        except:
            print("Error in Help Generator::getFrequency()")
            raise

    def setFrequency(self, freq):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':FREQ %f MHz' % freq)
        except:
            print("Error in Help Generator::setFrequency()")
            raise

    def setFreqSweep(self, beg_freq_sweep, end_freq_sweep):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':SOUR:FREQ:START %f MHZ' % beg_freq_sweep)
            self.hGenerator.write(':SOUR:FREQ:START %f MHZ' % end_freq_sweep)

            self.beg_freq_sweep = str(beg_freq_sweep)
            self.end_freq_sweep = str(end_freq_sweep)
        except:
            print('Error in Help Generator::setFreqSweep()')
            raise

    def freqSweepMode(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return

            self.hGenerator.write(':SOUR:FREQ:MODE LIST')
            self.hGenerator.write(':INIT:CONT OFF')
            self.hGenerator.write('LIST:DIR UP')
            self.hGenerator.write('TRIG:FSW:SOUR SING')

        except:
            print('Error in Help Generator::freqSweepMode()')
            raise

    def setSweeepStep(self, sweep):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return

            self.hGenerator.write(':SOUR:SWE:FREQ:STEP:LIN %f MHz ' % sweep)

            self.sweep = str(sweep)
        except:
            print('Error in Help Generator::setSweepStep()')
            raise

    def setDwell(self, time):
        if self.hGenerator:
            try:
                self.hGenerator.write(':SOUR:SWE:FREQ:DWEL %d ms' %time)
            except:
                print("(G)Exception in setDwellTIme")
                raise

    def setLevel(self, level,unit=None):
        if self.hGenerator:
            try:
                if level >= -5:
                    return
                self.hGenerator.write(':POW %f dBm' % level)
                #self.waitEndCmd()
            except:
                print("(G)Exception in setPOW")
                raise

    def RFOutON(self):
        if self.hGenerator:
            try:
                self.hGenerator.write(':OUTP:STAT ON')
            except:
                print("(G)Exception in RFOutON")
                raise

    def RFOutOFF(self):
        if self.hGenerator :
            try:
                self.hGenerator.write(':OUTP:STAT OFF')
            except:
                print("(G)Exception in RFOutOFF")
                raise

    def reset(self):
        if self.hGenerator:
            try:
                self.hGenerator.write('*RST')
            except:
                try:
                    self.hGenerator.write('*RST')
                    #self.waitEndCmd()
                    self.hGenerator.write('*CLS')
                   # self.waitEndCmd()
                except:
                    print("(G)Exception in reset 2 state")
                    raise
                print("(G)Exception in reset")
                pass

    def nextStep(self):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
           # !!!
            # :LIST:TYPE:LIST:INITialize:FSTep
            self.hGenerator.write(':INIT:IMM')
        except:
            print('Error in Generator::reset()')
            raise


    def enableTwoTone(self, state):
        if self.hGenerator:
            try:
                if state:
                    self.hGenerator.write('SOUR:RAD:TTON:ARB ON')
                if not state:
                    self.hGenerator.write('SOUR:RAD:TTON:ARB OFF')
            except:
                print("(G)Exception in enableTwoTone")
                raise

    def setFreqTwoTone(self, val, units):
        try:
            if not self.hGenerator:
                print('hGenerator is None')
                return
            self.hGenerator.write(':RAD:TTON:ARB:ALIG CENT')
            self.hGenerator.write((':RAD:TTON:ARB:FSP %f' % val) + units)

        except:
            print('Error in helpGenerator::setFreqTwoTone()')
            raise

    def enableMod(self):
        if self.hGenerator:
            try:
                self.hGenerator.write(':OUTP:MOD ON')
            except:
                print("(G)Exception in enableModulation")
                raise
