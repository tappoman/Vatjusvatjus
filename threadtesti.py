from communication import *
from guioperations import *
import threading
import time
import sys
import serial
import os
import time

gui = Guioperations()

gui.pysaytaKairaus()
gui.aloitaAlkutila()
gui.tiedusteleAika()
gui.aloitaAlkukairaus()
gui.lopetaAlkukairaus()
gui.aloitaMittaustila()
time.sleep(5)
gui.pysaytaKairaus()
gui.aloitaAlkutila()
#gui.tulostaStream()
gui.closeConnection()
