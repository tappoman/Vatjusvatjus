#TODO
#Hoida tallennus loppuun
#Testaa palauttaako threadi oikean alimman rivin.


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



import sys, time, os.path

class Saving (object):

    def __init__ (self, mittaus_polku="", asetus_polku="", port="", baud="" ):
        self.mittaus_polku = mittaus_polku
        self.asetus_polku = asetus_polku
        self.port = port
        self.baud = baud

    #asettaa polun tallennettavalle datalle ja mittaukseen liittyville parametreille
    #ottaa polun vastaan muododssa 'C:/POLKU/'
    def asetaMittauspolku(self, polku):
        self.mittaus_polku = polku


    #sisältää "kiinteät" yksittäisestä mittauksesta riippumattomat asetukset esim. com
    def asetaAsetuspolku(self, polku):
        self.asetus_polku = polku
        if not os.path.exists(self.asetus_polku):
            os.makedirs(self.asetus_polku)

    #sisältää "kiinteät" yksittäisestä mittauksesta riippumattomat asetukset esim. com
    def asetaMITpolku(self, polku):
        self.asetus_polku = polku
        if not os.path.exists(self.asetus_polku):
            os.makedirs(self.asetus_polku)


    def asetaKommunikaatio(self, port, baud):
        self.port = port
        self.baud = baud

        #tallennettaan kommunikaatioasetukset tiedostoon asetuspolunmääräämään kansioon:
        self.tiedosto = "com_params.txt"
        self.fullpath = os.path.join(self.asetus_polku, self.tiedosto)
        file = open(self.fullpath, "w")
        file.write(self.port + ";" + self.baud)

    def tallennaMIT(self, MIT):
        file = open("c:/TMP/MIT_data.txt", "a")
        file.write(MIT + "\n")

    #def tallennaParametrit (self, params):

#sa = Saving()
#sa.asetaAsetuspolku('C:/testi/')
#sa.asetaKommunikaatio("COM1", "9600")

