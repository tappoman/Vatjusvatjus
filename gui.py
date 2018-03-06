'''
luokka käyttöliittymän hallintaan
parsii tiedot communications luokalta
ja siirtää ne bar_graph luokalle

tarvittavat kirjastot:
wxpython
wx.lib.scrolledpanel
'''

import wx
import os
import wx.lib.scrolledpanel as scrolled
import re
import configparser
import shutil
import saving
from saving import *
from kks_operations import *
from piirto import *
import time

import communication
# import guioperations
# import threading
# import serial

#com = Communication()

class windowClass(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, size=wx.Size(600, 960))

        self.Centre()
        self.basicGUI()
        self.data = TiedonKasittely(gui=self)

        #self.timer = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.data.ikuuntele, self.timer)
        self.config = configparser.ConfigParser()

        self.sa = Saving
        #self.com = Communication()

        self.timer = wx.Timer(self)
        #self.timer2 = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.data.ikuuntele, self.timer)

        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        #self.Bind(wx.EVT_TIMER, self.updatepistearvot(self.data), self.timer2)

    def onClose(self):
        self.data.kks.kuittaaTanko()
        self.data.kks.lopetaKairaus()
        self.data.kks.aloitaAlkutila()
        self.data.kks.closeConnection()


    def basicGUI(self):

        panel = wx.Panel(self, wx.ID_ANY)
        self.SetTitle('Vatjus 3000')
        font1 = self.GetFont()
        font2 = self.GetFont()
        font3 = self.GetFont()
        font1.SetPointSize(15)
        font2.SetPointSize(25)
        font3.SetPointSize(35)

        # nappuloiden alustus
        #Framen sulkemisnappi
        #closeBtn = wx.Button(panel, label="Close")
        #closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.suljelistener)

        # hanke
        # avaa hankkeen listalta
        self.hankebutton = wx.Button(panel, label="Valitse\nhanke", pos=(5, 10), size=(110, 110))
        self.hankebutton.SetFont(font1)
        self.hankebutton.Bind(wx.EVT_BUTTON, self.hankkeenavaus)

        # piste
        # avaa pisteen hankkeen sisältä
        self.pistebutton = wx.Button(panel, label="valitse piste/\nluo uusi piste", pos=(120, 10), size=(110, 110))
        self.pistebutton.SetFont(font1)
        self.pistebutton.Bind(wx.EVT_BUTTON, self.pisteenavaus)
        self.pistebutton.Disable()

        # tutkimus-tapa
        #
        self.ohjelmabutton = wx.Button(panel, label="Tutkimus-\ntapa", pos=(235, 10), size=(110, 110))
        self.ohjelmabutton.SetFont(font1)
        self.ohjelmabutton.Bind(wx.EVT_BUTTON, self.valitseohjelma)

        # Tietojen hallinta
        # muokataan .ini-tiedostoja
        self.hallintabutton = wx.Button(panel, label="Tietojen\nhallinta", pos=(350, 10), size=(110, 110))
        self.hallintabutton.SetFont(font1)
        self.hallintabutton.Bind(wx.EVT_BUTTON, self.hallintamenu)

        # maalaji
        # käyttäjä asettaa maalajin listalta
        self.maalajibutton = wx.Button(panel, label="Maalaji", pos=(465, 10), size=(110, 110))
        self.maalajibutton.SetFont(font1)
        self.maalajibutton.Bind(wx.EVT_BUTTON, self.valitsemaalaji)
        self.maalajibutton.Disable()

        # hae
        # communications listenerin mockup
        self.huombutton = wx.Button(panel, label="Kirjoita\nhuom", pos=(400, 125), size=(75, 75))
        self.huombutton.SetFont(font1)
        self.huombutton.Bind(wx.EVT_BUTTON, self.kommenttirivi)
        self.huombutton.Disable()

        # kks koment.
        # lähettää kkssälle käyttäjän antaman komennon
        self.alustabutton = wx.Button(panel, label="kks\nkomen.", pos=(480, 125), size=(75, 75))
        self.alustabutton.SetFont(font1)
        self.alustabutton.Bind(wx.EVT_BUTTON, self.komennakks)

        # piirto
        # käyttäjä voi valita piirtonäkymän
        self.graphbutton = wx.Button(panel, label="Piirto", pos=(10, 215), size=(100, 100))
        self.graphbutton.SetFont(font1)
        self.graphbutton.Bind(wx.EVT_BUTTON, self.graafinpiirto)
        self.graphbutton.Disable()

        # alkukairaus
        # käyttäjä valitsee kairaustyypin ja alkusyvyyden, joka lähetetään kkssälle
        self.alkukairausbutton = wx.Button(panel, label="Alku\nkairaus", pos=(120, 215), size=(100,100))
        self.alkukairausbutton.SetFont(font1)
        self.alkukairausbutton.Bind(wx.EVT_BUTTON, self.aloitaalkukairaus)
        self.alkukairausbutton.Disable()
        # kairauksen lopetus
        # käyttäjä valitsee lopetussyyn
        # tiedot kkssälle
        self.lopetusbutton = wx.Button(panel, label="Aloita\nkairaus", pos=(400, 215), size=(100,100))
        self.lopetusbutton.SetFont(font1)
        self.lopetusbutton.Bind(wx.EVT_BUTTON, self.lopetakairaus)
        self.lopetusbutton.Disable()

        # tankobutton
        # heilutellaan sitä tankoa
        # disco
        self.tankobutton = wx.Button(panel, label="Tanko", pos=(500, 215), size=(75, 75))
        self.tankobutton.SetFont(font1)
        self.tankobutton.Bind(wx.EVT_BUTTON, self.tanko)

        # tietotekstien alustus
        self.hanketeksti = wx.StaticText(panel, -1, "Hanke: ", pos=(10, 120))
        self.hanketeksti.SetFont(font2)

        # tiedostonimiteksti näyttää valitun hankkeen nimen
        self.hankenimiteksti = wx.StaticText(panel, -1, "", pos=(120, 120))
        self.hankenimiteksti.SetFont(font2)

        self.pisteteksti = wx.StaticText(panel, -1, "Työnro: ", pos=(10, 165))
        self.pisteteksti.SetFont(font2)

        # pistenimiteksti näyttää valitusta hankkeesta valitun pisteen
        self.pistenimiteksti = wx.StaticText(panel, -1, "", pos=(120, 165))
        self.pistenimiteksti.SetFont(font2)

        # ohjelmanimiteksti näyttää valitusta ohjelmanappulasta käytössäolevan ohjelman
        self.ohjelmateksti = wx.StaticText(panel, -1, "TT:", pos=(230, 210))
        self.ohjelmateksti.SetFont(font1)

        self.ohjelmaarvoteksti = wx.StaticText(panel, -1, "", pos=(260, 210))
        self.ohjelmaarvoteksti.SetFont(font1)

        # alkukairausteksti päivittyy käyttäjän valinnan mukaan
        self.alkukairausteksti = wx.StaticText(panel, -1, "AL:", pos=(230, 245))
        self.alkukairausteksti.SetFont(font1)

        self.alkukairausarvoteksti = wx.StaticText(panel, -1, "", pos=(260, 245))
        self.alkukairausarvoteksti.SetFont(font1)

        self.alkusyvyysteksti = wx.StaticText(panel, -1, "A-syv:", pos=(230, 280))
        self.alkusyvyysteksti.SetFont(font1)

        self.alkusyvyysarvoteksti = wx.StaticText(panel, -1, "0", pos=(295, 280))
        self.alkusyvyysarvoteksti.SetFont(font1)

        # alatekstien alustus
        self.syvyysteksti = wx.StaticText(panel, -1, "Syvyys", pos=(10, 315))
        self.syvyysteksti.SetFont(font1)

        # syvyysarvoteksti päivittyy alkusyvyys + listeneriltä tuleva syvyys
        self.syvyysarvoteksti = wx.StaticText(panel, -1, "", pos=(10, 345))
        self.syvyysarvoteksti.SetFont(font2)

        self.voimateksti = wx.StaticText(panel, -1, "Voima", pos=(120, 315))
        self.voimateksti.SetFont(font1)

        # voima-arvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.voimaarvoteksti = wx.StaticText(panel, -1, "", pos=(120, 345))
        self.voimaarvoteksti.SetFont(font2)

        self.puolikierroksetteksti = wx.StaticText(panel, -1, "P-kierr", pos=(200, 315))
        self.puolikierroksetteksti.SetFont(font1)

        # puolikierroksetarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.puolikierroksetarvoteksti = wx.StaticText(panel, -1, "", pos=(200, 345))
        self.puolikierroksetarvoteksti.SetFont(font2)

        self.nopeusteksti = wx.StaticText(panel, -1, "Nopeus", pos=(305, 315))
        self.nopeusteksti.SetFont(font1)

        # nopeusarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.nopeusarvoteksti = wx.StaticText(panel, -1, "", pos=(305, 345))
        self.nopeusarvoteksti.SetFont(font2)

        self.maalajiteksti = wx.StaticText(panel, -1, "Maalaji", pos=(400, 315))
        self.maalajiteksti.SetFont(font1)

        # maalajiarvoteksti päivittyy käyttäjän valitessa maalaji
        self.maalajiarvoteksti = wx.StaticText(panel, -1, "", pos=(400, 345))
        self.maalajiarvoteksti.SetFont(font2)

        self.tankoteksti = wx.StaticText(panel, -1, "Tanko", pos=(525, 315))
        self.tankoteksti.SetFont(font1)

        #  tankoarvolaatikko vaihtaa väriä tarpeen mukaan
        self.tankoarvolaatikko = wx.Panel(panel, pos=(525, 345), size=(50,50))
        self.tankoarvolaatikko.SetBackgroundColour('red')

        # kirjoituspaneelin ja tekstielementtien alustus
        # addspacer paddaa paneelin ylälaidan arvotekstien alapuolelle
        self.scrolled_panel = scrolled.ScrolledPanel(panel, -1, style=wx.SUNKEN_BORDER)
        self.spSizer = wx.BoxSizer(wx.VERTICAL)
        self.scrolled_panel.SetSizer(self.spSizer)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.AddSpacer(400)
        panelSizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        panel.SetSizer(panelSizer)

    #TANKOVARITYSTA
    def vaihdatankovari(self, color):
        self.tankoarvolaatikko.SetBackgroundColour(color)
        self.tankoarvolaatikko.Refresh()

    #alustetaan näyttöarvot kairaustavan mukaan:
    # PAINOK : Syvyys, voima, puolikierrokset, nopeus, maalaji
    # HEIJARIK : syvyys, heijari / isku
    # PORAKAIR : syvyys, aika
    # TÄRYKAIR : syvyys
    # PUR. / HEIJ.K : syvyys, voima/paine, vääntö vaihe P
    # PUR. / HEIJ.K : syvyys, iskut,vääntö, vaihe H
    def alustaarvopaneeli(self, kairaustapa):

        if kairaustapa == "PA":
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("Voima")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("P-kierr")
            self.puolikierroksetarvoteksti.SetLabelText("0")
            self.nopeusteksti.SetLabelText("Nopeus")
            self.nopeusarvoteksti.SetLabelText("0")

        if kairaustapa == "HE":
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("H / I")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabelText("")
            self.nopeusteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")

        if kairaustapa == "PO":
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("Aika")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("Tnk. nop")
            self.puolikierroksetarvoteksti.SetLabelText("0")
            self.nopeusteksti.SetLabelText("Pyör. nop")
            self.nopeusarvoteksti.SetLabelText("0")
            lista = ["KELLO","EI KELLOA"]
            kello = wx.SingleChoiceDialog(None, "Aloitetaanko kello?", "Porakairaus kello", lista,
                                            wx.CHOICEDLG_STYLE)
            if kello.ShowModal() == wx.OK:
                print("tässä pitäisi lähettää kkssälle tieto kellon aloituksesta")
                kello.Destroy()
                return None
            else:
                kello.Destroy()
                return None

        if kairaustapa == "TR":
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("")
            self.voimaarvoteksti.SetLabelText("")
            self.puolikierroksetteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabelText("")
            self.nopeusteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")

        if kairaustapa == "PH":
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("Voima")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("Vääntö")
            self.puolikierroksetarvoteksti.SetLabelText("0")
            self.nopeusteksti.SetLabelText("P / H")
            self.nopeusarvoteksti.SetLabelText("P")

    def hankkeenavaus(self, event):
        if self.hankenimiteksti.GetLabel() != "":
            self.hankenimiteksti.SetLabelText("")
            self.pistenimiteksti.SetLabelText("")
            self.syvyysarvoteksti.SetLabelText("")
            self.voimaarvoteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")
            self.graphbutton.Disable()
            self.alkukairausbutton.Disable()
            self.lopetusbutton.Disable()
            self.huombutton.Disable()
            self.data.iavaahanke()
            self.update(event)
            self.timer.Start(50)
        else:
            self.data.iavaahanke()
            self.update(event)
            self.timer.Start(50)
            try:
                self.hankenimiteksti.SetLabelText(self.data.hanke)
                self.pistebutton.Enable()
            except TypeError:
                print("Hanketta ei avattu")

    # jos ei luoda uutta pistettä, niin jatketaan vanhasta
    # avataan tekstifile, joka luetaan kunnes viimeinen pistenimi-tunnistin tulee
    # ja tämän perään jatketaan datan kirjoittamista
    def pisteenavaus(self, event):
        self.data.piste = ""
        self.pistenimiteksti.SetLabelText("")
        self.alkukairausbutton.Disable()
        self.lopetusbutton.Disable()
        self.graphbutton.SetLabelText("Piirto")
        self.graphbutton.Disable()
        self.maalajibutton.Disable()
        self.syvyysarvoteksti.SetLabelText("")
        self.data.syvyys = 0
        self.data.iavaapiste()
        #self.update(event)
        #self.timer.Start(50)

    #tarkistetaan onko pisteessä mittaustietoja
    def tarkistapiste(self):
        piste = []
        pistevalinta = self.pistenimiteksti.GetLabel().strip()
        syvyyslista = []
        printtilista = []
        parsilista = []
        os.chdir(self.data.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hankenimiteksti.GetLabel()), "r")
        tiedosto = file.readlines()
        file.close()

        for line in tiedosto:
            if line.__contains__(pistevalinta):
                piste.append(line)
                alku = tiedosto.index(line) + 1
                while alku < len(tiedosto):
                    linepartindex = tiedosto[alku]
                    if linepartindex[0:2] == ("ty"):
                        break
                    else:
                        piste.append(linepartindex)
                        alku = alku + 1

        for rivi in piste[::-1]:
            if rivi.__contains__("HM"):
                continue
            elif rivi == "\n":
                continue
            elif rivi.__contains__("ln"):
                break
            else:
                syvyyslista.append(rivi)
        syvyyslista.reverse()

        for s in syvyyslista:
            if s == "\n":
                syvyyslista.remove(s)
            else:
                parsilista.append(s.rsplit(None, 3))

        for i in parsilista:
            if len(printtilista) < len(syvyyslista):
                printtilista.append(i[0])

        if printtilista == []:
            varoitus = wx.MessageDialog(None, "Pisteessä ei ole mittaustuloksia", "Huom!")
            varoitus.ShowModal()
            varoitus.Destroy()
            return None
        else:
            return True

    def aloitaalkukairaus(self, event):
        if self.hankenimiteksti.GetLabel() == "":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        elif self.alkukairausbutton.GetLabelText()=="Lopeta\nalkukair.":
            self.data.kks.lopetaAlkukairaus()
            self.lopetusbutton.Enable()
            self.alkukairausbutton.Enable()
            self.tankobutton.Enable()
            self.alkukairausbutton.SetLabelText("Alku\nkairaus")



        else:
            self.data.kks.asetaHanke(self.data.piste, self.data.hanke)
            self.data.kks.asetaPiste(self.data.piste)
            self.data.kks.asetaTapa(self.data.tutkimustapa)
            self.graphbutton.Enable()
            os.chdir(self.data.root)
            z = []
            with open("alkukairaus.txt", "r") as textfile:
                for line in textfile:
                    if len(line) > 1:
                        z.append(line.rsplit(" ")[1].strip("\n"))
            textfile.close()
            kairausvalinta = wx.SingleChoiceDialog(None, "Valitse alkukairaustapa", "Alkukairaus", z, wx.CHOICEDLG_STYLE)
            if kairausvalinta.ShowModal() == wx.ID_OK:
                kairausvalinta = kairausvalinta.GetStringSelection()
                if kairausvalinta == "OHITETAAN":
                    self.lopetusbutton.Enable()
                    self.tankobutton.Enable()
                    self.data.kks.aloitaOdotustila()
                    self.data.kks.asetaKairaussyvyys("0")
                    self.config.read("USECONTROL.ini")
                    os.chdir(self.config["DEFAULT"]["polku"])
                    #with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                    #    textfile.write("\n" + "alkukairaus ohitetaan\n")
                    #    textfile.close()
                    os.chdir(self.data.root)
                else:
                    with open("alkukairaus.txt", "r") as textfile:
                        for line in textfile:
                            if line.__contains__(kairausvalinta):
                                self.alkukairausarvoteksti.SetLabelText(line[1:3])
                    alkusyvyys = wx.TextEntryDialog(None, 'Aseta alkusyvyys sentteinä',"Alkusyvyys","",
                                                    style=wx.OK)
                    alkusyvyys.Centre()
                    alkusyvyys.ShowModal()
                    self.alkusyvyysarvoteksti.SetLabelText(alkusyvyys.GetValue())
                    self.data.asetaalkusyvyys(int(alkusyvyys.GetValue()))
                    self.data.kks.asetaAlkusyvyys(alkusyvyys.GetValue())

                    print(alkusyvyys.GetValue())
                    self.data.kks.lopetaAlkukairaus()
                    alkusyvyys.Destroy()
                    self.alkukairausbutton.SetLabelText("Lopeta\nalkukair.")
                    self.config.read("USECONTROL.ini")
                    os.chdir(self.config["DEFAULT"]["polku"])

                    #with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                    #    textfile.write("\n" + "alkukairaus: {} syvyydellä {}\n".format(self.data.syvyys, kairausvalinta))
                    #    textfile.close()

                    os.chdir(self.data.root)
                    self.data.kks.aloitaAlkukairaus()
            else:
                return None

    def lopetakairaus(self, event):
        if self.hankenimiteksti.GetLabel() == "":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        elif self.lopetusbutton.GetLabel() == "Lopeta\nkairaus":
            self.data.kks.kuittaaTanko()
            time.sleep(0.5)
            self.data.kks.lopetaKairaus()
            self.alkukairausbutton.Enable()
            self.tankobutton.Enable()
            self.vaihdatankovari('red')
            os.chdir(self.data.root)
            z = []
            with open("kairausloppu.txt", "r") as textfile:
                for line in textfile:
                    if len(line) > 1:
                        if line.__contains__("TIIVIS"):
                            z.append(line.strip(",TM" + "\n"))
                        elif line.__contains__("KALLIO"):
                            z.append(line.strip(",KA" + ",KK" + "\n"))
                        else:
                            z.append(line.rsplit(" ")[1].strip("\n"))
            textfile.close()
            kairausvalinta = wx.SingleChoiceDialog(None, "Valitse lopetussyy", "Kairauksen lopetus", z,
                                                   wx.CHOICEDLG_STYLE)
            if kairausvalinta.ShowModal() == wx.ID_OK:
                kairausvalinta = kairausvalinta.GetStringSelection()
                self.config.read("USECONTROL.ini")
                os.chdir(self.config["DEFAULT"]["polku"])
                with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                    textfile.write("\n" + "-1\t{}\n".format(self.data.syvyys, kairausvalinta))
                    textfile.close()
                os.chdir(self.data.root)
                self.lopetusbutton.SetLabel("Aloita\nkairaus")
                self.lopetusbutton.Disable()
            else:
                return None
        else:
            self.data.kks.aloitaOdotustila()
            self.lopetusbutton.SetLabel("Lopeta\nkairaus")
            self.data.kks.asetaKairaussyvyys(self.data.alkusyvyys)
            self.data.kks.aloitaKairaus()
            self.graphbutton.Enable()
            #print("kuunnellaan kks")

    def kommenttirivi(self, event):

        printtilista = []
        parsilista = []
        headerit = ["FO","KJ","OM","ML","ORG","TY","PK","LA","TT","TX","XY","LN"]
        os.chdir(self.data.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hankenimiteksti.GetLabel()), "r")
        tiedosto = file.readlines()
        file.close()

        #parsitaan pistedata valitusta pisteestä
        pistevalinta = self.pistenimiteksti.GetLabel()
        pistedata = self.data.iparsipiste(pistevalinta)

        #parsitaan headertiedot pois pistedatasta
        for header in headerit:
            for rivi in pistedata:
                if rivi.__contains__(header):
                    pistedata.remove(rivi)

        for s in pistedata:
            if s.__contains__("AL"):
                alku = s.rsplit(None, 4)
                parsilista.append(alku[1])
            else:
                parsilista.append(s.rsplit(None, 3))

        for i in parsilista:
            if i == []:
                printtilista.append("tyhjä rivi")
            elif len(printtilista) < len(parsilista):
                printtilista.append(i[0])

        valinta = wx.SingleChoiceDialog(None, "Valitse kohta", "Kirjoita huomautus",
                                              printtilista, wx.CHOICEDLG_STYLE)


        if valinta.ShowModal() == wx.ID_OK:
            valinta = valinta.GetStringSelection()
            for elem in printtilista:
                if elem.__contains__(valinta):
                    rivimatch = elem
                    break

            for p in printtilista:
                if p == (rivimatch):
                    indeksi = printtilista.index(p)
        else:
            return None

        huomautus = wx.TextEntryDialog(None, "Kirjoita huomautus",
                                           "Kohtaan {}".format(valinta))
        if huomautus.ShowModal() == wx.ID_OK:
            huomautus = huomautus.GetValue()
            for a in tiedosto:
                if a.__contains__(pistevalinta):
                    syvyyshead = tiedosto.index(a)+7 + indeksi
                    tiedosto.insert(syvyyshead + 1, "HM {}\n\n".format(huomautus))

                    os.remove(os.path.join(self.data.config["DEFAULT"]["polku"],
                                           self.hankenimiteksti.GetLabel()+".txt"))
                    luotavahanke = self.hankenimiteksti.GetLabel()
                    os.chdir(self.data.config["DEFAULT"]["polku"])
                    file = open(luotavahanke+".txt", "w")
                    for i in tiedosto:
                        file.write(i)
                    file.close()
                    self.data.iparsipiste(self.pistenimiteksti.GetLabel())
                    break

        else:
            print("Kommenttia ei kirjoitettu")
            return None

    def tanko(self, event):
        self.data.kks.kuittaaTanko()
        return None

    def update(self, event):
        self.updatepistearvot(self.data)
        self.data.ikuuntele(event)

    def linepanelille(self, line):
        self.scrolled_panel.ScrollLines(10)
        self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()
        new_text = wx.StaticText(self.scrolled_panel, -1, line, size=(550, 30))
        font = new_text.GetFont()
        font.SetPointSize(15)
        new_text.SetFont(font)
        self.spSizer.Add(new_text)
        self.scrolled_panel.ScrollLines(10)
        self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()

    # päivittää tekstipaneelin yläpuolella olevat arvotekstit com-listenerin tietojen mukaan
    def updatepistearvot(self, data):
        if self.data.tutkimustapa == "PA":
            self.voimaarvoteksti.SetLabelText(str(data.voima))
            self.puolikierroksetarvoteksti.SetLabelText(str(data.puolikierrokset))
            self.nopeusarvoteksti.SetLabelText(str(data.nopeus))
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))
        elif self.data.tutkimustapa == "HE":
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))
            self.voimaarvoteksti.SetLabelText(str(data.voima))
        elif self.data.tutkimustapa == "PO":
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))
            self.voimaarvoteksti.SetLabelText(str(data.voima))
        elif self.data.tutkimustapa == "TR":
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))
        elif self.data.tutkimustapa == "PH":
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))
            self.voimaarvoteksti.SetLabelText(str(data.voima))
            self.puolikierroksetarvoteksti.SetLabelText(str(data.puolikierrokset))

    # kirjoittaa tekstipaneelille uuden elementin data-luokan tiedoista
    def listenerupdate(self, data):
        self.scrolled_panel.ScrollLines(10)
        self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()
        line = "syvyys: {} voima: {} puolikierrokset: {} nopeus: {}".format(data.haesyvyys(),
                                                                            data.haevoima(),
                                                                            data.haepuolikierrokset(),
                                                                            data.haenopeus())
        new_text = wx.StaticText(self.scrolled_panel, -1, line, size=(550, 30))
        font = new_text.GetFont()
        font.SetPointSize(15)
        new_text.SetFont(font)
        self.spSizer.Add(new_text)
        self.scrolled_panel.ScrollLines(10)
        self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()

    # alustaa arvotekstit ja rullaa tekstipaneelin tyhjäksi
    def komennakks(self, event):
        komento = wx.TextEntryDialog(None, "KKS Komento", "Kirjoita komento")
        if komento.ShowModal() == wx.ID_OK:
            komento = str(komento.GetValue())
            print(komento)
            self.data.kks.annaKasky(komento)
        else:
            return None

    def graafinpiirto(self, event):

        os.chdir(self.data.config["DEFAULT"]["polku"])
        pisteet = []
        file = open("{}.txt".format(self.data.hanke), "r")
        tiedosto = file.readlines()
        file.close()
        os.chdir(self.data.root)
        for i in tiedosto:
            if i.__contains__("TY "):
                pisteet.append(i.strip("TY "))
        pisteet.reverse()
        if self.graphbutton.GetLabelText() =="Piirto":
            self.graphbutton.SetLabelText("Tekla")
            for i in range(20):
                line = ""
                new_text = wx.StaticText(self.scrolled_panel, -1, line, size=(550, 30))
                self.spSizer.Add(new_text)
                self.scrolled_panel.ScrollLines(10)
                self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
                self.scrolled_panel.Layout()
                self.scrolled_panel.Refresh()

            # luodaan piirto-olio ja passataan meidän scrollipaneli sille
            piirratama = pisteet[0].strip()
            if self.data.piste.strip() == piirratama:
                self.piirto = CanvasPanel(self.scrolled_panel)
                self.piirto.setValues(self.data.hanke, self.data.piste)
                self.piirto.draw()
            else:
                pistedata = self.data.iparsipistemittaukset(self.data.piste)
                if pistedata[::-1][0][0] == "-1":
                    del pistedata[-1]
                self.piirto = CanvasPanel(self.scrolled_panel)
                self.piirto.setOldValues(pistedata, self.data.tutkimustapa)
                self.piirto.draw()

        elif self.graphbutton.GetLabelText() == "Tekla":
            self.graphbutton.SetLabelText("Piirto")
            self.data.iparsipiste(self.pistenimiteksti.GetLabel().strip())
        else:
            return None

    def valitseohjelma(self, event):
        if self.hankenimiteksti.GetLabel() == "":
            varoitus = wx.MessageDialog(None, "Valitse ensin hanke ja piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            varoitus.ShowModal()
            varoitus.Destroy()
        else:
            try:
                ohjelma = self.data.ivalitseohjelma()
                self.ohjelmaarvoteksti.SetLabelText(ohjelma)
                self.alustaarvopaneeli(ohjelma)
            except TypeError:
                print("Tutkimustapaa ei valittu")


    def hallintamenu(self, event):
        self.data.ihallinta()

    # käyttäjä valitsee listalta maalajin, joka tallennetaan data-luokkaan ja teklaan oikealle syvyydelle
    def valitsemaalaji(self, event):
        self.data.iluemaalajit()
        tagi = self.data.haemaalaji()
        if tagi == "":
            os.chdir(self.data.root)
            return None
        if tagi == "Lieju":
            self.maalajiarvoteksti.SetLabelText("Lj")
            self.data.maalaji = "Lj"
        elif tagi == "EI PIIRRET":
            self.maalajiarvoteksti.SetLabelText("Ei")
            self.data.maalaji = "Ei"

        else:
            if tagi == "turve":
                 tagi = tagi.upper()
            if tagi == "multa":
                tagi = tagi.upper()
            if tagi == "humusmaa":
                tagi = tagi.upper()

            with open("maalajit.txt", "r", encoding="utf-8") as maatextfile:
                for line in maatextfile:
                    if len(line) > 1:
                        lineparts = line.replace("\n", "").strip("\t")
                        if lineparts.__contains__("{}".format(tagi)):
                            lyhenne = lineparts.rsplit(' ')[0].replace(',', "")
                            self.maalajiarvoteksti.SetLabelText(lyhenne)
                            self.data.maalaji = lyhenne
            maatextfile.close()

    def suljelistener(self, event):
            self.timer.Stop()
            self.timer = None
            event.Skip()
            self.onClose()

#tietojenkäsittely luokka
#tallentaa käyttäjän ja communicationin syöttämän datan ja syöttää sen eteenpäin windowclass luokalle
#ja tallennettaviin tietoihin
class TiedonKasittely(object):
    def __init__(self, hanke = None, piste=None, maalaji="", tutkimustapa="", alkusyvyys=0, syvyys=0, voima=0,
                 puolikierrokset=0, nopeus=0, figure=None, gui=None):
        super(TiedonKasittely, self).__init__()

        #ROOT_DIR = os.path.dirname("C:\\tmp\\GEOXX")

        #self.polku = os.path.dirname(os.path.abspath(__file__))
        self._config = configparser.ConfigParser()
        self._config.read("USECONTROL.ini", encoding='UTF-8')
        self.tallennus_polku = self._config["DEFAULT"]["polku"]
        if not os.path.exists(self.tallennus_polku):
            os.mkdir(self.tallennus_polku)

        self.hanke = hanke
        self.piste = piste
        self.maalaji = maalaji
        self.alkusyvyys = alkusyvyys
        self.syvyys = syvyys
        self.voima = voima
        self.puolikierrokset = puolikierrokset
        self.nopeus = nopeus
        self.figure = figure
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.config = configparser.ConfigParser()
        self.tutkimustapa = tutkimustapa


        self.oldline = ""

        self.com = Communication()

        self.comcheck = self.com.openConnection()
        if not self.comcheck:
            warning = wx.MessageDialog(None, "TARKASTA COM-PORTTI", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
            sys.exit(0)
        
        self.kks = Kksoperations(self.com)


        self.sa = Saving()
        self.gui = gui

    def palautatutkimustapa(self):
        return self.tutkimustapa

    def asetaalkusyvyys(self, alkusyvyys):
        self.alkusyvyys = alkusyvyys
    def asetasyvyys(self, syvyys):
        self.syvyys = syvyys
    def asetavoima(self, voima):
        self.voima = voima
    def asetapuolikierrokset(self, pkierr):
        self.puolikierrokset = pkierr
    def asetanopeus(self, nopeus):
        self.nopeus = nopeus
    def asetamaalaji(self, maalaji):
        self.maalaji = maalaji
    def asetafigure(self, figure):
        self.figure = figure

    def haesyvyys(self):
        kokonaisyvyys = self.alkusyvyys+self.syvyys
        return kokonaisyvyys
    def haevoima(self):
        return self.voima
    def haepuolikierrokset(self):
        return self.puolikierrokset
    def haenopeus(self):
        return self.nopeus
    def haealkusyvyys(self):
        return self.alkusyvyys
    def haemaalaji(self):
        return self.maalaji
    def haefigure(self):
        return self.figure

    def iavaahanke(self):
        self.config.read("USECONTROL.ini")
        os.chdir(self.config["DEFAULT"]["polku"])
        z = [nimi.replace(".txt","") for nimi in os.listdir(os.curdir) if nimi.endswith(".txt")]
        z.append("LUO UUSI HANKE")
        z.remove("MIT_temp")
        tiedostonvalinta = wx.SingleChoiceDialog(None, "Valitse hanke", "Hankkeet", z, wx.CHOICEDLG_STYLE)
        if tiedostonvalinta.ShowModal() == wx.ID_OK:
            if tiedostonvalinta.GetStringSelection() == "LUO UUSI HANKE":
                self.iluohanke()
                os.chdir(self.root)
                return None
            else:
                pisteet = []
                self.hanke = tiedostonvalinta.GetStringSelection()
                self.gui.hankenimiteksti.SetLabelText(self.hanke)
                os.chdir(self.config["DEFAULT"]["polku"])
                file = open("{}.txt".format(self.hanke), "r")
                tiedosto = file.readlines()
                file.close()
                if len(tiedosto) == 5:
                    tiedostonvalinta.Destroy()
                    self.gui.pistenimiteksti.SetLabelText("Ei pisteitä")
                    self.gui.lopetusbutton.Disable()
                    os.chdir(self.root)
                    return None
                else:
                    for i in tiedosto:
                        if i.__contains__("TY "):
                            pisteet.append(i)
                    pisteet.reverse()
                    self.iparsiuusinpiste(pisteet[0].replace("TY ", ""))
                    tiedostonvalinta.Destroy()
                    os.chdir(self.root)
        else:
            os.chdir(self.root)
            return None

    # luodaan hanke käyttäjän antamalla nimellä
    # erikoismerkit parsittu pois
    # estetään ylikirjoitus try-exceptillä
    def iluohanke(self):
        hankenimi = wx.TextEntryDialog(None, "Anna uudelle hankkeelle nimi", "Uuden hankkeen luonti")
        if hankenimi.ShowModal() == wx.ID_OK:
            hankenimi = hankenimi.GetValue()
            hankenimi = ''.join(e for e in hankenimi if e.isalnum())
            varmistus = wx.MessageDialog(None, "Luodaan hanke {}".format(hankenimi), "Luodaan..", wx.YES_NO)
            luo = varmistus.ShowModal()
            if luo == wx.ID_YES:
                z = [hanke.replace(".txt", "") for hanke in os.listdir(os.curdir)]
                if z.__contains__(hankenimi):
                    warning = wx.MessageDialog(None, "Hanke {} on jo olemassa".format(hankenimi), "Varoitus",
                                               wx.OK | wx.ICON_INFORMATION)
                    warning.ShowModal()
                    warning.Destroy()
                    os.chdir(self.root)
                else:
                    self.iluotempconfig()
                    file = open("{}.txt".format(hankenimi), 'a')
                    self.hanke = hankenimi
                    self.config.read("HANKETIEDOT.ini")
                    file.write("FO " + self.config["DEFAULT"]["fo"])
                    file.write("\nKJ "+self.config["DEFAULT"]["kj"])
                    file.write("\nOM "+self.config["DEFAULT"]["om"])
                    file.write("\nML "+self.config["DEFAULT"]["ml"])
                    file.write("\nORG "+self.config["DEFAULT"]["org"])
                    file.close()
                    self.gui.hankenimiteksti.SetLabelText(hankenimi)
                    self.ituhoatempconfig()
                    os.chdir(self.root)
            else:
                os.chdir(self.root)
                return None
        else:
            os.chdir(self.root)
            hankenimi.Destroy()
            return None

    def iavaapiste(self):
        pisteet = []
        piste = []
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hanke), "r")
        tiedosto = file.readlines()
        file.close()
        for i in tiedosto:
            if i.__contains__("TY "):
                pisteet.append(i.replace("TY ", ""))
        pisteet.append("LUO UUSI PISTE")
        valinta = wx.SingleChoiceDialog(None, "Valitse piste", "Pisteet",
                                        pisteet, wx.CHOICEDLG_STYLE)
        pisteet.remove("LUO UUSI PISTE")
        pisteet.reverse()
        if valinta.ShowModal() == wx.ID_OK:
            pistevalinta = valinta.GetStringSelection()
            if valinta.GetStringSelection() == "LUO UUSI PISTE":
                self.iluopiste(self.hanke)
                os.chdir(self.root)
                return None
            elif valinta.GetStringSelection() == pisteet[0]:
                self.piste = valinta.GetStringSelection().strip()
                self.iparsiuusinpiste(valinta.GetStringSelection())
                os.chdir(self.root)
                return None
            else:
                self.piste = valinta.GetStringSelection().strip()
                self.iparsipiste(valinta.GetStringSelection())
                os.chdir(self.root)
                return None
        else:
            valinta.Destroy()
            print("Pistettä ei avattu")
            os.chdir(self.root)

    def iparsipiste(self, pistenimi):
        pistedata = []
        alku = 0
        pisteet = []
        self.config.read("USECONTROL.ini")
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hanke), "r")
        tiedosto = file.readlines()
        file.close()
        for line in tiedosto:
            if line.__contains__("FO"):
                pistedata.append(line)
            if line.__contains__("KJ"):
                pistedata.append(line)
            if line.__contains__("OM"):
                pistedata.append(line)
            if line.__contains__("ML"):
                pistedata.append(line)
            if line.__contains__("ORG"):
                pistedata.append(line)
            if alku == 0:
                if line.__contains__("TY {}".format(pistenimi)):
                    pistedata.append(line)
                    pisteet.append(line)
                    alku = tiedosto.index(line) + 1
                    while alku < len(tiedosto):
                        linepartindex = tiedosto[alku]
                        if linepartindex.__contains__("TT "):
                            self.tutkimustapa = linepartindex.replace("TT ","").strip()
                            self.gui.ohjelmaarvoteksti.SetLabelText(self.tutkimustapa)
                        if linepartindex[0:2] == "TY":
                            break
                        else:
                            pistedata.append(linepartindex)
                            alku = alku + 1
        else:

            data = self.iparsipistesyvyydet(pistenimi)

            if data:
                self.gui.maalajibutton.Enable()
                self.gui.graphbutton.Enable()
            self.gui.linepanelille("")
            for i in pistedata:
                self.gui.linepanelille(i)
            self.gui.pistenimiteksti.SetLabelText(pistenimi.strip())
            os.chdir(self.root)
            return pistedata


    def iparsiuusinpiste(self, pistenimi):
        pistedata = []
        alku = 0
        pisteet = []
        self.config.read("USECONTROL.ini")
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hanke), "r")
        tiedosto = file.readlines()
        file.close()
        for line in tiedosto:
            if line.__contains__("FO"):
                pistedata.append(line)
            if line.__contains__("KJ"):
                pistedata.append(line)
            if line.__contains__("OM"):
                pistedata.append(line)
            if line.__contains__("ML"):
                pistedata.append(line)
            if line.__contains__("ORG"):
                pistedata.append(line)
            if alku == 0:
                if line.__contains__("TY {}".format(pistenimi)):
                    pistedata.append(line)
                    pisteet.append(line)
                    alku = tiedosto.index(line) + 1
                    while alku < len(tiedosto):
                        linepartindex = tiedosto[alku]
                        if linepartindex.__contains__("TT "):
                            self.tutkimustapa = linepartindex.replace("TT ", "").strip()
                            self.gui.ohjelmaarvoteksti.SetLabelText(self.tutkimustapa)
                            self.gui.alustaarvopaneeli(self.tutkimustapa)
                        if linepartindex[0:2] == "TY":
                            break
                        else:
                            pistedata.append(linepartindex)
                            alku = alku + 1

            else:
                pisteet.reverse()
                if pistenimi == pisteet[0]:
                    self.gui.alkukairausbutton.Enable()
                self.piste = pistenimi
                self.gui.linepanelille("")
                for i in pistedata:
                    self.gui.linepanelille(i)
                self.gui.pistenimiteksti.SetLabelText(pistenimi.strip())
                syvyysdata = self.iparsipistesyvyydet(pistenimi)

                if syvyysdata:
                    self.gui.lopetusbutton.Enable()
                    self.gui.graphbutton.Enable()
                    self.gui.huombutton.Enable()
                    self.gui.pistebutton.Enable()
                    self.gui.maalajibutton.Enable()
                    syvyysdata.reverse()
                    jatkasyvyys = syvyysdata[0]
                    self.gui.syvyysarvoteksti.SetLabelText(jatkasyvyys)
                    self.gui.maalajibutton.Enable()
                    self.kks.asetaKairaussyvyys(self.syvyys)
                    self.gui.graphbutton.SetLabelText("Piirto")
                    os.chdir(self.root)
                    return None

                else:
                    self.gui.alkukairausbutton.Enable()
                    os.chdir(self.root)
                    return None


    #listataan pisteen syvyysmittaukset
    def iparsipistesyvyydet(self, pistenimi):
        piste = []
        pistevalinta = pistenimi
        syvyyslista = []
        printtilista = []
        parsilista = []
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hanke), "r")
        tiedosto = file.readlines()
        file.close()

        for line in tiedosto:
            if line.__contains__(pistevalinta):
                piste.append(line)
                alku = tiedosto.index(line) + 1
                while alku < len(tiedosto):
                    linepartindex = tiedosto[alku]
                    if linepartindex[0:2] == ("TY"):
                        break

                    else:
                        piste.append(linepartindex)
                        alku = alku + 1

        for rivi in piste[::-1]:
            if rivi.__contains__("HM"):
                continue
            elif rivi == "\n":
                continue
            elif rivi.__contains__("LN"):
                break
            else:
                syvyyslista.append(rivi)

        syvyyslista.reverse()

        for s in syvyyslista:
            if s == "\n":
                syvyyslista.remove(s)
            elif s.__contains__("AL"):
                alku = s.rsplit(None, 4)
                parsilista.append(alku[1])
            else:
                parsilista.append(s.rsplit(None, 3))

        for i in parsilista:
            if len(printtilista) < len(syvyyslista):
                printtilista.append(i[0])

        if printtilista == []:
            os.chdir(self.root)
            return None

        else:
            self.gui.graphbutton.Enable()
            self.gui.huombutton.Enable()
            os.chdir(self.root)
            return printtilista

    #tämä parsii mit-datan piirtoa varten teklasta
    def iparsipistemittaukset(self, pistenimi):
        piste = []
        pistevalinta = pistenimi
        syvyyslista = []
        printtilista = []
        parsilista = []
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hanke), "r")
        tiedosto = file.readlines()
        file.close()

        for line in tiedosto:
            if line.__contains__(pistevalinta):
                piste.append(line)
                alku = tiedosto.index(line) + 1
                while alku < len(tiedosto):
                    linepartindex = tiedosto[alku]
                    if linepartindex[0:2] == ("TY"):
                        break
                    else:
                        piste.append(linepartindex)
                        alku = alku + 1

        for rivi in piste[::-1]:
            if rivi.__contains__("HM"):
                continue
            elif rivi == "\n":
                continue
            elif rivi.__contains__("LN"):
                break
            else:
                syvyyslista.append(rivi)

        syvyyslista.reverse()

        for s in syvyyslista:
            if s == "\n":
                syvyyslista.remove(s)
            elif s.__contains__("AL"):
                alku = s.rsplit(None, 4)
                parsilista.append(alku[1:4])
            else:
                parsilista.append(s.rsplit(None, 3))

        for i in parsilista:
            if len(printtilista) < len(syvyyslista):
                printtilista.append(i[0])

            return parsilista

    # luodaan piste käyttäjän antamalla nimellä
    def iluopiste(self, hanke):
        pistenimi = wx.TextEntryDialog(None, "Pisteen nimi",
                                       "Uuden pisteen luonti hankkeelle {}".format(hanke))

        if pistenimi.ShowModal() == wx.ID_OK:
            nimi = pistenimi.GetValue()
            pistenimi.Destroy()
            file = open("{}.txt".format(self.hanke), "r")
            tiedosto = file.readlines()
            file.close()
            for i in tiedosto:
                    if i.__contains__("TY {}".format(nimi)):
                        warning = wx.MessageDialog(None, "Piste {} on jo olemassa hankkeella {}".format(nimi, hanke)
                                       , "Varoitus",
                                       wx.OK | wx.ICON_INFORMATION)
                        warning.ShowModal()
                        warning.Destroy()
                        os.chdir(self.root)
                        return None
            os.chdir(self.root)
            varmistus = wx.MessageDialog(None, "Luodaan piste {} hankkeelle {}".format(nimi, hanke)
                                         , "Luodaan..", wx.YES_NO)
            luo = varmistus.ShowModal()
            if luo == wx.ID_YES:
                xkoordinaatti = wx.TextEntryDialog(None, "Anna N koordinaatti", "Pisteen koordinaatit X")
                if xkoordinaatti.ShowModal() == wx.ID_OK:
                    xkoord = xkoordinaatti.GetValue()
                    xkoordinaatti.Destroy()
                else:
                    print("Pistettä ei luotu")
                    return None
                ykoordinaatti = wx.TextEntryDialog(None, "Anna E koordinaatti", "Pisteen koordinaatit Y")
                if ykoordinaatti.ShowModal() == wx.ID_OK:
                    ykoord = ykoordinaatti.GetValue()
                    ykoordinaatti.Destroy()
                else:
                    print("Pistettä ei luotu")
                    return None

                tutkimustapa = self.ivalitseohjelma()
                self.tutkimustapa = tutkimustapa
                self.gui.alustaarvopaneeli(tutkimustapa)
                self.gui.ohjelmaarvoteksti.SetLabelText(tutkimustapa)
                self.piste = nimi
                self.iluotempconfig()
                file = open("{}.txt".format(hanke), "a", encoding="utf-8")
                self.config.read("PISTETIEDOT.ini")
                file.write("\n" + "TY {}".format(nimi))
                file.write("\nPK " + self.config["DEFAULT"]["PK"])
                file.write("\nLA " + self.config["DEFAULT"]["LA"])
                self.config.read("TUTKIMUSTIEDOT.ini")
                file.write("\nTT " + tutkimustapa)
                file.write("\nTX " + self.config["DEFAULT"]["TY"])
                file.write("\nXY " + "{} {}".format(xkoord, ykoord))
                file.write("\nLN " + self.config["DEFAULT"]["LN"] + "\n")
                file.close()
                self.ituhoatempconfig()
                self.syvyys = 0
                self.alkusyvyys = 0
                self.iparsiuusinpiste(self.piste)
                os.chdir(self.root)
            else:
                os.chdir(self.root)
                return None
        else:
            pistenimi.Destroy()
            print("työtä ei luotu")
            os.chdir(self.root)

    # valitaan ohjelma ohjelma-napista
    # tiedot luetaan tutkimustavat-tiedostosta
    def ivalitseohjelma(self):
        os.chdir(self.root)
        z = []
        vanhaohjelma = self.tutkimustapa
        with open("tutkimustavat.txt", "r", encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    z.append(line.rsplit(" ")[1])
        textfile.close()
        ohjelmavalinta = wx.SingleChoiceDialog(None, "Valitse ohjelma", "Ohjelmat", z, wx.CHOICEDLG_STYLE)

        if ohjelmavalinta.ShowModal() == wx.ID_OK:
            ohjelmavalinta = ohjelmavalinta.GetStringSelection()

            self.config.read("USECONTROL.ini")
            os.chdir(self.config["DEFAULT"]["polku"])
            #tähänkö uusi tutkimusheader?
            '''
            self.gui.linepanelille("{} vaihtui {} syvyydellä {}"
                               .format(self.tutkimustapa, ohjelmavalinta, self.syvyys))
            with open("{}.txt".format(self.hanke), 'a') as textfile:
                textfile.write("{} vaihtui {} syvyydellä {}"
                               .format(self.tutkimustapa, ohjelmavalinta, self.syvyys))
                textfile.close()
            '''
            os.chdir(self.root)
            with open("tutkimustavat.txt", "r", encoding="utf-8-sig") as textfile:
                for line in textfile:
                    if line.__contains__(ohjelmavalinta):
                        self.tutkimustapa = line[:2]
                        return line[:2]
        else:
            return None

    # valitaan luokalle maalaji listalta
    # maalajit kakkosikkunaan valitaan tekstitiedostosta ensimmäisen ikkunan
    # valinnan kolmen ensimmäisen kirjaimen mukaan.
    def ivalitsemaalaji(self, lista):


        maalaji = wx.SingleChoiceDialog(None, "Valitse maalaji", "Maalaji", lista,
                                           wx.CHOICEDLG_STYLE)
        if maalaji.ShowModal() == wx.ID_CANCEL:
            print("maalajia ei valittu")
            maalaji.Destroy()
            return None
        else:
            maalaji = maalaji.GetStringSelection()
            if maalaji == "Liejut":
                self.asetamaalaji("Lieju")
                return maalaji
            elif maalaji == "Turpeet":
                turvelaji = wx.SingleChoiceDialog(None, "Valitse turvelaji", "Turpeet", ['turve', 'multa', 'humusmaa'])
                if turvelaji.ShowModal() == wx.ID_OK:
                    turvelaji = turvelaji.GetStringSelection()
                    self.asetamaalaji(turvelaji)
                    return None
                else:
                    print("Maalajia ei valittu")
                    return None
            elif maalaji == "Muut ":
                maalaji = wx.SingleChoiceDialog(None, "Valitse maalaji", "Muut maat", ['TÄYTEMAA', 'KIVI', 'LOHKARE',
                                                                                       'LAPIPOR.LOHK', 'KALLIO', 'VESI',
                                                                                       'TUNTEMATON', 'EI PIIRRET'])
                if maalaji.ShowModal() == wx.ID_OK:
                    maalaji = maalaji.GetStringSelection()
                    self.asetamaalaji(maalaji)
                    return None
                else:
                    print("Maalajia ei valittu")
                    return None
            else:
                templista = []
                maalista = []
                printtilista = []
                indeksi = 0
                parseri_maski = maalaji[:3]
                file = open("maalajit.txt", "r", encoding="utf-8")
                tiedosto = file.readlines()
                file.close()
                for rivi in tiedosto:
                    if rivi.__contains__(maalaji):
                        indeksi = tiedosto.index(rivi)
                        while tiedosto[indeksi]:
                            if tiedosto[indeksi].startswith('\n'):
                                break

                            else:
                                templista.append(tiedosto[indeksi].rsplit("\t", 3))
                                indeksi = indeksi + 1


            for temp in templista:
                    maalista.append(temp[0])

            for maa in maalista:
                parsittu = re.sub(r'^[^" "]*', '', maa)
                printtilista.append(parsittu)


            maatyyppi = wx.SingleChoiceDialog(None, "Valitse maatyyppi", "{}".format(maalaji),
                                              printtilista, wx.CHOICEDLG_STYLE)

            if maatyyppi.ShowModal() == wx.ID_OK:
                maatyyppi = maatyyppi.GetStringSelection()
                for line in tiedosto:
                    if line.__contains__(maatyyppi):
                        self.asetamaalaji(maatyyppi)
                return None

            else:
                print("Maalajia ei valittu")
                maatyyppi.Destroy()
                return None


    # luetaan tiedot tekstitiedostosta, mockup communication listenistä
    def ikuuntele(self, event):
        z = []
        #with open("data0.txt", 'r', encoding="utf-8") as textfile:
        self.config.read("USECONTROL.ini")
        self.polku = self.config["DEFAULT"]["polku"]
        self.tiedosto = "MIT_temp.txt"
        self.fullpath = os.path.join(self.polku, self.tiedosto)
        with open(self.fullpath, 'r', encoding="utf-8") as textfile:
#           for line in textfile:
            line = textfile.read()
            if len(line) > 1:
                lineparts = line.replace('\n', '').split('\t')

                if lineparts != self.oldline:
                    print("--> ", lineparts)

                    #MITTAUS- JA TALLENNUSSANOMAT KKS:LTA
                    if lineparts[0][:4] == "#MIT":
                        if lineparts[0][:11] == "#MIT_ODOTUS":
                            print("MIT ODOTELLAAN")
                        else:
                            #print("MITTIA PUKKAA")
                            self.iparsitiedot(lineparts)

                    if lineparts[0][:4] == "#TAL":
                        #parsitaan vain arvot TEKLAAN vietavaksi
                        linearvot = lineparts[0].rpartition(":")[2]

                        #kutsutaan saving luokan metodia joka tallettaa sanoman tekla-tiedostoon
                        self.sa.tallennaTAL(self.hanke, linearvot, self.maalaji)
                        self.maalaji = ""

                        self.arvot = linearvot.split()
                        self.apu = '{0:.2f}'.format(float(self.arvot[0]) / 100.00)
                        self.arvot[0] = str(self.apu)
                        self.TAL = "\t" + "\t" .join(self.arvot)

                        #paivitetaan arvot piirtajalle. PITAISI OLLA LUOTU;PAINETTU NAPPIA PIIRTO KOSKA LUODAAN VASTA SILLOIN
                        if self.gui.graphbutton.GetLabelText() == "Tekla":
                            self.gui.piirto.setValues(self.hanke, self.piste)
                            self.gui.piirto.draw()
                        else:
                            #paivitetaan paneeli
                            # paivitetaan arvot scrollipanelille.
                            self.gui.linepanelille(self.TAL)
                            self.gui.scrolled_panel.Refresh()


                    if lineparts[0][:4] == "#END":
                        print("ENDI")
                        #self.iparsitiedot(lineparts)
                        #TEHDÄÄN MITAMITA??
                        #EI TULE TALLAISTA SANOMAA DEMOLLA,
                        self.sa.tallennaTAL(self.hanke, lineparts[0])

                    if lineparts[0][:4] == "#SYV":
                        #self.iparsitiedot(lineparts)
                        print("SYVI")
                        #TEHDAAN MITAMITA
                        #Alkukairaussyvyys 1s välein. < - - - - - - #SYV:nnn


                    #OHJAUSTIEDOT KKS:LTA
                    if lineparts[0] == "#ALKUKAIRAUS":
                        print("alkuk")

                    if lineparts[0] == "MIT-ODOTUS":
                        print("MIT-ODOTUS")

                    if lineparts[0] == "#NOSTO":
                        print("nosto")
                        self.gui.vaihdatankovari('red')

                    if lineparts[0] == "#NOSKU":
                        print("NOSTON KUITTAUS")
                        #self.gui.vaihdatankovari

                    if lineparts[0] == "#KAIRAUS":
                        print("KAIRAUS")
                        self.gui.vaihdatankovari('green')


                    if lineparts[0] == "#ALKUTILA":
                        print("ALKUTILA")
                        self.gui.vaihdatankovari('red')

                    if lineparts[0] =="#STOP":
                        print("STOPPI")
                        self.gui.vaihdatankovari('red')
                        self.gui.lopetusbutton.SetLabel("Aloita\nkairaus")

                    if lineparts[0] == "#MIT_ODOTUS":
                        self.gui.vaihdatankovari('red')
                        self.gui.lopetusbutton.SetLabel("Aloita\nkairaus")

                    #NAPIT KKS:LTA MITÄ IKINÄ TULEEKAAN --> TÄHÄN
                    if lineparts[0] == "#JOKUKOMENTO":
                        print("JOKUKOMENTO")
                        #DO JOTAKI

                    self.oldline = lineparts

    def iparsiheader(self):
        headlista = []
        with open("data0.txt", 'r', encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    lineparts = line.replace('\n', '')
                    if not lineparts.startswith("#"):
                        headlista.append(lineparts)
            return headlista

    def iluemaalajit(self):
        os.chdir(self.root)
        lajit = []
        temp_list = []
        with open("maalajit.txt", "r", encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    lineparts = line.replace('\n', '').split('\t')
                    for line in lineparts:
                        if line.__contains__(":"):
                            temp_list.append(line)
            for alkio in temp_list:
                parsittu = re.sub('[^a-zA-Z0-9 \n\.]', '', alkio)
                lajit.append(parsittu)
        textfile.close()
        self.ivalitsemaalaji(lajit)
        return None

    # parsitaan data merkittävään muotoon
    # parsitaan data merkittävään muotoon
    def iparsitiedot(self, line):

        tutkimustapa = self.palautatutkimustapa()
        linearvot = line[0].rpartition(":")[2]
        arvot = linearvot.split()

        if tutkimustapa == "PA":
            syvyys = int(arvot[0])
            # print(syvyys, " syvyys")
            self.asetasyvyys(syvyys)

            voima = int(arvot[1])
            # print(voima, " voima")
            self.asetavoima(voima)

            puolikierrokset = int(arvot[2])
            self.asetapuolikierrokset(puolikierrokset)
            # print(puolikierrokset, " puolik.")

            nopeus = int(arvot[3])
            # print(nopeus, " nopeus")
            self.asetanopeus(nopeus)

        if tutkimustapa == "HE":
            syvyys = int(arvot[0])
            self.asetasyvyys(syvyys)

            voima = int(arvot[1])
            self.asetavoima(voima)

        if tutkimustapa == "TR":
            syvyys = int(arvot[0])
            self.asetasyvyys(syvyys)

        if tutkimustapa == "PO":
            syvyys = int(arvot[0])
            self.asetasyvyys(syvyys)

            voima = int(arvot[1])
            self.asetavoima(voima)

        if tutkimustapa == "PH":
            syvyys = int(arvot[0])
            # print(syvyys, " syvyys")
            self.asetasyvyys(syvyys)

            '''
            voima = int(arvot[1])
            # print(voima, " voima")
            self.asetavoima(voima)

            puolikierrokset = int(arvot[2])
            self.asetapuolikierrokset(puolikierrokset)
            # print(puolikierrokset, " puolik.")

            nopeus = int(arvot[3])
            # print(nopeus, " nopeus")
            self.asetanopeus(nopeus)
            '''

    def ihallinta(self):
        os.chdir(self.root)
        x = [config.replace(".ini", "") for config in os.listdir(os.curdir) if config.endswith(".ini")
             and config != "USECONTROL.ini"]
        valinta = wx.SingleChoiceDialog(None, "Valitse muokattavat tiedot", "Hallinta",
                                        x, wx.CHOICEDLG_STYLE)
        if valinta.ShowModal() == wx.ID_OK:
            muokattava = valinta.GetStringSelection()
            valinta.Destroy()
            if muokattava == "HANKETIEDOT":
                self.ihankeheader()
            if muokattava == "PISTETIEDOT":
                self.ipisteheader()
            if muokattava == "TUTKIMUSTIEDOT":
                self.itutkimusheader()
            if muokattava == "HWCONTROL":
                self.ihwasetus()
        else:
            print("Tietoja ei muutettu")
            return None

    def ihwasetus(self):
        self.config.read("HWCONTROL.ini")
        uusi_logging = wx.TextEntryDialog(None, "logging", "HWCONTROL", self.config["DEFAULT"]["logging"])

        if uusi_logging.ShowModal() == wx.ID_OK:
            uusi_logging = uusi_logging.GetValue()
        else:
            return None

        uusi_puls_cm = wx.TextEntryDialog(None, "puls_cm", "HWCONTROL", self.config["DEFAULT"]["puls_cm"])

        if uusi_puls_cm.ShowModal() == wx.ID_OK:
            uusi_puls_cm = uusi_puls_cm.GetValue()
        else:
            return None

        uusi_puls_pk = wx.TextEntryDialog(None, "puls_pk", "HWCONTROL", self.config["DEFAULT"]["puls_pk"])

        if uusi_puls_pk.ShowModal() == wx.ID_OK:
            uusi_puls_pk = uusi_puls_pk.GetValue()
        else:
            return None

        # lähetetään komennot KKS:lle
        # paitsi logging, komento puuttuu...
        # if uusi_logging != self.config["DEFAULT"]["logging"]:
        # self.kks.

        # TOISTAISEKSI NÄMÄKIN POIS, DEMOLAITE EI VASTAA KOMENTOIHIN
        if uusi_puls_cm != self.config["DEFAULT"]["puls_cm"]:
            self.kks.asetaSyvyydenVakio(uusi_puls_cm)

        if uusi_puls_pk != self.config["DEFAULT"]["puls_pk"]:
            self.kks.asetaPuolikierrostenVakio(uusi_puls_pk)

        # tallennetaan hwcontrol.ini tiedostoon uudet muuttujat
        self.sa.asetaHWcontrol(uusi_logging, uusi_puls_cm, uusi_puls_pk)

    def ihankeheader(self):
        self.config.read("HANKETIEDOT.ini")
        uusifo = wx.TextEntryDialog(None, "FO", "HANKETIEDOT",
                                    self.config["DEFAULT"]["FO"])
        if uusifo.ShowModal() == wx.ID_OK:
            uusifo = uusifo.GetValue()
        else:
            return None

        uusikj = wx.TextEntryDialog(None, "KJ", "HANKETIEDOT",
                                    self.config["DEFAULT"]["KJ"])

        if uusikj.ShowModal() == wx.ID_OK:
            uusikj = uusikj.GetValue()
        else:
            return None

        uusiom = wx.TextEntryDialog(None, "OM", "HANKETIEDOT",
                                    self.config["DEFAULT"]["OM"])

        if uusiom.ShowModal() == wx.ID_OK:
            uusiom = uusiom.GetValue()
        else:
            return None

        uusiml = wx.TextEntryDialog(None, "ML", "HANKETIEDOT",
                                    self.config["DEFAULT"]["ML"])
        if uusiml.ShowModal() == wx.ID_OK:
            uusiml = uusiml.GetValue()
        else:
            return None

        uusiorg = wx.TextEntryDialog(None, "ORG", "HANKETIEDOT",
                                     self.config["DEFAULT"]["ORG"])
        if uusiorg.ShowModal() == wx.ID_OK:
            uusiorg = uusiorg.GetValue()
        else:
            return None

        self.sa.asetaHanketiedot(uusifo, uusikj, uusiml, uusiom, uusiorg)

    def ipisteheader(self):
        self.config.read("PISTETIEDOT.ini")
        uusity = wx.TextEntryDialog(None, "TY", "PISTETIEDOT",
                                    self.config["DEFAULT"]["TY"])
        if uusity.ShowModal() == wx.ID_OK:
            uusity = uusity.GetValue()
        else:
            return None

        uusipk = wx.TextEntryDialog(None, "PK", "PISTETIEDOT",
                                    self.config["DEFAULT"]["PK"])
        if uusipk.ShowModal() == wx.ID_OK:
            uusipk = uusipk.GetValue()
        else:
            return None

        uusila = wx.TextEntryDialog(None, "LA", "PISTETIEDOT",
                                    self.config["DEFAULT"]["LA"])
        if uusila.ShowModal() == wx.ID_OK:
            uusila = uusila.GetValue()
        else:
            return None

        self.sa.asetaPistetiedot(uusity, uusipk, uusila)

    def itutkimusheader(self):
        self.config.read("TUTKIMUSTIEDOT.ini")
        uusitt = wx.TextEntryDialog(None, "TT", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["TT"])
        if uusitt.ShowModal() == wx.ID_OK:
            uusitt = uusitt.GetValue()
        else:
            return None

        uusitx = wx.TextEntryDialog(None, "TX", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["TX"])
        if uusitx.ShowModal() == wx.ID_OK:
            uusitx = uusitx.GetValue()
        else:
            return None

        uusixy = wx.TextEntryDialog(None, "XY", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["XY"])
        if uusixy.ShowModal() == wx.ID_OK:
            uusixy = uusixy.GetValue()
        else:
            return None

        uusiln = wx.TextEntryDialog(None, "LN", "TUTKIMUSTIEDOT",
                                        self.config["DEFAULT"]["LN"])
        if uusiln.ShowModal() == wx.ID_OK:
            uusiln = uusiln.GetValue()
        else:
            return None

        self.sa.asetaTutkimustiedot(uusitt, uusitx, uusixy, uusiln)

    def iluotempconfig(self):
        os.chdir(self.root)
        shutil.copy('HANKETIEDOT.ini', self.config["DEFAULT"]["polku"])
        shutil.copy('PISTETIEDOT.ini', self.config["DEFAULT"]["polku"])
        shutil.copy('TUTKIMUSTIEDOT.ini', self.config["DEFAULT"]["polku"])
        self.config.read("USECONTROL.ini")
        os.chdir(self.config["DEFAULT"]["polku"])
        return None

    def ituhoatempconfig(self):
        os.remove('HANKETIEDOT.ini')
        os.remove('PISTETIEDOT.ini')
        os.remove('TUTKIMUSTIEDOT.ini')

def main():
    app = wx.App()
    frame = windowClass(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()



