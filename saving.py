#TODO
#Hoida tallennus loppuun
#alkukairauksen ja lopetussyyn tallennus?

"""Tämä luokka vastaa tiedostonkäsittelystä.
sisältää metodit
kks-parametrien tallennukseen,
kks-tallennussanomien tallennukseen,
aloituskenttien sisällön tallentamiseen,
kalibrointitiedot,
kielivalinnat ,
tallennuspolku,
kommunikaation hallinta(portti, baudi) ..."""


import sys
import time
import os.path
import configparser

class Saving (object):

    def __init__ (self):
        self.asetus_polku = os.path.dirname(os.path.abspath(__file__))
        self._config = configparser.ConfigParser()

        self._config.read("USECONTROL.ini", encoding='UTF-8')
        self.tal_polku = self._config["DEFAULT"]["polku"]
        if not os.path.exists(self.tal_polku):
            os.mkdir(self.tal_polku)


    #Määrittää tallenustiedoston kaikelle kks-laitteelta tulevalle datalle ja tallettaa sen
    def tallennaMIT(self, MIT):
        self._config.read("USECONTROL.ini", encoding='UTF-8')
        self.tal_polku = self._config["DEFAULT"]["polku"]
        if not os.path.exists(self.tal_polku):
            os.mkdir(self.tal_polku)
        self.tiedosto = "MIT_temp.txt"
        self.fullpath = os.path.join(self.tal_polku, self.tiedosto)
        file = open(self.fullpath, "w")
        file.write(MIT)

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
                                   "HANKE": hanke}
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
    def asetaAloitustiedot(self, FO="2.3", KJ="KKJ-N60", OM="TILAAJA", ML="GEO", ORG="GEOPOJAT"):
        '''self.fo = FO
        self.kj = KJ
        self.om = OM
        self.ml = ML
        self.org = ORG'''

        self._config["DEFAULT"] = {"FO": FO,
                                   "KJ": KJ,
                                   "OM": OM,
                                   "ML": ML,
                                   "ORG": ORG}
        with open ("ALOITUSTIEDOT.ini", "w") as cfgfile:
            self._config.write(cfgfile)

#lisää nämä
            '''Pisteen yleistiedot. Tiedosto voi sisältää useita pisteitä kairattuna
            eri menetelmillä. Kunkin pisteen alkuun tarjotaan tallennettavaksi
            tiedot ylläpidosta. Muuttuvat kentät päivitetään ylläpitoon.
            Näitä voidaan myös tarkastella/muuttaa omana ikkunana.
            Kentät ovat:
            # TYÖNUMERO	12345678
            # TYÖNIMI	POHJANTIE
            # LAITTEET	GM65-sn13256		'monitoimikaira
            # KAIRAAJA	S LAAKKONEN
            	TY  123456             HAILA				'työnumero     työnimi
	PK  0      MK						'pöytäkirja   0    kairaaja
	LA  GM75GT						'laitteet
            '''


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



    #METODIT JOTKA KOOSTAVAT VARSINAISEN TEKLATIEDOSTON
    # ottaa vastaan hankenimen = tallennustiedoston nimi, tallennuspolun (USECONTROL tiedosto), sekä tallenettavan TAL rivin ja kirjoittaa näm polunn tiedostoon

    def koostaHankeheader(self):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        self.hanke = self._config["DEFAULT"]["hanke"]

        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "w")

        #TIEDOSTOKOHTAISET
        self._config.read("ALOITUSTIEDOT.ini")
        file.write("FO\t" + self._config["DEFAULT"]["fo"] + "\n" +
                    "KJ\t" + self._config["DEFAULT"]["kj"] + "\n" +
                    "OM\t" + self._config["DEFAULT"]["om"] + "\n" +
                    "ML\t" + self._config["DEFAULT"]["ml"] + "\n" +
                    "OR\t" + self._config["DEFAULT"]["org"] + "\n")


    def koostaPisteheader(self):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        self.hanke = self._config["DEFAULT"]["hanke"]

        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "a")

        self._config.read("PISTETIEDOT.ini")

        file.write("TY\t" + self._config["DEFAULT"]["ty"] + "\n" +
                    "PK\t" + self._config["DEFAULT"]["pk"] + "\n" +
                    "LA\t" + self._config["DEFAULT"]["la"] + "\n")


    def koostaTutkimusheader(self):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        self.hanke = self._config["DEFAULT"]["hanke"]

        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "a")

        self._config.read("TUTKIMUSTIEDOT.ini")

        file.write("TT\t" + self._config["DEFAULT"]["tt"] + "\n" +
                    "TX\t" + self._config["DEFAULT"]["tx"] + "\n" +
                    "XY\t" + self._config["DEFAULT"]["xy"] + "\n" +
                    "LN\t" + self._config["DEFAULT"]["ln"] + "\n")

    def tallennaSYV(self, hanke, SYV):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        #self.hanke = self._config["DEFAULT"]["hanke"]

        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "a")
        file.write(SYV + "\n")


    def tallennaTAL(self, hanke, TAL):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        self.hanke = hanke + ".txt"
        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "a")
        file.write(TAL + "\n")

    #lisaa maalajin datarivin peraan vaihdettaessa
    def tallennaMaalaji(self, hanke, maalaji):
        self._config.read("USECONTROL.ini")
        self.tal_polku = self._config["DEFAULT"]["polku"]
        self.hanke = hanke
        self.fullpath = os.path.join(self.tal_polku, self.hanke)
        file = open(self.fullpath, "a")
        file.write(maalaji + "\n")



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
#sa.asetaParams("COM3", "9500", "c:/tmp/", "hanke1.txt")
#sa.asetaHWcontrol()
#sa.asetaAloitustiedot()
#sa.asetaPistetiedot("12344", "0 MK", "GM6364")
#sa.asetaTutkimustiedot("PA", "KALIBBLAA", "LALLAA")

#sa.koostaHankeheader()
#sa.koostaPisteheader()
#sa.koostaTutkimusheader()



#config = configparser.ConfigParser()
#config.read("USECONTROL.ini")
#print(config["DEFAULT"]["port"])
#sa.asetaAsetuspolku('C:/testi/')
#sa.asetaKommunikaatio("COM1", "9600")

