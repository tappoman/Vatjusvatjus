#class which handles all the communication between computer and adapter
#****************************************
#******pySerial MUST be installed********
#******pip install pyserial**************
#****************************************

import threading
import time
import sys
import serial
import os
import time
from saving import *
import configparser

class Communication (object):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read("USECONTROL.ini")
        self.port = self._config["DEFAULT"]["port"]
        self.baudrate = int(self._config["DEFAULT"]["baud"])
        self.hands = self._config["DEFAULT"]["hands"]
        self.stopbits = int(self._config["DEFAULT"]["stopbits"])
        self.bytesize = int(self._config["DEFAULT"]["bytesize"])
        self.sa = Saving()

    def openConnection(self):
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.hands, stopbits=self.stopbits, timeout=2)
            return True
        except (FileNotFoundError, serial.serialutil.SerialException):
            print("Serial Connection Problem")
            return False
            sys.exit(0)


    def closeConnection(self):
        #print("COMCLOSE")
        self.keep_running = False

        #self.ser.flushOutput()
        #self.ser.flushInput()
        self.ser.close()
        #return self.ser.isOpen
        
        
    def setCommand(self, command):
        self.ser.flushInput()
        self.command = '#' + command + "\r"
        print("<--\t", self.command)
        #self.ser.flushOutput()

        try:
            self.ser.write(self.command.encode('UTF-8'))
            time.sleep(.5)

        except (KeyboardInterrupt, SystemExit, serial.serialutil.SerialException):

            self.ser.close
            sys.exit(0)

    def readValues(self):

        self.keep_running = True
        while self.keep_running:
            try:
                self.ser.flushOutput()
                self.value = self.ser.readline().decode()
                if self.value:
                    #print("READ: ", self.value)
                    self.sa.tallennaMIT(self.value)
                #time.sleep(0.5)

            except (KeyboardInterrupt, SystemExit, serial.serialutil.SerialException):
                self.ser.close
                sys.exit(0)




