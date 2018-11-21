from A_Test import A_Test
import time

class UD_Test(A_Test):
    def __init__(self):
        super(UD_Test, self).__init__()


    def run(self):

        try:

            # ----- Установка параметров

            self.count = int(self.user[0])
            self.span = self.user[1]
            self.time = self.user[2]
            self.pan = False

            if self.dev.type == 'Panaroma':
                self.pan = True


            # ------ Инициализация устройства

            if self.pan:
               # self.dev.resetDef()
                pass

            # ------ Инициализация анализатора

            self.an.reset()
            self.an.setFreqSpan(self.span, 'kHz')
            self.an.setTracAver(True)
            self.an.setSweep(50, 'ms')
            self.an.setRefLvl(self.level + 30, 'dBm')

            if self.pan:
                self.an.setFreqCent(750, 'MHz')


            # ------ Инициализация генератора

            self.gen.reset()
            self.gen.setLevel(self.level)
            self.gen.setFreq(self.beg)
            #self.gen.RFOutON()
            time.sleep(1)

            # ------ Непосредственно тест


            for i in range(int(self.count)):  # количество повторов

                if self.stop_flg:
                    raise Warning

                self.progress_signal.emit(i)

                self.gen.RFOutOFF()
                time.sleep(0.1)
                self.dev.resetDef()
                self.gen.RFOutON()

                # ----

                bg  = self.beg
                ed = self.end

                while bg <= ed:
                    self.gen.setFreq(bg)

                    if self.pan:
                        self.dev.setFreqReboot(bg)

                    time.sleep(self.time)

                    self.savescreen_an_signal.emit('CNT_' + str(i) + '_UP_' + str(int(bg)) + '_MHz.png',
                                                   self.logfile)

                    time.sleep(3)
                    bg = bg + 1
                # ----

                bg = self.end
                ed = self.beg

                while bg >= ed:
                    self.gen.setFreq(bg)

                    if self.pan:
                        self.dev.setFreqReboot(bg)

                    time.sleep(self.time)

                    self.savescreen_an_signal.emit('CNT_' +  str(i) + '_DOWN_' + str(int(bg)) + '_MHz.png',
                                                   self.logfile)

                    time.sleep(3)
                    bg = bg - 1





        except:
            if self.stop_flg:
                print('UD stopped')
            else:
                print('Error in UD()')
        finally:

            self.gen.RFOutOFF()

            self.end_signal.emit(False)
            self.progress_signal.emit(self.count)
            self.log_signal.emit('READY!')

