#TODO
#Hoida tallennus loppuun

"""Tämä luokka vastaa tiedostonkäsittelystä.
sisältää metodit
kks-parametrien tallennukseen,
kks-tallennussanomien tallennukseen,
aloituskenttien sisällön tallentamiseen,
kalibrointitiedot,
kielivalinnat ,
tallennuspolku,
kommunikaation hallinta(portti, baudi) ..."""


#Eli Kansio_1 --> Hankkeen nimi:
#Tiedoston nimi --> Piste
#Headeri --> Työnumero, Tutkimustapa, sijainti (E, N, syvyys). Päivämäärä, kalibrointiarvot
#    --> perään TAL:

#Maalaji (lisätään myös syvyyteen X kun maalaji muuttuu)

#Tiedosto_2 (asetukset): Portti, baudi, polku,



import sys
import time
import os.path
import configparser

class Saving (object):

    def __init__ (self, tal_polku="", port="", baud="" ):
        self.tal_polku = tal_polku
        self.asetus_polku = os.path.dirname(os.path.abspath(__file__))
        self.port = port
        self.baud = baud
        self.TAL_fullpath = ""
        self._config = configparser.ConfigParser()


    #Määrittää tallenustiedoston kaikelle kks-laitteelta tulevalle datalle ja tallettaa sen
    def tallennaMIT(self, MIT):
        self.tiedosto = "MIT_temp.txt"
        self.fullpath = os.path.join(self.tal_polku, self.tiedosto)
        file = open(self.fullpath, "a")
        file.write(MIT + "\n")

    #asettaa polun tallennettavalle datalle ja kommunikaation liittyville parametreille (baud, port)
    #ottaa polun vastaan muododssa 'C:/POLKU/'
    #tallennettaaan kaikki data määriteltyyn TALLENNUS kansioon rivi kerrallaan ts. parsittava tiedosto.txt
    def asetaParams(self, port, baud, talpolku, hanke):
        self.port = port
        self.baud = baud
        self.tal_polku = talpolku

        #tallennettaan kommunikaatioasetukset tiedostoon asetuspolunmääräämään kansioon = ohjelmistokansio
        #cfgfile = open(self.asetus_polku + "USECONTROL.ini", "w")
        self._config["DEFAULT"] = {"PORT": self.port,
                                   "BAUD": self.baud,
                                   "POLKU": self.tal_polku,
                                   "TIEDOSTO": hanke}
        with open ("USECONTROL.ini", "w") as cfgfile:
            self._config.write(cfgfile)


    def asetaHWcontrol(self, LOGGING=20, PULS_CM=45.55, PULS_PK=30):
        self.logging = LOGGING
        self.puls_cm = PULS_CM
        self.puls_pk = PULS_PK

        self._config["DEFAULT"] = {"LOGGING": self.logging,
                                   "PULS_CM": self.puls_cm,
                                   "PULS_PK": self.puls_pk}
        with open ("HWCONTROL.ini", "w") as cfgfile:
            self._config.write(cfgfile)

    #tee nämä joskus
    def asetaANparams(self):
        '''PK-VOIMA	N256	K0.255	P25.01.2018	'AN2 nollaus, kerroin, kalibrointipäiväys
        # PH-VOIMA	N344	K1.245	P25.01.2018	'AN1  -- " --
        # PH-VÄÄNTÖ	N299	K1.945	P25.01.2018	'AN3  -- " --
        # VESI-VI	N299	K1.945	P25.01.2018	'AN4  -- " --	SGF tarve myöhemmin
        # VESI-PA	N299	K1.945	P25.01.2018	'AN5  -- " --	SGF tarve myöhemmin
        # VASARA		N299	K1.945	P25.01.2018	'AN6  -- " --	SGF tarve myöhemmin'''


    #Aina tiedoston alkuun, määritellään ylläpidosta
    def asetaAloitustiedot(self, FO="2.3", KJ="KKJ-N60", OM="TILAAJA", ML="GEO", ORG="GEOpojat"):
        '''self.fo = FO
        self.kj = KJ
        self.om = OM
        self.ml = ML
        self.org = ORG'''

        self._config["DEFAULT"] = {"FO": FO,
                                   "KJ": KJ,
                                   "OM": OM,
                                   "ML": ML,
                                   "OR": ORG}
        with open ("ALOITUSTIEDOT.ini", "w") as cfgfile:
            self._config.write(cfgfile)

        #self.tiedosto = "ALOITUSTIEDOT.txt"
        #self.fullpath = os.path.join(self.asetus_polku, self.tiedosto)
        #file = open(self.fullpath, "w")
        #file.write("FO \t" + self.fo + "\n" + "KJ \t" + self.kj + "\n" + "OM \t" + self.om + "\n" +
        #           "ML \t" + self.ml + "\n" + "OR \t" + self.org + "\n")


    #pistekohtaiset tiedot, aina uuden pisteen alkuun
    def asetaPistetiedot(self, TY, PK, LA):
        self._config["DEFAULT"] = {"TY": TY,
                                   "PK": PK,
                                   "LA": LA}
        with open ("PISTETIEDOT.ini", "w") as cfgfile:
            self._config.write(cfgfile)

        '''self.ty = TY
        self.pk = PK
        self.la = LA
        self.tiedosto = "PISTETIEDOT.txt"
        self.fullpath = os.path.join(self.asetus_polku, self.tiedosto)
        file = open(self.fullpath, "w")
        file.write("TY \t" + self.ty + "\n" + "PK \t" + self.pk + "\n" + "LA \t" + self.la + "\n")'''


    def asetaTutkimustiedot(self, TT, TX, XY, LN="-\t" + "-\t"):
        self._config["DEFAULT"] = {"TT": TT,
                                   "TX": TX,
                                   "XY": XY,
                                   "LN": LN}
        with open ("TUTKIMUSTIEDOT.ini", "w") as cfgfile:
            self._config.write(cfgfile)

        '''self.tt = TT
        self.tx = TX
        self.xy = XY
        self.ln = LN

        self.tiedosto = "TUTKIMUSTIEDOT.txt"
        self.fullpath = os.path.join(self.asetus_polku, self.tiedosto)
        file = open(self.fullpath, "w")
        file.write("TT \t" + self.tt + "\n" "TX \t" + self.tx + "\n" + "XY \t" + self.xy + "\n" + "LN \t" + self.ln + "\n")'''


        # ottaa vastaan hankenimen = tallennustiedoston nimi, tallennuspolun (USECONTROL tiedosto), sekä tallenettavan TAL rivin ja kirjoittaa näm polunn tiedostoon
        def tallennaTAL(self, hanke, polku, TAL):
            self.TALtiedosto = hanke
            self.TAL_fullpath = os.path.join(polku, self.TALtiedosto)
            file = open(self.fullpath, "a")
            file.write(TAL + "\n")



        # sisältää "kiinteät" yksittäisestä mittauksesta riippumattomat asetukset esim. com
        # Tätä ei tarvita, asetukset tulevat ohjelmistokansioon!!!.
        '''def asetaAsetuspolku(self, polku):
            self.asetus_polku = polku
            if not os.path.exists(self.asetus_polku):
                os.makedirs(self.asetus_polku)'''

        # sisältää "kiinteät" yksittäisestä mittauksesta riippumattomat asetukset esim. com
        '''def asetaMITpolku(self, polku):
            self.asetus_polku = polku
            if not os.path.exists(self.asetus_polku):
                os.makedirs(self.asetus_polku)'''

        #def tallennaParametrit (self, params):

#sa = Saving()
#sa.asetaParams("COM3", "9500", "polkupapolku", "hanke1.txt")
#sa.asetaHWcontrol()

#config = configparser.ConfigParser()
#config.read("USECONTROL.ini")
#print(config["DEFAULT"]["port"])
#sa.asetaAsetuspolku('C:/testi/')
#sa.asetaKommunikaatio("COM1", "9600")

