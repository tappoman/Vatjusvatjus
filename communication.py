#class which handles all the communication between computer and adapter
#****************************************
#******pySerial MUST be installed********
#******pip install pyserial**************
#****************************************

import sys, time, serial

class Communication (object):

    def __init__(self, port="", baud_rate=""):
        self.port = port
        self.baud_rate = baud_rate

    def openConnection(self, port, baud_rate):
        """Avaa yhteyden sovittimen ja tietokoneen välille.
        Parametrina annetaan comtype (yhteystyyppi): BT tai RS-232
        toteutetaan ensin RS-232, mutta tehdään jo optio BT:lle. Palauttaa yhteyden tilan"""

        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baudrate, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
        ser.open()
        return ser.isOpen()

    
    def closeConnection(self):
        ser.close()
        return ser.isOpen
        
        
    def setCommand(self, command):
        ser.write('#', commmand, '\r\n')
        self.reply = ser.read()
        return self.reply
        
        
    def readValues(self):
        self.value = ser.read()
        return self.value
    
    
    #ser.open()
    #ser.isOpen()
    #ser.close()

