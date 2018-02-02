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
import bar_animation as ba
import re
import configparser
import shutil
import saving
from saving import *
from kks_operations import *
from piirto import *

# import communication
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
        self.ba = ba
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



    #NAMA PITAISI SAADA MYOS OIKEAN YLANURKAN PUNAISEESN AXAAN (SULKEMISNAPPI)
    def onClose(self):
        #self.kks.closeConnection()
        self.data.kks.closeConnection()
        #self.Close()
        #self.Destroy()


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
        self.hankebutton = wx.Button(panel, label="Hanke", pos=(5, 10), size=(110, 110))
        self.hankebutton.SetFont(font1)
        self.hankebutton.Bind(wx.EVT_BUTTON, self.hankkeenavaus)

        # piste
        # avaa pisteen hankkeen sisältä
        self.pistebutton = wx.Button(panel, label="Työnro/\nuusi työ", pos=(120, 10), size=(110, 110))
        self.pistebutton.SetFont(font1)
        self.pistebutton.Bind(wx.EVT_BUTTON, self.pisteenavaus)

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

        # hae
        # communications listenerin mockup
        self.huombutton = wx.Button(panel, label="Kirjoita\nhuom", pos=(400, 125), size=(75, 75))
        self.huombutton.SetFont(font1)
        self.huombutton.Bind(wx.EVT_BUTTON, self.kommenttirivi)

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

        # alkukairaus
        # käyttäjä valitsee kairaustyypin ja alkusyvyyden, joka lähetetään kkssälle
        self.alkukairausbutton = wx.Button(panel, label="Alku\nkairaus", pos=(120, 215), size=(100,100))
        self.alkukairausbutton.SetFont(font1)
        self.alkukairausbutton.Bind(wx.EVT_BUTTON, self.aloitaalkukairaus)

        # kairauksen lopetus
        # käyttäjä valitsee lopetussyyn
        # tiedot kkssälle
        self.lopetusbutton = wx.Button(panel, label="Aloita\nkairaus", pos=(400, 215), size=(100,100))
        self.lopetusbutton.SetFont(font1)
        self.lopetusbutton.Bind(wx.EVT_BUTTON, self.lopetakairaus)

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
        self.hankenimiteksti = wx.StaticText(panel, -1, ">hankkeen nimi<", pos=(120, 120))
        self.hankenimiteksti.SetFont(font2)

        self.pisteteksti = wx.StaticText(panel, -1, "Työnro: ", pos=(10, 165))
        self.pisteteksti.SetFont(font2)

        # pistenimiteksti näyttää valitusta hankkeesta valitun pisteen
        self.pistenimiteksti = wx.StaticText(panel, -1, ">työn numero<", pos=(120, 165))
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
        self.syvyysarvoteksti = wx.StaticText(panel, -1, "", pos=(15, 345))
        self.syvyysarvoteksti.SetFont(font2)

        self.voimateksti = wx.StaticText(panel, -1, "Voima", pos=(85, 315))
        self.voimateksti.SetFont(font1)

        # voima-arvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.voimaarvoteksti = wx.StaticText(panel, -1, "", pos=(95, 345))
        self.voimaarvoteksti.SetFont(font2)

        self.puolikierroksetteksti = wx.StaticText(panel, -1, "P-kierr", pos=(165, 315))
        self.puolikierroksetteksti.SetFont(font1)

        # puolikierroksetarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.puolikierroksetarvoteksti = wx.StaticText(panel, -1, "", pos=(170, 345))
        self.puolikierroksetarvoteksti.SetFont(font2)

        self.nopeusteksti = wx.StaticText(panel, -1, "Nopeus", pos=(235, 315))
        self.nopeusteksti.SetFont(font1)

        # nopeusarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.nopeusarvoteksti = wx.StaticText(panel, -1, "", pos=(240, 345))
        self.nopeusarvoteksti.SetFont(font2)

        self.maalajiteksti = wx.StaticText(panel, -1, "Maalaji", pos=(315, 315))
        self.maalajiteksti.SetFont(font1)

        # maalajiarvoteksti päivittyy käyttäjän valitessa maalaji
        self.maalajiarvoteksti = wx.StaticText(panel, -1, "", pos=(320, 345))
        self.maalajiarvoteksti.SetFont(font2)

        self.iskuteksti = wx.StaticText(panel, -1, "Isku", pos=(455, 315))
        self.iskuteksti.SetFont(font1)

        # iskuarvoteksti päivittyy käyttäjän valitessa isku
        self.iskuarvoteksti = wx.StaticText(panel, -1, "OFF", pos=(445, 345))
        self.iskuarvoteksti.SetFont(font2)

        self.tankoteksti = wx.StaticText(panel, -1, "Tanko", pos=(515, 315))
        self.tankoteksti.SetFont(font1)

        #  tankoarvolaatikko vaihtaa väriä tarpeen mukaan
        self.tankoarvolaatikko = wx.Panel(panel, pos=(515, 345), size=(50,50))
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
            self.puolikierroksetteksti.SetLabelText("P-kierr")
            self.puolikierroksetarvoteksti.SetLabelText("0")
            self.syvyysteksti.SetLabelText("Syvyys")
            self.syvyysarvoteksti.SetLabelText("0")
            self.voimateksti.SetLabelText("Voima")
            self.voimaarvoteksti.SetLabelText("0")
            self.nopeusteksti.SetLabelText("Nopeus")
            self.nopeusarvoteksti.SetLabelText("0")
            self.maalajiteksti.SetLabelText("Maalaji")
            self.maalajiarvoteksti.SetLabelText("")

        if kairaustapa == "HE":
            self.voimateksti.SetLabelText("H / I")
            self.voimaarvoteksti.SetLabelText("H")
            self.puolikierroksetteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabel("")
            self.nopeusteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")

        if kairaustapa == "PO":
            self.voimateksti.SetLabelText("Aika")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabelText("")
            self.nopeusteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")

        if kairaustapa == "TR":
            self.voimateksti.SetLabelText("")
            self.voimaarvoteksti.SetLabelText("")
            self.puolikierroksetteksti.SetLabelText("")
            self.puolikierroksetarvoteksti.SetLabelText("")
            self.nopeusteksti.SetLabelText("")
            self.nopeusarvoteksti.SetLabelText("")

        if kairaustapa == "PH":
            self.voimateksti.SetLabelText("Voima")
            self.voimaarvoteksti.SetLabelText("0")
            self.puolikierroksetteksti.SetLabelText("Vääntö")
            self.puolikierroksetarvoteksti.SetLabelText("0")
            self.nopeusteksti.SetLabelText("P / H")
            self.nopeusarvoteksti.SetLabelText("P")


    def hankkeenavaus(self, event):
        if self.hankenimiteksti.GetLabel() != ">hankkeen nimi<":
            self.data.iavaahanke()
            self.hankenimiteksti.SetLabelText(self.data.hanke)
            self.pistenimiteksti.SetLabelText(">pisteen nimi<")
            self.syvyysarvoteksti.SetLabelText("><")
            self.voimaarvoteksti.SetLabelText("><")
            self.puolikierroksetarvoteksti.SetLabelText("><")
            self.nopeusarvoteksti.SetLabelText("><")
        else:
            self.data.iavaahanke()
            self.hankenimiteksti.SetLabelText(self.data.hanke)

    # jos ei luoda uutta pistettä, niin jatketaan vanhasta
    # avataan tekstifile, joka luetaan kunnes viimeinen pistenimi-tunnistin tulee
    # ja tämän perään jatketaan datan kirjoittamista
    def pisteenavaus(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            uusikysymys = wx.MessageDialog(None, "Luodaanko uusi piste hankkeelle {}?".format(self.data.hanke), "Piste",
                                           wx.YES_NO)
            uusivastaus = uusikysymys.ShowModal()
            uusikysymys.Destroy()
            if uusivastaus == wx.ID_YES:
                self.data.iluopiste(self.data.hanke)
                self.pistenimiteksti.SetLabelText(self.data.piste)
                self.pistetiedotpaneelille()
                self.update(event)
                self.timer.Start(50)
                #self.timer2.Start(50)
            else:
                self.pistetiedotpaneelille()
                self.config.read("USECONTROL.ini")
                os.chdir(self.config["DEFAULT"]["polku"])
                pisteet = []
                with open("{}.txt".format(self.hankenimiteksti.GetLabel())) as textfile:
                    for line in textfile:
                        if line.__contains__("ty "):
                            linepart = line.replace("ty = ", "").strip("\n")
                            pisteet.append(linepart)
                    self.pistenimiteksti.SetLabel(pisteet[len(pisteet)-1])
                    self.data.piste = self.pistenimiteksti.GetLabel()
                textfile.close()
                self.timer.Start(50)
                os.chdir(self.data.root)

    # kysyy käyttäjältä alkusyvyyttä, joka tallennetaan
    # windowclassin.data luokkaan


    def aloitaalkukairaus(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        elif self.alkukairausbutton.GetLabelText()=="Lopeta\nalkukair.":
            self.data.kks.aloitaOdotustila()
            self.alkukairausbutton.SetLabelText("Alku\nkairaus")

        else:
            self.data.kks.asetaHanke(self.data.piste, self.data.hanke)
            self.data.kks.asetaPiste(self.data.piste)
            self.data.kks.asetaTapa(self.data.tutkimustapa)
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
                    self.data.kks.aloitaOdotustila()
                    self.config.read("USECONTROL.ini")
                    os.chdir(self.config["DEFAULT"]["polku"])
                    with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                        textfile.write("\n" + "alkukairaus ohitetaan")
                        textfile.close()
                    os.chdir(self.data.root)
                else:
                    with open("alkukairaus.txt", "r") as textfile:
                        for line in textfile:
                            if line.__contains__(kairausvalinta):
                                self.alkukairausarvoteksti.SetLabelText(line[1:3])
                    alkusyvyys = wx.TextEntryDialog(None, 'Aseta alkusyvyys',"Alkusyvyys","",
                                                    style=wx.OK)
                    alkusyvyys.Centre()
                    alkusyvyys.ShowModal()
                    self.alkusyvyysarvoteksti.SetLabelText(alkusyvyys.GetValue())
                    self.data.asetaalkusyvyys(int(alkusyvyys.GetValue()))
                    self.data.kks.asetaAlkusyvyys(alkusyvyys.GetValue())
                    alkusyvyys.Destroy()
                    self.alkukairausbutton.SetLabelText("Lopeta\nalkukair.")
                    self.config.read("USECONTROL.ini")
                    os.chdir(self.config["DEFAULT"]["polku"])
                    with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                        textfile.write("\n" + "alkukairaus: {} syvyydellä {}".format(self.data.syvyys, kairausvalinta))
                        textfile.close()
                    os.chdir(self.data.root)

                    #print("lähetetään kkssälle: työnumero, kairausvalinta, piste, pvm(timestä?)")
                    self.data.kks.aloitaAlkukairaus()

                    self.linepanelille("Alkukairaus {} syvyydellä {}".format(kairausvalinta, alkusyvyys.GetValue()))
                    # print("lähetetään kkssälle: työnumero(hanke?), {}, {}, pvm(timestä?)".format(kairausvalinta)
                    #       , self.data.piste)

    def lopetakairaus(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        elif self.lopetusbutton.GetLabel() == "Lopeta\nkairaus":
            self.data.kks.lopetaKairaus()
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
                print("lähetetään kkssälle tieto kairaus lopetettiin syvyydellä {} syystä {}"
                      .format(self.data.haesyvyys(), kairausvalinta))
                self.config.read("USECONTROL.ini")
                os.chdir(self.config["DEFAULT"]["polku"])
                with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                    textfile.write("\n" + "lopetus: {} syvyydellä {}".format(self.data.syvyys, kairausvalinta))
                    textfile.close()
                os.chdir(self.data.root)
                self.linepanelille("Kairaus lopetettiin {} syvyydellä {}".format(kairausvalinta, self.data.haesyvyys()))
                self.lopetusbutton.SetLabel("Aloita\nkairaus")
            else:
                return None
        else:
            self.lopetusbutton.SetLabel("Lopeta\nkairaus")
            self.data.kks.aloitaKairaus()
            #self.vaihdatankovari()
            print("kuunnellaan kks")

    def kommenttirivi(self, event):
        z = []
        os.chdir(self.config["DEFAULT"]["polku"])
        file = open("{}.txt".format(self.hankenimiteksti.GetLabel()), "a")
        kommentti = wx.TextEntryDialog(None, "Kirjoita huomautus syvyydelle {}".format(self.data.syvyys),
                                               "Kirjoita huomautus")
        if kommentti.ShowModal() == wx.ID_OK:
            kommentti = kommentti.GetValue()
            file.write("\nHM {}".format(kommentti))
            self.linepanelille("HM {}".format(kommentti))
        else:
            file.close()
            return None
            # sa.tallennaHM(self.hankenimiteksti.GetLabel(), kommentti)
        file.close()
            #oikeesti tähän saving luokan meotodi hoitaa def tallennaHM(self, hanke, huomautus)


    def tanko(self, event):
        self.data.kks.kuittaaTanko()

        return None


    def lataapiste(self, event):
        if self.pistenimiteksti.GetLabel() == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        elif self.ohjelmaarvoteksti.GetLabel() == "><":
            warning = wx.MessageDialog(None, "Valitse tutkimustapa", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.data.piste = self.pistenimiteksti.GetLabel()

            self.update()
            self.timer.Start(50)

    def update(self, event):
        #print(self.listener)
        #self.data.ikuuntele()
        self.updatepistearvot(self.data)
        self.data.ikuuntele(event)

        #self.listenerupdate(self.data)

    def pistetiedotpaneelille(self):
        self.config.read("USECONTROL.ini")
        os.chdir(self.config["DEFAULT"]["polku"])
        print(self.hankenimiteksti.GetLabel())
        with open("{}.txt".format(self.hankenimiteksti.GetLabel())) as textfile:
            for line in textfile:
                self.linepanelille(line)
        textfile.close()
        os.chdir(self.data.root)

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
        #print("uppaaa!!!!")
        self.voimaarvoteksti.SetLabelText(str(data.voima))
        self.puolikierroksetarvoteksti.SetLabelText(str(data.puolikierrokset))
        self.nopeusarvoteksti.SetLabelText(str(data.nopeus))
        if self.data.alkusyvyys != 0:
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys+data.alkusyvyys))
        else:
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))

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
        # if ba.fig == None:
        #     graafi.show()
        #ba.main(self.data)
        #print("lululu noob noob")


        #luodaan piirto-olio ja passataan meidän scrollipaneli sille
        self.piirto = CanvasPanel(self.scrolled_panel)
        self.piirto.draw()

    def valitseohjelma(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            varoitus = wx.MessageDialog(None, "Valitse ensin hanke ja piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            varoitus.ShowModal()
            varoitus.Destroy()
        else:
            ohjelma = self.data.ivalitseohjelma()
            self.ohjelmaarvoteksti.SetLabelText(ohjelma)
            self.alustaarvopaneeli(ohjelma)
            self.linepanelille("TT {} syvyydellä {}".format(ohjelma, self.data.haesyvyys()))

            #komento kks:lle kairaustavan valinnasta
            #self.tapa = "TEK-" + ohjelma
            #print(self.tapa)
            #self.data.kks.asetaTapa(self.data.tapa)

    def hallintamenu(self, event):
        '''
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            varoitus = wx.MessageDialog(None, "Valitse ensin hanke ja piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            varoitus.ShowModal()
            varoitus.Destroy()
        elif self.pistenimiteksti.GetLabel() == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
        else:
        '''
        self.data.ihallinta()

    # käyttäjä valitsee listalta maalajin, joka tallennetaan data-luokkaan
    def valitsemaalaji(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.data.iluemaalajit()
            print("tägättiin maalaji {} syvyydelle {}".format(self.data.haemaalaji(), self.data.haesyvyys()))
            tagi = self.data.haemaalaji()
            os.chdir(self.data.root)

            if tagi == "Lieju":
                self.maalajiarvoteksti.SetLabelText("Lj")
                self.config.read("USECONTROL.ini")
                os.chdir(self.config["DEFAULT"]["polku"])
                with open("{}.txt".format(self.data.hanke), 'a') as hanketextfile:
                    hanketextfile.write(
                        "\n" + "{} syvyydellä {}".format(self.maalajiarvoteksti.GetLabel(), self.data.syvyys))
                    os.chdir(self.data.root)
                    hanketextfile.close()
            else:
                if tagi == "turve":
                     tagi = tagi.upper()
                if tagi == "multa":
                    tagi = tagi.upper()
                if tagi == "humusmaa":
                    tagi = tagi.upper()
                print(tagi)
                with open("maalajit.txt", "r", encoding="utf-8") as maatextfile:
                    for line in maatextfile:
                        if len(line) > 1:
                            lineparts = line.replace("\n", "").strip("\t")
                            if lineparts.__contains__("{}".format(tagi)):
                                lyhenne = lineparts.rsplit(' ')[0].replace(',', "")
                                self.maalajiarvoteksti.SetLabelText(lyhenne)
                self.config.read("USECONTROL.ini")
                os.chdir(self.config["DEFAULT"]["polku"])
                with open("{}.txt".format(self.data.hanke), 'a') as hanketextfile:
                    hanketextfile.write("\n" + "{} syvyydellä {}".format(self.maalajiarvoteksti.GetLabel(), self.data.syvyys))
                    os.chdir(self.data.root)
                    maatextfile.close()
                    hanketextfile.close()

    def suljelistener(self, event):
            event.Skip()
            self.onClose()
            #wx.EVT_WINDOW_DESTROY

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

        self.kks = Kksoperations()
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
        tiedostonvalinta = wx.SingleChoiceDialog(None, "Valitse hanke", "Hankkeet", z, wx.CHOICEDLG_STYLE)
        if tiedostonvalinta.ShowModal() == wx.ID_OK:
            if tiedostonvalinta.GetStringSelection() == "LUO UUSI HANKE":
                self.iluohanke()
                os.chdir(self.root)
                return None
            else:
                self.hanke = tiedostonvalinta.GetStringSelection()
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
                    file.write("fo = " + self.config["DEFAULT"]["fo"])
                    file.write("\nkj = "+self.config["DEFAULT"]["kj"])
                    file.write("\nom = "+self.config["DEFAULT"]["om"])
                    file.write("\nml = "+self.config["DEFAULT"]["ml"])
                    file.write("\norg = "+self.config["DEFAULT"]["org"])
                    file.close()
                    #self.ituhoatempconfig()
                    os.chdir(self.root)
            else:
                os.chdir(self.root)
                return None
        else:
            os.chdir(self.root)
            hankenimi.Destroy()
            return None

    # luodaan piste käyttäjän antamalla nimellä
    def iluopiste(self, hanke):
        pistenimi = wx.TextEntryDialog(None, "Anna hankkeen {} uudelle pisteelle nimi".format(hanke),
                                       "Uuden pisteen luonti hankkeelle {}".format(hanke))
        if pistenimi.ShowModal() == wx.ID_OK:
            nimi = pistenimi.GetValue()
            varmistus = wx.MessageDialog(None, "Luodaan piste {} hankkeelle {}".format(nimi, hanke)
                                         , "Luodaan..", wx.YES_NO)
            luo = varmistus.ShowModal()
            if luo == wx.ID_YES:
                self.piste = nimi
                self.iluotempconfig()
                file = open("{}.txt".format(hanke), "a", encoding="utf-8")
                self.config.read("PISTETIEDOT.ini")
                file.write("\n" + "ty = {}".format(nimi))
                file.write("\npk = " + self.config["DEFAULT"]["pk"])
                file.write("\nla = " + self.config["DEFAULT"]["la"])
                self.config.read("TUTKIMUSTIEDOT.ini")
                file.write("\ntt = " + self.config["DEFAULT"]["tt"])
                file.write("\ntx = " + self.config["DEFAULT"]["tx"])
                file.write("\nxy = " + self.config["DEFAULT"]["xy"])
                file.write("\nln = " + self.config["DEFAULT"]["ln"] + "\n")
                file.close()
                self.ituhoatempconfig()
                os.chdir(self.root)
            else:
                os.chdir(self.root)
                return None
        else:
            os.chdir(self.root)
            return None

    # valitaan ohjelma ohjelma-napista
    # tiedot luetaan tutkimustavat-tiedostosta
    def ivalitseohjelma(self):
        os.chdir(self.root)
        z = []
        with open("tutkimustavat.txt", "r", encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    z.append(line.rsplit(" ")[1])
        textfile.close()
        ohjelmavalinta = wx.SingleChoiceDialog(None, "Valitse ohjelma", "Ohjelmat", z, wx.CHOICEDLG_STYLE)

        if ohjelmavalinta.ShowModal() == wx.ID_OK:
            ohjelmavalinta = ohjelmavalinta.GetStringSelection()
            print("lähetetään kkssälle tieto tt syvyydellä {} on {}".format(self.haesyvyys(), ohjelmavalinta))

            self.config.read("USECONTROL.ini")
            os.chdir(self.config["DEFAULT"]["polku"])
            with open("{}.txt".format(self.hanke), 'a') as textfile:
                textfile.write("\n{} syvyydellä {}".format(self.syvyys, ohjelmavalinta))
                textfile.close()
            os.chdir(self.root)
            with open("tutkimustavat.txt", "r", encoding="utf-8-sig") as textfile:
                for line in textfile:
                    if line.__contains__(ohjelmavalinta):
                        self.tutkimustapa = line[:2]
                        return line[:2]

    # valitaan luokalle maalaji listalta
    # maalajit kakkosikkunaan valitaan tekstitiedostosta ensimmäisen ikkunan
    # valinnan kolmen ensimmäisen kirjaimen mukaan.
    def ivalitsemaalaji(self, lista):
        maalista = []
        temp_lista = []
        maalaji = wx.SingleChoiceDialog(None, "Valitse maalaji", "Maalaji", lista,
                                           wx.CHOICEDLG_STYLE)
        if maalaji.ShowModal() == wx.ID_OK:
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
            elif maalaji == "Muut":
                maalaji = wx.SingleChoiceDialog(None, "Valitse maalaji", "Muut maat", ['TÄYTEMAA', 'KIVI', 'LOHKARE',
                                                                                       'LAPIPOR.LOHK', 'KALLIO', 'VESI',
                                                                                       'TUNTEMATON', 'EI PIIRRETÄ'])
                if maalaji.ShowModal() == wx.ID_OK:
                    maalaji = maalaji.GetStringSelection()
                    self.asetamaalaji(maalaji)
                    return None
            else:
                maalaji = maalaji.lower()
                parseri_maski = maalaji[:3]
                with open("maalajit.txt", "r", encoding="utf-8") as textfile:
                    for line in textfile:
                        if len(line) > 1:
                            lineparts = line.replace("\n", "").split("\t")
                            for line in lineparts:
                                if line.__contains__(parseri_maski):
                                    temp_lista.append(line)
                textfile.close()
                for alkio in temp_lista:
                    parsittu = re.sub('[^a-zA-Z0-9 \n\.]', '', alkio)
                    maalista.append(parsittu)
                maatyyppi = wx.SingleChoiceDialog(None, "Valitse maatyyppi", "{}".format(maalaji),
                                                  maalista, wx.CHOICEDLG_STYLE)
                if maatyyppi.ShowModal() == wx.ID_OK:
                    maatyyppi = maatyyppi.GetStringSelection()
                    self.asetamaalaji(maatyyppi)
                    return None
        else:
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
                        sa.tallennaTAL(self.hanke, linearvot)

                        self.arvot = linearvot.split()
                        self.apu = '{0:.2f}'.format(float(self.arvot[0]) / 100.00)
                        self.arvot[0] = str(self.apu)
                        self.TAL = "\t" + "\t" .join(self.arvot)

                        self.gui.linepanelille(self.TAL)

                        #kutsutaan piirtäjää ja passataan tiedot sinne --> suoraan vaiko parserin kautta?
                        #Taidetaan tehdä piirto suoraan filesta

                    if lineparts[0][:4] == "#END":
                        print("ENDI")
                        #self.iparsitiedot(lineparts)
                        #TEHDÄÄN MITAMITA??
                        #EI TULE TALLAISTA SANOMAA DEMOLLA,
                        sa.tallennaTAL(self.hanke, lineparts[0])

                    if lineparts[0][:4] == "#SYV":
                        #self.iparsitiedot(lineparts)
                        print("ENDI")
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

            voima = int(arvot[1])
            # print(voima, " voima")
            self.asetavoima(voima)

            puolikierrokset = int(arvot[2])
            self.asetapuolikierrokset(puolikierrokset)
            # print(puolikierrokset, " puolik.")

            nopeus = int(arvot[3])
            # print(nopeus, " nopeus")
            self.asetanopeus(nopeus)

    def ihallinta(self):
        os.chdir(self.root)
        x = [config.replace(".ini", "") for config in os.listdir(os.curdir) if config.endswith(".ini")
             and config != "USECONTROL.ini" and config != "HWCONTROL.ini"]
        valinta = wx.SingleChoiceDialog(None, "Valitse muokattavat tiedot", "Hallinta",
                                        x,  wx.CHOICEDLG_STYLE)
        if valinta.ShowModal() == wx.ID_OK:
            muokattava = valinta.GetStringSelection()
            valinta.Destroy()
            if muokattava == "HANKETIEDOT":
                self.ihankeheader()
            if muokattava == "PISTETIEDOT":
                self.ipisteheader()
            if muokattava == "TUTKIMUSTIEDOT":
                self.itutkimusheader()
        else:
            return None

    def ihankeheader(self):
        self.config.read("HANKETIEDOT.ini")
        uusifo = wx.TextEntryDialog(None, "FO", "HANKETIEDOT",
                                    self.config["DEFAULT"]["FO"])
        if uusifo.ShowModal() == wx.ID_OK:
            uusifo = uusifo.GetValue()

        uusikj = wx.TextEntryDialog(None, "KJ", "HANKETIEDOT",
                                    self.config["DEFAULT"]["KJ"])
        if uusikj.ShowModal() == wx.ID_OK:
            uusikj = uusikj.GetValue()

        uusiom = wx.TextEntryDialog(None, "OM", "HANKETIEDOT",
                                    self.config["DEFAULT"]["OM"])
        if uusiom.ShowModal() == wx.ID_OK:
            uusiom = uusiom.GetValue()

        uusiml = wx.TextEntryDialog(None, "ML", "HANKETIEDOT",
                                    self.config["DEFAULT"]["ML"])
        if uusiml.ShowModal() == wx.ID_OK:
            uusiml = uusiml.GetValue()

        uusiorg = wx.TextEntryDialog(None, "ORG", "HANKETIEDOT",
                                     self.config["DEFAULT"]["ORG"])
        if uusiorg.ShowModal() == wx.ID_OK:
            uusiorg = uusiorg.GetValue()

        #sa = saving.Saving()
        sa.asetaHanketiedot(uusifo, uusikj, uusiml, uusiom, uusiorg)

    def ipisteheader(self):
        self.config.read("PISTETIEDOT.ini")
        uusity = wx.TextEntryDialog(None, "TY", "PISTETIEDOT",
                                    self.config["DEFAULT"]["TY"])
        if uusity.ShowModal() == wx.ID_OK:
            uusity = uusity.GetValue()

        uusipk = wx.TextEntryDialog(None, "PK", "PISTETIEDOT",
                                    self.config["DEFAULT"]["PK"])
        if uusipk.ShowModal() == wx.ID_OK:
            uusipk = uusipk.GetValue()

        uusila = wx.TextEntryDialog(None, "LA", "PISTETIEDOT",
                                    self.config["DEFAULT"]["LA"])
        if uusila.ShowModal() == wx.ID_OK:
            uusila = uusila.GetValue()

        #sa = saving.Saving()
        sa.asetaPistetiedot(uusity, uusipk, uusila)

    def itutkimusheader(self):
        self.config.read("TUTKIMUSTIEDOT.ini")
        uusitt = wx.TextEntryDialog(None, "TT", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["TT"])
        if uusitt.ShowModal() == wx.ID_OK:
            uusitt = uusitt.GetValue()

        uusitx = wx.TextEntryDialog(None, "TX", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["TX"])
        if uusitx.ShowModal() == wx.ID_OK:
            uusitx = uusitx.GetValue()

        uusixy = wx.TextEntryDialog(None, "XY", "TUTKIMUSTIEDOT",
                                    self.config["DEFAULT"]["XY"])
        if uusixy.ShowModal() == wx.ID_OK:
            uusixy = uusixy.GetValue()

        uusiln = wx.TextEntryDialog(None, "LN", "TUTKIMUSTIEDOT",
                                        self.config["DEFAULT"]["LN"])
        if uusiln.ShowModal() == wx.ID_OK:
            uusiln = uusiln.GetValue()

        #sa = saving.Saving()
        sa.asetaTutkimustiedot(uusitt, uusitx, uusixy, uusiln)

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

# saisko tästä graafille uuden ikkunan jotenkin hienosti
class OtherFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Piirto", size=(500,500))
        panel = wx.Panel(self)


def main():
    app = wx.App()
    frame = windowClass(None)

    frame.Show(True)
    #frame.tankoarvolaatikko.SetBackgroundColor('green')
    #frame.vaihdatankovari()
    #frame.tanko()
    app.MainLoop()


if __name__ == '__main__':
    main()


#tiedontallennukset saving.py palautaTalpolku tallennuspolku, avaustiedosto jne


