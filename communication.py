#class which handles all the communication between computer and adapter
#****************************************
#******pySerial MUST be installed********
#******pip install pyserial**************
#****************************************

#TODO FIksaa serial.serialutil.SerialEXCPE ei toimi jos ei jotaki laitetta ehkä

import threading
import time
import sys
import serial
import os
import time
from saving import *
import configparser

sa = Saving()


class Communication (object):

    def __init__(self):

        self._config = configparser.ConfigParser()
        self._config.read("USECONTROL.ini")
        self.port = self._config["DEFAULT"]["port"]
        self.baudrate = int(self._config["DEFAULT"]["baud"])
        self.hands = self._config["DEFAULT"]["hands"]
        self.stopbits = int(self._config["DEFAULT"]["stopbits"])
        self.bytesize = int(self._config["DEFAULT"]["bytesize"])
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.hands, stopbits=self.stopbits, timeout=2)
        except (FileNotFoundError, serial.serialutil.SerialException):
            print("Serial Connection Problem")
            closeConnection()
            sys.exit(0)

    def closeConnection(self):
        self.keep_running = False
        self.ser.close()
        return self.ser.isOpen
        
        
    def setCommand(self, command):
        self.ser.flushInput()
        self.command = '#' + command + "\r"
        #self.ser.flushOutput()

        self.ser.write(self.command.encode('UTF-8'))
        time.sleep(.5)

        #com.readValues()
        #return 1

    def readValues(self):

        self.keep_running = True
        while self.keep_running:
            try:
                self.ser.flushOutput()
                self.value = self.ser.readline().decode()
                if self.value:
                    #print("READ: ", self.value)
                    sa.tallennaMIT(self.value)
                #time.sleep(0.5)

            except (KeyboardInterrupt, SystemExit):
                self.ser.close
                sys.exit(0)

    """def readValues(self, que):
        #while self.ser.isOpen():
        self.keep_running = True
        while self.keep_running:
            try:
                self.ser.flushOutput()
                #lck.acquire()
                self.value = self.ser.readline().decode()
                #lck.release()
                if self.value:
                    #print(self.value)
                    que.put(self.value)
                    que.task_done()
                #time.sleep(0.5)

            except (KeyboardInterrupt, SystemExit):
                self.ser.close
                sys.exit(0)


#tekee lukija threadin joka käynnistetään guissa, palauttaa aina viimeisimmän luetun rivin
    def readValues(self, que):
             try:
                self.ser.flushOutput()
                self.value = self.ser.readline().decode()
                if self.value:
                    print(self.value)
                    que.put(self.value)

             except (KeyboardInterrupt, SystemExit):
                self.ser.close
                sys.exit(0)

"""



#TESTING ZONE
#com = Communication("COM3", 9600)
#lck = threading.Lock()
#t1 = threading.Thread(target = com.readValues)
#t1 = threading.Thread(target = com.readValues, args=[lck])

#print("Aloitetaan kuuntelu\n")
#t1.start()

#com.setCommand('#RTC:?')
#time.sleep(0.5)
#com.setCommand('#ALKUK:1')
#time.sleep(0.5)
#com.setCommand('#STATE')
#time.sleep(0.5)
#com.setCommand('#HOME')
#time.sleep(0.5)
#com.closeConnection()


#print(com.readValues())

#ser.open()
#ser.is_open
#ser.close()

"""def readValues(self):
    try:

        #self.ser.flushInput()
        #self.ser.flushOutput()
        #self.waiting = self.ser.read(self.ser.in_waiting)
        #time.sleep(1)
        if self.ser.readline() is not None:
            self.value = self.ser.readline()
        else: exit(0)
        #self.value = self.ser.readline().decode()
        #self.outbuffer = self.ser.out_waiting

        print("value:", self.value.decode())
        print("buffer_out:", self.outbuffer)
        #return str(self.waiting) + str(self.value)
    except (KeyboardInterrupt, SystemExit):
        raise
        exit(0)
    
    def openConnection(self, port, baudrate):
        Avaa yhteyden sovittimen ja tietokoneen välille.
        Parametrina annetaan comtype (yhteystyyppi): BT tai RS-232
        toteutetaan ensin RS-232, mutta tehdään jo optio BT:lle. Palauttaa yhteyden tilan

        self.port = port
        self.baudrate = baudrate
        #ser = serial.Serial(port="COM3", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
        #serial.Serial.port()
        #ser.open()
        return self.ser.isOpen()"""


