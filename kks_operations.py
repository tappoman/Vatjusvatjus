﻿#Class which pass all the commands from gui to communication class

from communication import *
import threading
import time
import sys
import serial
import os
import time
import queue

class Kksoperations (object):

    def __init__(self, com=None):

        self.com = com
        self.t1 = threading.Thread(target=self.com.readValues)
        self.t1.start()

    def tulostaStream(self):
        print(results)

    def closeConnection(self):
        #print("suletaan")
        self.com.closeConnection()

    def lueThread(self):
        t1 = threading.Thread(target=self.com.readValues)
        t1.start()

    def annaKasky(self, command):
        self.com.setCommand(command)


#KKS-YLEISKASKYT

    def asetaViive(self):
        """Aseta viive 1-99 ms, jonka jälkeen vasta tablet (=SOVITIN???)= lähettää vastauksensa. Palauttaa #1"""
        self.com.setCommand("DELAY")
        #return "#DELAY"

    def tiedusteleTila(self):
        """Tiedustelee ja palauttaa tilan"""
        self.com.setCommand("STATE")
        #return "#STATE"

    def tiedusteleAika(self):
        """Tiedustelee ja palauttaa kalenterin ja ajan muodossa #RTC:pp.kk.vvvv-tt.mm.ss """
        self.com.setCommand("RTC:?")
        #return "#RTC:pp.kk.vvvv-tt.mm.ss """"

    def asetaAika(self, aika):
        """"asettaa ajan muodossa hh:mm:sss ja palauttaa 1"""
        self.com.setCommand("RTC:T:", aika)
        #return "#1"

    def asetaPaiva(self, paiva):
        """asettaa paivan muodossa pp.kk.vvvv ja palauttaa 1"""
        self.com.setCommand("RTC:D", paiva)
        #return "#1"

    # def tallennaPaiva(self):
    # #RTC:M 		PVM � tallennus KKS:ssa	"""
    # return self.com.setCommand("RTC:M")


    """HW-ASETUS / KYSELY"""
    def asetaSyvyydenVakio(self, pulssivakio):
    #palauttaa #1
        self.com.setCommand("SYV-PV:" + str(pulssivakio))
        #return "#1"

    def asetaPuolikierrostenVakio(self, pulssivakio):
        #palautta #1
        self.com.setCommand("PK-PV:" + str(pulssivakio))
        #return "#1"

    def kysyHwVakiot(self):
        # palauttaa syvyyden(SYV-PV) ja puolikierrosten (PK-PV) vakiot
        self.com.setCommand("?PULVA")
        #return "#PV:nnn.n-nn"

    def kysyAkkujenJannite(self):
        #Palauttaa jännitteen muodossa #AN0:nn.n:n.n
        self.com.setCommand("?AKKU")
        #return "#AN0:nn.n:n.n"



    """PISTEEN ALUSTUS"""
    def asetaHanke(self, hanke):
        """#HANKE:nnn..n:		HANKE Ty�numero, hanke"""
        """palauttaa #1"""
        self.com.setCommand("HANKE:" + hanke)
        #return "#1"

    def asetaPiste(self, piste):
        """#PISTE:ss..s:		kohdemuuttuja. palauttaa #1"""
        self.com.setCommand("PISTE:" + piste)
        #return "#1"

    def asetaTapa(self, tapa):
        """#TAPA:ccc-cc:		Tutkimustapa (TEK-PA,TEK-HE,TEK-PH,TEK-PO ...). palauttaa (SGF-PA,SGF-HE,SGF-PH,SGF-PO ...)"""
        #print("TAPA:" + tapa)
        self.com.setCommand("TAPA:TEK-" + tapa)
        #return "#1"

    def tiedusteleTapa(self):
        """#?TAPA			palauta tutkimustavan #TAPA:ccc-cc:"""
        self.com.setCommand("?TAPA")
        #return "#TAPA:CCC-CC"


    """AN_KANAVAT"""
    def asetaKanavanNolla(self, kanava, nolla_arvo):
        """palauttaa #1"""
        self.com.setcommand("AN", kanava, "N:", nolla_arvo, ":")
        #return "#1"

    def asetaKanavanKerroin(self, kanava, kerroin):
        """palauttaa #1"""
        self.com.setCommand("AN", kanava, "K:", kerroin, ":")
        #return "#1"

    def annaKanavanAsetukset(self, kanava):
        """palauttaa kanavan asetukset: #AN1:N123:K1.123"""
        setCommand("?AN", kanava, "S")
        #return "#AN1:N123:K1.123"

    def annaKanavanTieto(self, kanava):
        """palauttaa kanavan tiedon: #AN1:2567:2222"""
        self.com.setCommand("AN", kanava,"D:")
        #return "#AN1:2567:2222"




    """KAIRAUKSEN VALMISTELU"""

    def kuittaaTanko(self):
        """#TANKO			kuittaa tila pois. palauttaa #1"""
        self.com.setCommand("TANKO")
        #return "#1"

    def aloitaAlkukairaus(self):
        """aloittaa alkukairauksen, palauttaa #alkukairaus
        SIIRTYY ALKUKAIRAUSTILAAN -->
        PARSITAAN MYÖS #NOSKU #NOSTO"""
        self.com.setCommand('ALKUK:1')

    def aloitaOdotustila(self):
        """menee mittauksen odotustilaan josta jatketaan kairausta. Palauttaa #MIT_ODOTUS"""
        self.com.setCommand("STOP")
        #return "MIT-ODOTUS"

    def aloitaOdotustila(self):
        self.com.setCommand("M-ODOTUS")

    def asetaAlkusyvyys(self, syvyys):
        self.com.setCommand("ALKUSYV:" + syvyys)

    def aloitaAlkutila(self):
        self.com.setCommand("HOME")

    def lopetaAlkukairaus(self):
        """lopettaa alkukairauksen ja siirtyy kairauksen odotustilaan (Saattaa palauttaa MIT_ODOTUS???)"""
        self.com.setCommand("ALKUK:0")


    """"MITTAUKSEN ODOTUSTILA"""
    def asetaKairaussyvyys(self, syvyys):
        self.com.setCommand("SYVYYS:" + str(syvyys))
        #return "#1"

    def aloitaKairaus(self):
        """aloittaa mittauksen --> SIIRTYY MITTAUSTILAAN (MITTAUSTILA-2???)"""
        self.com.setCommand("START")

    def lopetaKairaus(self):
        """lopettaa kairauksen ja palaa alkutilaan Palauttaa END:123 15 vajaan patkan arvot"""
        self.com.setCommand("END")
       # return "#END:123"


    """MITTAUSTILA-2"""
    def pysaytaKairaus(self):
        """lopettaa kairauksen ja siirtyy odotustilaan"""
        self.com.setCommand("STOP")
        #return "MIT-ODOTUS"

    def asetaSekuntiaskellus(self, askellus):
        self.com.setCommand("TIMER:" + askellus)
        #return "#1"

    """MITTAUSTILA-1"""
    #def aloitaKairaus(self):
        #self.com.setCommand("START")
        #return "#KAIRAUS"

    def kuunteleKairausta(self):
        self.com.readValues()

