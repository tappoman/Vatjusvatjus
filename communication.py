#class which handles all the communication between computer and adapter
#****************************************
#******pySerial MUST be installed********
#******pip install pyserial**************
#****************************************

import sys, time, serial

class Communication (object):

    def __init__(self):
        """Avaa yhteyden sovittimen ja tietokoneen välille.
        Parametrina annetaan comtype (yhteystyyppi): BT tai RS-232         
        toteutetaan ensin RS-232, mutta tehdään jo optio BT:lle. Palauttaa yhteyden tilan"""
        
        self.ser = serial.Serial(port='COM1', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
        #ser.open()

        return ser.isOpen()
        
        
    def openConnection(self):
        ser.open()
        return ser.isOpen()
    
    
    def closeConnection(self):
        ser.close()
        return ser.isOpen
        
        
    def setCommand(self, command):
        ser.write('#' + commmand + '\r\n')
        self.reply = ser.read()
        return self.reply
        
        
    def readValues(self):
        value = ser.read()
		return value
    
    
    #ser.open()
    #ser.isOpen()
    #ser.close()

