#Class which pass all the commands from gui to communication class

#TODO: hoida vastausten parsinnat täällä jos tarvitsee:
#KUUNNELLESSA HEADERIIN TULEE VASTAUS JOITA PARSITAAN 
#(NÄMÄ ON TOISINSANOEN KOMENTOJA JOITA ANNETAAN KKS:LTÄ JA NIIHIN PITÄÄ REAGOIDA):
#NOSTO, #KAIRAUS, MITÄ?


from communication import *
import threading
import time
import sys
import serial
import os
import time
import queue

"""luodaan communication olio com ja avataan yhteys sovittimelle"""
com = Communication("COM3", 9600)

class Guioperations (object):

    def __init__(self):

        """Thread for KKS-reader
        # lck = threading.Lock()
        #que = queue.Queue()
        t1 = threading.Thread(target=com.readValues)
        #t1 = threading.Thread(target=com.readValues)
        #t1 = threading.Thread(target=lambda q, arg1: q.put(com.readValues(arg1)), args=(que, "t"))
        #t1.start()
        #result = que.get()
        #print(result)"""

        t1 = threading.Thread(target=com.readValues)
        t1.start()

    def tulostaStream(self):
        print (results)

    def closeConnection(self):
        com.closeConnection()


    def lueThread(self):
        t1 = threading.Thread(target=com.readValues)
        t1.start()


#KKS-YLEISKASKYT

    def asetaViive(self):
        """Aseta viive 1-99 ms, jonka jälkeen vasta tablet (=SOVITIN???)= lähettää vastauksensa. Palauttaa #1"""
        com.setCommand("DELAY")
        #return "#DELAY"

    def tiedusteleTila(self):
        """Tiedustelee ja palauttaa tilan"""
        com.setCommand("STATE")
        #return "#STATE"

    def tiedusteleAika(self):
        """Tiedustelee ja palauttaa kalenterin ja ajan muodossa #RTC:pp.kk.vvvv-tt.mm.ss """
        com.setCommand("RTC:?")
        #return "#RTC:pp.kk.vvvv-tt.mm.ss """"

    def asetaAika(self, aika):
        """"asettaa ajan muodossa hh:mm:sss ja palauttaa 1"""
        com.setCommand("RTC:T:", aika)
        #return "#1"

    def asetaPaiva(self, paiva):
        """asettaa paivan muodossa pp.kk.vvvv ja palauttaa 1"""
        com.setCommand("RTC:D", paiva)
        #return "#1"

    # def tallennaPaiva(self):
    # #RTC:M 		PVM � tallennus KKS:ssa	"""
    # return com.setCommand("RTC:M")


    """HW-ASETUS / KYSELY"""
    def asetaSyvyydenVakio(self, pulssivakio):
    #palauttaa #1
        com.setCommand("SYV-PV:", pulssivakio, ":")
        #return "#1"

    def asetaPuolikierrostenVakio(self, pulssivakio):
        #palautta #1
        com.setCommand("PK-PV:", pulssivakio, ":")
        #return "#1"

    def kysyHwVakiot(self):
        # palauttaa syvyyden(SYV-PV) ja puolikierrosten (PK-PV) vakiot
        com.setCommand("?PULVA")
        #return "#PV:nnn.n-nn"

    def kysyAkkujenJannite(self):
        #Palauttaa jännitteen muodossa #AN0:nn.n:n.n
        com.setCommand("?AKKU")
        #return "#AN0:nn.n:n.n"



    """PISTEEN ALUSTUS"""
    def asetaHanke(self, tyonumero, hanke):
        """#HANKE:nnn..n:		HANKE Ty�numero, hanke"""
        """palauttaa #1"""
        com.setCommand("HANKE:", tyonumero, "..", hanke)
        #return "#1"

    def asetaPiste(self, piste):
        """#PISTE:ss..s:		kohdemuuttuja. palauttaa #1"""
        com.setCommand("PISTE", piste)
        #return "#1"

    def asetaTapa(self, tapa):
        """#TAPA:ccc-cc:		Tutkimustapa (TEK-PA,TEK-HE,TEK-PH,TEK-PO ...). palauttaa (SGF-PA,SGF-HE,SGF-PH,SGF-PO ...)"""
        com.setCommand(tapa)
        #return "#1"

    def tiedusteleTapa(self):
        """#?TAPA			palauta tutkimustavan #TAPA:ccc-cc:"""
        com.setCommand("?TAPA")
        #return "#TAPA:CCC-CC"


    """AN_KANAVAT"""
    def asetaKanavanNolla(self, kanava, nolla_arvo):
        """palauttaa #1"""
        com.setcommand("AN", kanava, "N:", nolla_arvo, ":")
        #return "#1"

    def asetaKanavanKerroin(self, kanava, kerroin):
        """palauttaa #1"""
        com.setCommand("AN", kanava, "K:", kerroin, ":")
        #return "#1"

    def annaKanavanAsetukset(self, kanava):
        """palauttaa kanavan asetukset: #AN1:N123:K1.123"""
        setCommand("?AN", kanava, "S")
        #return "#AN1:N123:K1.123"

    def annaKanavanTieto(self, kanava):
        """palauttaa kanavan tiedon: #AN1:2567:2222"""
        com.setCommand("?AN", kanava,"D:")
        #return "#AN1:2567:2222"




    """KAIRAUKSEN VALMISTELU"""

    def kuittaaTanko(self):
        """#TANKO			kuittaa tila pois. palauttaa #1"""
        com.setCommand("TANKO")
        #return "#1"

    def aloitaAlkukairaus(self):
        """aloittaa alkukairauksen, palauttaa #alkukairaus
        SIIRTYY ALKUKAIRAUSTILAAN -->
        TÄYTYY ALOITTAA KUUNTELU GUI:N PUOLELTA guioperations.kuunteleAlkukairausta() --> POLLAUSVÄLI 1S.
        PARSITAAN MYÖS #NOSKU #NOSTO"""
        com.setCommand('ALKUK:1')

    def aloitaOdotustila(self):
        """menee mittauksen odotustilaan josta jatketaan kairausta. Palauttaa #MIT_ODOTUS"""
        com.setCommand("M-ODOTUS")
        #return "MIT-ODOTUS"


    """ALKUKAIRAUSTILA"""

    """Tilaan tulo	 				< - - - - - -    #ALKUKAIRAUS 
    Alkukairaussyvyys 1s välein. 	< - - - - - -    #SYV:nnn
    Nosto asetettu KKS:ssa.			< - - - - - -    #NOSTO
    Nosto kuitattu KKS:ssa.			< - - - - - -    #NOSKU"""

    def kuunteleAlkukairausta(self):
        com.readValues()

    def asetaAlkusyvyys(self, syvyys):
        com.setCommand("ALKUSYV:", syvyys)

    def aloitaAlkutila(self):
        com.setCommand("HOME")

    def lopetaAlkukairaus(self):
        """lopettaa alkukairauksen ja siirtyy kairauksen odotustilaan (Saattaa palauttaa MIT_ODOTUS???)"""
        com.setCommand("ALKUK:0")


    """"MITTAUKSEN ODOTUSTILA"""
    def asetaKairaussyvyys(self, syvyys):
        com.setCommand("SYVYYS:", syvyys, ":")
        #return "#1"

    def aloitaMittaustila(self):
        """aloittaa mittauksen --> SIIRTYY MITTAUSTILAAN (MITTAUSTILA-2???)"""
        com.setCommand("START")

    def lopetaKairaus(self):
        """lopettaa kairauksen ja palaa alkutilaan Palauttaa END:123 15 vajaan patkan arvot (mitvit???) ja"""
        com.setCommand("END")
       # return "#END:123"


    """MITTAUSTILA-2"""
    def pysaytaKairaus(self):
        """lopettaa kairauksen ja siirtyy odotustilaan"""
        com.setCommand("STOP")
        #return "MIT-ODOTUS"

    def asetaSekuntiaskellus(self, askellus):
        com.setCommand("TIMER:", askellus, ":")
        #return "#1"

    """MITTAUSTILA-1"""
    #def aloitaKairaus(self):
        #com.setCommand("START")
        #return "#KAIRAUS"

    def kuunteleKairausta(self):
        com.readValues()


"""NOSTOTILA VAIKUTTAA HIEMAN SEKAVALTA
tilaan tulaan KKS-Komennolla, lähettää headerin #NOSTO. TULEEKO GUI:n PUOLELLE SIIRTYMÄÄ???"""

""""#STATE 	Tilan tiedustelu.		< - - - - - -   #NOSTO
 #TANKO 	Tangon kuittaus.		(< - - - - - -   #NOSKU)
            Jatkuu kairaustilana. 	< - - - - - -   #MITTAUSTILA
                                    
Kuittaus [Fn] painikkeella
Jatkuu kairaustilana.
(< - - - - -    #NOSKU)
< - - - - - -   #MITTAUSTILA"""


#TESTINGZONE

"""
gui = Guioperations()

gui.pysaytaKairaus()
gui.aloitaAlkutila()
gui.tiedusteleAika()
gui.aloitaAlkukairaus()
gui.lopetaAlkukairaus()
gui.aloitaMittaustila()

time.sleep(15)
gui.pysaytaKairaus()
gui.aloitaAlkutila()
com.closeConnection()

"""