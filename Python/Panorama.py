import serial
import io
import re
import time

class Panorama:

    type = 'Panorama'
    port = None
    status = 'Disconn'

    att_max = 31
    att_min = 0


    #  'Disconn', 'Conn', 'Err'

    def __init__(self):
        self.port = serial.Serial()


        # ----- Настройки порта
        self.port.baudrate = 115200
        self.port.bytesize = 8
        self.port.parity = 'N'
        self.port.stopbits = 1
        self.port.timeout = 0.1


    def resetDef(self):
        self.setMode('standby')
        time.sleep(1)
        self.setMode('work')
        time.sleep(1)

        #self.setAtt(0)
        #time.sleep(0.1)
        #self.setLNA(False)
        #time.sleep(0.1)
        #self.setRef('INT')
        #time.sleep(0.1)




    def ask(self, indata):
        self.send(indata)
        return self.read()

    def testConnection(self):
        data = self.ask('ver')
        try:
            if data != [] and data[0].find('PAN_SYN') != -1:
                return True
            else:
                return False
        except:
            return False

    def send(self, comm):
        comm = comm + '\n\r'
        self.port.write(comm.encode('utf-8'))

    def read(self):
        data = []
        ret_data = []
        try:
            data = self.port.readlines()

            for lines in data:
                lines = lines.decode('utf-8')
                lines = lines.replace('\n', '')
                lines = lines.replace('\r', '')

                if lines != '' and lines != 'SHELL>' and (lines.find('No argument(s)') == -1):
                    ret_data.append(lines)

            ret_data.pop(0)

            return ret_data
        except:
            return data

    def search(self):
        try:
            self.port.close()
        except:
            pass

        ports = self.listPorts()

        for i in ports:
            try:
                self.port.port = i
                self.port.open()
                if self.testConnection():
                    self.port.close()
                    return i
                else:
                    self.port.close()
            except:
                pass

        return None

    def listPorts(self):
        ports = []
        for i in range(1, 20):
            try:
                self.port.port = 'COM' + str(i)
                self.port.open()
                self.port.close()
                ports.append('COM' + str(i))
            except:
                continue
        return ports

    def connect(self, _port):
        try:
            self.port.port = _port
            self.port.open()
            self.status = 'Conn'
        except:
            self.status = 'Err'
            raise  # отправляем наверх

    def disconnect(self):
        try:
           self.port.close()
           self.status = 'Conn'
        except:
            self.status = 'Err'
            raise  # отправляем наверх

    def setAtt(self, val):
        if val < 0:
            val = 0
        if val > 31.75:
            val = 31.75
        try:
            data = self.ask('att ' + str(val))
            time.sleep(0.1)
            if not data or (data[0].find('Invalid') != -1):
                return None
            else:
                return 'OK'
        except:
            return None

    def getAtt(self):
        try:
            data = self.ask('att')
            if not data or (data[0].find('Invalid') != -1):
                return None
            else:
                res = re.search(r'\d{1,2}\.\d{1,2}', data[0])
                res = float(res.group(0))
                return res
        except:
            return None

    # -----

    def setDAC(self, val):
        if val < 0:
            val = 0
        if val > 1024:
            val = 1024
        try:
            data = self.ask('dac ' + str(val))
            if not data or (data[0].find('Invalid') != -1):
                return None
            else:
                return 'OK'
        except:
            return None

    def getDAC(self):
        try:
            data = self.ask('dac')
            if not data or (data[0].find('Invalid') != -1):
                return None
            else:
                res = re.search(r'\d+', data[0])
                res = int(res.group(0))
                return res
        except:
            return None

    # ---

    def setInj(self, val):
        try:
            if val:
                data = self.ask('injector on')
            else:
                data = self.ask('injector off')
            if not data:
                return None
            else:
                return 'OK'
        except:
            return None

    def getInj(self):
        try:
            data = self.ask('injector')
            if not data:
                return None
            else:
                if data[0].find('on') != -1:
                    return True
                if data[0].find('off') != -1:
                    return False
                return None
        except:
            return None

    # -----

    def setLNA(self, val):
        try:
            if val:
                data = self.ask('lna int')
            else:
                data = self.ask('lna ext')
            if not data:
                return None
            else:
                return 'OK'
        except:
            return None

    def getLNA(self):
        try:
            data = self.ask('lna')
            if not data:
                return None
            else:
                if data[0].find('on') != -1:
                    return True
                if data[0].find('off') != -1:
                    return False
                else:
                    return None
        except:
            return None


    # -----

    def setMode(self, val):
        try:
            if val == 'work':
                data = self.ask('mode work')
            elif val == 'standby':
                data = self.ask('mode standby')
            else:
                return None
            if not data:
                return None
            else:
                return 'OK'
        except:
            return None

    def getMode(self):
        try:
            data = self.ask('mode')
            if not data:
                return None
            else:
                if data[0].find('standby') != -1:
                    return 'standby'
                if data[0].find('operation') != -1:
                    return 'work'
                else:
                    return None
        except:
            return None

    # ----

    def setRef(self, val):
        try:
            if val == 'EXT':
                data = self.ask('ref ext')
            elif val == 'INT':
                data = self.ask('ref int')
            else:
                return None
            if not data:
                return None
            else:
                return 'OK'
        except:
            return None

    def getRef(self):
        try:
            data = self.ask('ref')
            if not data:
                return None
            else:
                if data[0].find('External') != -1:
                    return 'EXT'
                if data[0].find('Internal') != -1:
                    return 'INT'
                else:
                    return None
        except:
            return None

    #-----

    def setTcxo(self, val):
        try:
            if val == 'on':
                data = self.ask('tcxo on')
            elif val == 'off':
                data = self.ask('tcxo off')
            else:
                return None
            if not data:
                return None
            else:
                return 'OK'
        except:
            return None

    def getTcxo(self):
        try:
            data = self.ask('tcxo')
            if not data:
                return None
            else:
                if data[0].find('on') != -1:
                    return 'ON'
                if data[0].find('off') != -1:
                    return 'OFF'
                else:
                    return None
        except:
            return None

    def setFreq(self, val):
        try:
            if val < 500:
                val = 500
            if val > 2500:
                val = 2500
            val = (val + 3600)
            val = str(int(val))
            data = self.ask('lmx2592 frequency adjust ' + val + '000000')
            if data[0].find('set'):
                return 'OK'
            else:
                return None
        except:
            return None

    def getFreq(self):
        try:
            data = self.ask('lmx2592 frequency')
            data = re.search(r'\d+\.\d+', data[0])
            data = float(data.group(0))
            data = float(data) / 1000000
            data = data - 3600
            return int(data)
        except:
            return None

    def getLmxFreq(self):
        data = self.ask('lmx2592 frequency')
        data = re.search(r'\d+\.\d+', data[0])
        data = float(data.group(0))
        data = float(data) / 1000000
        return data

    def setFreqReboot(self, val):
        ret = self.setFreq(val)
        time.sleep(0.3)
        return ret
