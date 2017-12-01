import threading
import time
import sys
import serial
import os
import time

def Task1(ser, lck):
    while ser.is_open:
        try:
            print("Inside Thread 1")
            time.sleep(1)
            lck.acquire()
            #b = ser.read(7)
            b = ser.readline()
            lck.release()
            print ("b: ", b)
            print ("Thread 1 still going on")
            #time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

"""def Task2(ser, lck):

    try:
        print ("Inside Thread 2")
        print ("I stopped Task 1 to start and execute Thread 2")
        lck.acquire()
        ser.write(b'RTC:?')
        b = ser.read(7)
        lck.release()
        print(b)
        print ("Thread 2 complete")

    except (KeyboardInterrupt, SystemExit):
        raise"""


try:

    #ser = serial.Serial(port="COM3", baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS, timeout=2)
    ser = serial.Serial(port="COM3", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)

    lck = threading.Lock()
    t1 = threading.Thread(target = Task1, args=[ser,lck])
    #t2 = threading.Thread(target = Task2, args=[ser,lck])
    print ("Starting Thread 1")
    t1.start()
    #print ("Starting Thread 2")
    #t2.start()
    #ser.write(b'RTC:?')
    #time.sleep(1)
    ser.write("#ALKUK:1\n".encode("UTF-8"))

    ser.close()
    exit()

except (serial.SerialException, KeyboardInterrupt, TypeError) as e:
    print("ei toimi", e)
    quit(0)


    """print('Enter your commands below.\r\nInsert "exit" to leave the application.')
    ser = serial.Serial(port="COM3", baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.SEVENBITS, timeout=2)
    #input = 1
    while 1:
        # Python 3 users
        inni = input(">> ")
        if inni == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            print(inni)
            inni = str.encode(inni)
            print(inni)
            ser.write(inni)
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)

            if out != '':
                print (">>" + out)"""