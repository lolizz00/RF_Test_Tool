from dropbox.files import WriteMode
import dropbox
from dropbox import *
from PyQt5.QtCore import *
import time

class LOADER(QThread):
    def __init__(self):
        super(LOADER, self).__init__()

    def cnt(self):
        self.dbx = dropbox.Dropbox('Wtlm3Gln9dAAAAAAAAAADAf0oPC_RkRd-O9PTIxn89ddUwrT13YsMWlQjPsJDkqg')
        pass

    def load(self, name, path_in_pc, path_in_drp):
        tmp = str(name)
        with open(path_in_pc, 'rb') as f:
            self.dbx.files_upload(f.read(),   path_in_drp + tmp + '.png', mode=WriteMode('overwrite'))