# gqrx-hamlib - a gqrx to Hamlib interface to keep frequency
# between gqrx and a radio in sync when using gqrx as a panadaptor
# using Hamlib to control the radio
#
# The Hamlib daemon (rigctld) must be running, gqrx started with
# the 'Remote Control via TCP' button clicked and
# comms to the radio working otherwise an error will occur when
# starting this program. Ports used are the defaults for gqrx and Hamlib.
#
# Return codes from gqrx and Hamlib are printed to stderr
#
# This program is written in Python 3.5
# Python libraries required are:
#   - socket
#   - sys
#   - getopt
#   - time
#   - xmlrpc.client
#
# To run it type the following on the command line in the directory where
# you have placed this file:
#   python3.5 ./gqrx-hamlib-fldigi.py [-f]
#
# The -f option will cause the program to tune fldigi to the gqrx frequency.
#
# Copyright 2017 Simon Kennedy, G0FCU, g0fcu at g0fcu.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
import time
from PyQt4 import QtCore
from PyQt4.QtCore import QThread
from PyQt4 import QtGui
import design
import sys 

class startControl(QThread):
    reportErr = QtCore.pyqtSignal(str, str)
    
    def __init__(self, control, oneoff):
        QThread.__init__(self)
        self.control = control
        self.oneoff = oneoff
                  
    def __del__(self):
        self.wait()
      
    def run(self):    
        TCP_IP = 'localhost'
        RIG_PORT = 4532
        GQRX_PORT = 7356
        FLDIGI_PORT = 7362
        
        MESSAGE = ""
        
        rig_freq = 0
        gqrx_freq = 0
        old_rig_freq = 0
        old_gqrx_freq = 0
        rig_mode = ''
        gqrx_mode = ''
        set_mode = ''
        old_rig_mode = ''
        old_gqrx_mode = ''
       
        while self.control > 0:       
            time.sleep(0.2)
            if self.control == 1 or self.control == 3:
                rig_freq = self.getfreq(TCP_IP, RIG_PORT)
                if rig_freq[:4] == 'RPRT':
                    if rig_freq[:6] != 'RPRT 0':
                        self.reportErr.emit('hamlib',str(rig_freq))
                        return
                if rig_freq != old_rig_freq:
                    # set gqrx to Hamlib frequency
                    rc = self.setfreq(TCP_IP, GQRX_PORT, float(rig_freq))
                    if rc[:4] == 'RPRT':
                        if rc[:6] != 'RPRT 0':
                            self.reportErr.emit('gqrx', str(rc))
                            return
                    #print('SetFreq Return Code from GQRX: {0}'.format(rc))
                    old_rig_freq = rig_freq
                    old_gqrx_freq = rig_freq
                    
                rig_mode = self.getmode(TCP_IP, RIG_PORT)[:3]
                if rig_mode[:4] == 'RPRT':
                    if rig_mode[:6] != 'RPRT 0':
                        self.reportErr.emit('hamlib',str(rig_mode))
                        return
                if rig_mode != old_rig_mode:
                    if rig_mode == 'CW':
                        set_mode = 'CW-U'
                    else:
                        set_mode = rig_mode
                    # set gqrx to Hamlib frequency
                    rc = self.setmode(TCP_IP, GQRX_PORT, set_mode)
                    if rc[:4] == 'RPRT':
                        if rc[:6] != 'RPRT 0':
                            self.reportErr.emit('gqrx', str(rc))
                            return
                    #print('SetMode Return Code from GQRX: {0}'.format(rc))
                    old_rig_mode = rig_mode
                    old_gqrx_mode = rig_mode
                    
            if self.control == 1 or self.control == 2:
                gqrx_freq = self.getfreq(TCP_IP, GQRX_PORT)
                if gqrx_freq[:4] == 'RPRT':
                    if gqrx_freq[:6] != 'RPRT 0':
                        self.reportErr.emit('gqrx',str(gqrx_freq))
                        return
                if gqrx_freq != old_gqrx_freq:
                    # set Hamlib to gqrx frequency
                    rc = self.setfreq(TCP_IP, RIG_PORT, float(gqrx_freq))
                    if rc[:4] == 'RPRT':
                        if rc[:6] != 'RPRT 0':
                            self.reportErr.emit('hamlib', str(rc))
                            return
                    #print('SetFreq Return Code from Hamlib: {0}'.format(rc))
                    # Set fldigi to gqrx frequency
                    #if fldigi_option_set == 1:
                    #    server.main.set_frequency(float(gqrx_freq))
                    old_gqrx_freq = gqrx_freq
                    old_rig_freq = gqrx_freq
                        
                gqrx_mode = self.getmode(TCP_IP, GQRX_PORT)[:3]
                if gqrx_mode[:4] == 'RPRT':
                    if gqrx_mode[:6] != 'RPRT 0':
                        self.reportErr.emit('gqrx',str(gqrx_mode))
                        return
                if gqrx_mode != old_gqrx_mode:
                    # set Hamlib to gqrx frequency
                    rc = self.setmode(TCP_IP, RIG_PORT, gqrx_mode)
                    if rc[:4] == 'RPRT':
                        if rc[:6] != 'RPRT 0':
                            self.reportErr.emit('hamlib', str(rc))
                            return
                    #print('SetMode Return Code from Hamlib: {0}'.format(rc))
                    old_gqrx_mode = gqrx_mode
                    old_rig_mode = gqrx_mode  
            
            if self.oneoff == True:
                return
            
    def getfreq(self, TCP_IP, PORT):
        sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_STREAM) 
        # Bind the socket to the port
        server_address = (TCP_IP, PORT)
        sock.connect(server_address)
        sock.sendall(b'f\n')
        # Look for the response
        amount_received = 0
        amount_expected = 8 #len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
        sock.close()
        return data
    
    def setfreq(self, TCP_IP, PORT, freq):
        sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_STREAM) 
        # Bind the socket to the port
        server_address = (TCP_IP, PORT)
        sock.connect(server_address)
        build_msg = 'F ' + str(freq) + '\n'
        MESSAGE = bytes(build_msg)
        sock.sendall(MESSAGE)
        # Look for the response
        amount_received = 0
        amount_expected = 7 #len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
        sock.close()
        return data
    
    def getmode(self, TCP_IP, PORT):
        sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_STREAM) 
        # Bind the socket to the port
        server_address = (TCP_IP, PORT)
        sock.connect(server_address)
        sock.sendall(b'm\n')
        # Look for the response
        amount_received = 0
        amount_expected = 4 #len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
        sock.close()
        return data
    
    def setmode(self, TCP_IP, PORT, mode):
        sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_STREAM) 
        # Bind the socket to the port
        server_address = (TCP_IP, PORT)
        sock.connect(server_address)
        build_msg = 'M ' + str(mode) + ' 0' + '\n'
        MESSAGE = bytes(build_msg)
        sock.sendall(MESSAGE)
        # Look for the response
        amount_received = 0
        amount_expected = 7 #len(message)
        data = ''
        while amount_received < amount_expected:
            data = sock.recv(7)
            amount_received += len(data)
        sock.close()
        return data
       
class gqrxHamlib(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        control = 0
        oneoff = False
        global rc 
        rc = ''
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        # At this point we want to allow user to stop/terminate the thread
        # so we enable that button
        self.btn_stop.setEnabled(True)
        self.controlThread.setTerminationEnabled(True)
        # And we connect the click of that button to the built in
        # terminate method that all QThread instances have
        self.btn_stop.clicked.connect(self.stopThread)
        control = self.pushButton.clicked.connect(self.gqrxhamlibSync)
        control = self.pushButton_2.clicked.connect(self.gqrxControl)
        control = self.pushButton_3.clicked.connect(self.hamlibControl)
        control = self.pushButton_6.clicked.connect(self.gqrxControlOneoff)
        control = self.pushButton_4.clicked.connect(self.hamlibControlOneoff) 
    
    def reportErrMsg(self, source, rc):
        self.errorMsg.setText('Error, return code ' + rc + ' reported by ' + source)
                    
    def stopThread(self):
        self.btn_stop.setStyleSheet("background-color: red")
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton_2.setStyleSheet("background-color: green")
        self.pushButton_3.setStyleSheet("background-color: green")
        self.pushButton_4.setStyleSheet("background-color: green")
        self.pushButton_6.setStyleSheet("background-color: green")
        self.controlThread.terminate()
        
    def gqrxhamlibSync(self):
        self.btn_stop.setStyleSheet("background-color: green")
        self.pushButton.setStyleSheet("background-color: red")
        self.pushButton_2.setStyleSheet("background-color: green")
        self.pushButton_3.setStyleSheet("background-color: green")
        self.pushButton_4.setStyleSheet("background-color: green")
        self.pushButton_6.setStyleSheet("background-color: green")
        control = 1
        oneoff = False
        self.controlThread.terminate()
        self.errorMsg.setText('')
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        self.controlThread.start()
        
    def gqrxControl(self):
        self.btn_stop.setStyleSheet("background-color: green")
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton_2.setStyleSheet("background-color: red")
        self.pushButton_3.setStyleSheet("background-color: green")
        self.pushButton_4.setStyleSheet("background-color: green")
        self.pushButton_6.setStyleSheet("background-color: green")
        control = 2
        oneoff = False
        self.controlThread.terminate()
        self.errorMsg.setText('')
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        self.controlThread.start()
    
    def hamlibControl(self):
        self.btn_stop.setStyleSheet("background-color: green")
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton_2.setStyleSheet("background-color: green")
        self.pushButton_3.setStyleSheet("background-color: red")
        self.pushButton_4.setStyleSheet("background-color: green")
        self.pushButton_6.setStyleSheet("background-color: green")
        control = 3
        oneoff = False
        self.controlThread.terminate()
        self.errorMsg.setText('')
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        self.controlThread.start()
              
    def gqrxControlOneoff(self):
        self.btn_stop.setStyleSheet("background-color: green")
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton_2.setStyleSheet("background-color: green")
        self.pushButton_3.setStyleSheet("background-color: green")
        self.pushButton_4.setStyleSheet("background-color: green")
        self.pushButton_6.setStyleSheet("background-color: red")
        control = 2
        oneoff = True
        self.controlThread.terminate()
        self.errorMsg.setText('')
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        self.controlThread.start()
        self.pushButton_6.setStyleSheet("background-color: green")
        
    def hamlibControlOneoff(self):
        self.btn_stop.setStyleSheet("background-color: green")
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton_2.setStyleSheet("background-color: green")
        self.pushButton_3.setStyleSheet("background-color: green")
        self.pushButton_4.setStyleSheet("background-color: red")
        self.pushButton_6.setStyleSheet("background-color: green")
        control = 3
        oneoff = True
        self.controlThread.terminate()
        self.errorMsg.setText('')
        self.controlThread = startControl(control, oneoff)
        self.controlThread.reportErr.connect(self.reportErrMsg)
        self.controlThread.start()
        self.pushButton_4.setStyleSheet("background-color: green")
        
  
    #if fldigi_option_set == 1:
        #server = xmlrpc.client.ServerProxy('http://{}:{}/'.format(TCP_IP, FLDIGI_PORT))
        #fldigi_option_set = 0
        
              #if len(sys.argv) > 0:
        #    try:
        #        opts, args = getopt.getopt(sys.argv, 'f',)
        #    except getopt.GetoptError:
        #        print('gqrx-hamlib.py [-f]')
        #       sys.exit(2)
        #    for index in range(len(args)):
        #        if args[index] == '-f':
        #           fldigi_option_set = 1
        
        #if fldigi_option_set == 1:
        #   import xmlrpc.client

def main():
    app = QtGui.QApplication(sys.argv)
    form = gqrxHamlib()
    form.show()
    app.exec_()
            
if __name__ == '__main__':
    main()

