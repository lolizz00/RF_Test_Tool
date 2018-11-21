import visa
import time
class Analyzer:
    def __init__(self):
        self.ip = None
        self.fullName = None
        self.name = None
        self.rm = visa.ResourceManager()
        self.hAnalyzer = None
        self.sweep = None
        self.freq_cent = None
        self.span = None
        self.ref_lvl = None

    def setBandwidth(self, bw, unit='khz'):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':BAND:RES ' + str(bw) + ' ' + unit)
                #self.waitEndCmd()
            except:
                print("Exception in setBandwidth")
                raise

    def getPhaseNoise(self):
        if self.hAnalyzer:
            try:
                readStr = self.hAnalyzer.query('CALC:DELT2:FUNC:PNO:RES?')
            except:
                print("Exception in getPhaseNoise")
                raise
            return float(readStr)

    def enablePhaseNoise(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:DELT2:FUNC:PNO ON')
                #self.waitEndCmd()
            except:
                print("Exception in enablePhaseNoise")
                raise


    def PhaseNoisePeakSearch(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:DELT2:FUNC:FIX:RPO:MAX')
            except:
                print("Exception in PhaseNoisePeakSearch")
                raise

    def setDeltaMarker2(self, delta, unit='kHz'):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:DELT2:X '+ str(delta) + ' ' + unit)
            except:
                print("Exception in setDeltaMarker2")
                raise

    def setCenterOnMarker(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:MARK:FUNC:CENT')
            except:
                print("Exception in setCenterOnMarker")
                raise

    def waitEndCmd(self):

        if self.hAnalyzer:
            try:

                self.hAnalyzer.write('*CLS')
                self.hAnalyzer.write('*OPC')

                ESRvalue = 0
                while (ESRvalue & 1) == 0:
                    ESRvalue = int(self.hAnalyzer.query('*ESR?'))
                    time.sleep(0.5)

            except:
                print("Exception in waitEndCmd")
                raise

    def averBeginMeas(self, count=20):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            #self.beginMeas()
            self.hAnalyzer.write('SWE:COUN ' +str(count))
            self.hAnalyzer.write('INIT;*WAI')
        except:
            print('Error in Analyzer:averBeginMeas()')
            raise


    def connect(self):
        try:
            if self.ip is None:
                print("IP is None")
                self.fullName = 'Error'
                return
            self.hAnalyzer = self.rm.open_resource(self.ip, open_timeout=1000)
            print('Analyzer connected...')
            self.fullName = self.hAnalyzer.query('*IDN?').replace('\n', '')
        except:
            self.hAnalyzer = None
            self.fullName = 'Error'
            print('Error in Analyzer::connect()')
            raise

    def setIP(self, ip):
            self.ip = ip

    def setName(self, name):
            self.name = name

    def markerOneOn(self):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write('CALC:MARK1:ON')
        except:
            print('Error in Analyzer::markerOneOn()')
            raise

    def setCenterOnMarker(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:MARK:FUNC:CENT')
            except:
                print("Exception in setCenterOnMarker")
                raise

    def setMarkerOne(self, x):  # OK
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write(':CALC:MARK1:X %f MHz' % float(x))
        except:
            print('Error in Analyzer::setMarkerOne()')
            raise


    def setMarkerTwo(self, x):  # OK
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write(':CALC:MARK2:X %d MHz' % x)
        except:
            print('Error in Analyzer::setMarkerOne()')
            raise

    def setDisplay(self, stat):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            if stat == True:
                self.hAnalyzer.write('SYST:DISP:UPD ON')
            if stat == False:
                self.hAnalyzer.write('SYST:DISP:UPD OFF')
        except:
            print('Error in Analyzer::setDisplay())')
            raise

    def getNoiseLevel(self):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            res = float(self.hAnalyzer.query('CALC:MARK:FUNC:NOIS:RES?'))
            return res
        except:
            print('Error in Analyzer::getNoiseLevel()')
            raise

    def setSweep(self, sweep, unit='ms'): # OK
            try:
                if not self.hAnalyzer:
                    print('hAnalyzer is None')
                    return
                self.hAnalyzer.write('SWE:TIME %f ' % sweep + unit)
                self.sweep = str(sweep) + ' ' + unit
            except:
                print('Error in Analyzer::setSweep()')
                raise

    def wait(self):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write('INIT;*WAI')
        except:
            print('Error in Analyzer::wait()')
            raise

    def setFreqCent(self, freq_cent, unit='MHz'): # OK
            try:
                if not self.hAnalyzer:
                    print('hAnalyzer is None')
                    return
                self.hAnalyzer.write(':FREQ:CENT %f ' % freq_cent + unit)
                self.freq_cent = str(freq_cent) + ' ' + unit
            except:
                print('Error in Analyzer::setFreqCent()')
                raise

    def reset(self):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write('*RST')
        except:
            print('Error in Analyzer::reset()')
            raise

    def setFreqSpan(self, span, unit='MHz'):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write(':FREQ:SPAN %f' % span + unit)
            self.span = str(span) + ' ' + unit
        except:
            print('Error in Analyzer::setFreqSpan()')
            raise

    def getMarkerOne(self):
        if self.hAnalyzer:
            try:
                readStr = self.hAnalyzer.query('CALC:MARK1:Y?')
            except:
                print("Exception in getMarkerOne")
                raise
            return float(readStr)

    def getMarkerOneFreq(self):
        if self.hAnalyzer:
                try:
                    readStr = self.hAnalyzer.query('CALC:MARK1:X?')
                except:
                    print("Exception in getMarkerOne")
                    raise
                return float(readStr)

    def setSweepCount(self, count):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write('SWE:COUN %d' % count)
        except:
            print('Error in Analyzer::setSweepCount()')
            raise

    def beginMeas(self):
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write(':INIT;*WAI')
        except:
            print('Error in Analyzer::beginMeas()')
            raise

    def waitEndCmd(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('*CLS')
                self.hAnalyzer.write('*OPC')

                ESRvalue = 0

                while (ESRvalue & 1) == 0:
                    time.sleep(0.2)
                    ESRvalue = int(self.hAnalyzer.query('*ESR?'))


            except:
                print("Exception in waitEndCmd")
                raise

    def traceClearWrite(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':DISP:TRAC:MODE WRIT')
            except:
                print("Exception in traceClearWrite")
                raise

    def singleSweepMode(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':INIT:CONT OFF')
               # self.waitEndCmd()
            except:
                print("Exception in singleSweepMode")
                raise

    def setRefLvl(self, val, unit='dBm'):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':DISP:TRAC:Y:RLEV %f ' % val + unit )
            except:
                print("Exception in setRefLvl")
                raise

    def enableDetectorRMS(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('DET RMS')
                self.waitEndCmd()
            except:
                print("Exception in enableDetectorRMS")
                raise

    def setPreamp(self, state):
        if self.hAnalyzer:
            try:
                if state:
                    self.hAnalyzer.write('INP:GAIN:STAT ON')
                else:
                    self.hAnalyzer.write('INP:GAIN:STAT OFF')
            except:
                print("Exception in enablePreamp")
                raise

    def enableNoiseMeasMarkX(self, x):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:MARK%d:FUNC:NOIS ON' %x)
            except:
                print("Exception in enableNoiseMeasMarkX")
                raise

    def disableNoiseMeasMarkX(self, x):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:MARK%d:FUNC:NOIS OFF' %x)
                #self.waitEndCmd()
            except:
                print("Exception in enableNoiseMeasMarkX")
                raise

    def getNoiseMarkX(self, x):
        if self.hAnalyzer:
            try:
                res = round(float(self.hAnalyzer.query('CALC:MARK%d:FUNC:NOIS:RES?' % x)), 2)
            except:
                print("Exception in getNoiseMarkX")
                raise
            return res

    def setMarker1PeakMIN(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':CALC:MARK1:MIN:PEAK')
                # self.waitEndCmd()
            except:
                print("Exception in setMarker1PeakMIN")
                raise

    def markerOneSetMax(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write(':CALC:MARK1:MAX')
                # self.waitEndCmd()
            except:
                print("Exception in searchNextPeakMarkerTwo")
                raise


    def enableTOI(self, state):
        if self.hAnalyzer:
            try:
                if state:
                    self.hAnalyzer.write('CALC:MARK:FUNC:TOI ON')
                if not state:
                    self.hAnalyzer.write('CALC:MARK:FUNC:TOI OFF')
            except:
                print("Exception in enableTOI")
                raise

    def getTOI(self):
        if self.hAnalyzer:
            try:
                readStr = self.hAnalyzer.query('CALC:MARK:FUNC:TOI:RES?')
            except:
                print("Exception in getTOI")
                raise
            return float(readStr)

    def setMarkerX(self, x, pos):  # OK
        try:
            if not self.hAnalyzer:
                print('hAnalyzer is None')
                return
            self.hAnalyzer.write(':CALC:MARK{}:X {} MHz'.format(x, pos))
        except:
            print('Error in Analyzer::setMarkerOne()')
            raise

    def getMarkerX(self, x):
        if self.hAnalyzer:
            try:
                readStr = self.hAnalyzer.query('CALC:MARK%d:Y?' % x)
            except:
                print("Exception in getMarkerOne")
                raise
            return float(readStr)

    # ----- Работа со скриншотами

    def copyScreenshot(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('MMEM:COPY \'C:\\scr.JPG,\'Y:\\\'')
            except:
                print("Exception in copyScreenshot")
                raise

    def delScreenshot(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('MMEM:DEL \'C:\\scr.JPG')
            except:
                print("Exception in delScreenshot")
                raise

    def getScreenshot(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('HCOP:NEXT')
            except:
                print("Exception in getScreenshot")
                raise

    # -----

    def setTracAver(self, state):
        if self.hAnalyzer:
            try:
                if state:
                    self.hAnalyzer.write(':AVER ON')
                else:
                    self.hAnalyzer.write(':AVER OFF')
            except:
                print("Exception in setTracAver")
                raise

    def setRef(self, state):
        if self.hAnalyzer:
            try:
                if state == 'INT':
                    self.hAnalyzer.write('ROSC:SOUR INT')
                elif state == 'EXT':
                    self.hAnalyzer.write('ROSC:SOUR EXT')
            except:
                print("Exception in setRef")
                raise

    def getNextMax(self):
        if self.hAnalyzer:
            try:
                self.hAnalyzer.write('CALC:MARK:MAX:NEXT')
            except:
                print("Exception in getAllMax")

    def getAllMax(self):
        if self.hAnalyzer:
            try:
                res = []
                last = None
                curr = None
                self.hAnalyzer.write('CALC:MARK1:MAX')

                while True:
                    last = curr
                    curr = self.getMarkerOne()

                    if curr == last:
                        break
                    else:
                        res.append(curr)
                        self.hAnalyzer.write('CALC:MARK:MAX:NEXT')

                return res

            except:
                print("Exception in getAllMax")
                return []
