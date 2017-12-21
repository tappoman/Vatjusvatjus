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

# import communication
# import guioperations
# import threading
# import serial

'''
from communication import threading
import guioperations as gui
com = Communication("com3", 9600)
gui = Guioperations()
threadin aloitus 
t1 = threading.Thread(target=com.readValues()
t1.start()
'''

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, size=wx.Size(600, 960))

        self.Centre()
        self.basicGUI()
        self.data = TiedonKasittely()
        self.ba = ba
        #self.com = communication
        #self.gui = guioperations
        #self.listener = self.com.Communication("com3", 9600)
        #t1 = threading.Thread(target=self.com.Communication.readValues(self.listener))
        #t1.start()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

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

        # hanke
        # avaa hankkeen listalta
        self.hankebutton = wx.Button(panel, label="Hanke", pos=(5, 10), size=(110, 110))
        self.hankebutton.SetFont(font1)
        self.hankebutton.Bind(wx.EVT_BUTTON, self.hankkeenavaus)

        # piste
        # avaa pisteen hankkeen sisältä
        self.pistebutton = wx.Button(panel, label="Piste", pos=(120, 10), size=(110, 110))
        self.pistebutton.SetFont(font1)
        self.pistebutton.Bind(wx.EVT_BUTTON, self.pisteenavaus)

        # ohjelma
        # valitsee kairausohjelman
        self.ohjelmabutton = wx.Button(panel, label="Tutkimus-\ntapa", pos=(235, 10), size=(110, 110))
        self.ohjelmabutton.SetFont(font1)
        self.ohjelmabutton.Bind(wx.EVT_BUTTON, self.valitseohjelma)

        # hallinta
        # hallitaan valtakuntaa
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
        self.loadbutton = wx.Button(panel, label="Hae", pos=(465, 120), size=(50, 50))
        self.loadbutton.SetFont(font1)
        self.loadbutton.Bind(wx.EVT_BUTTON, self.lataapiste)

        # alusta
        # tyhjentää paneelin ja asettaa arvot alkuarvoiksi
        self.alustabutton = wx.Button(panel, label="Alusta", pos=(520, 120), size=(65, 50))
        self.alustabutton.SetFont(font1)
        self.alustabutton.Bind(wx.EVT_BUTTON, self.alustatiedot)

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
        self.lopetusbutton = wx.Button(panel, label="Lopeta", pos=(400, 215), size=(100,100))
        self.lopetusbutton.SetFont(font1)
        self.lopetusbutton.Bind(wx.EVT_BUTTON, self.lopetakairaus)

        # tankobutton
        # heilutellaan sitä tankoa
        # disco
        self.tankobutton = wx.Button(panel, label="Tanko", pos=(500, 215), size=(50,50))
        self.tankobutton.SetFont(font1)
        self.tankobutton.Bind(wx.EVT_BUTTON, self.tanko)

        # tietotekstien alustus
        self.hanketeksti = wx.StaticText(panel, -1, "Hanke: ", pos=(10, 120))
        self.hanketeksti.SetFont(font2)

        # tiedostonimiteksti näyttää valitun hankkeen nimen
        self.hankenimiteksti = wx.StaticText(panel, -1, ">hankkeen nimi<", pos=(120, 120))
        self.hankenimiteksti.SetFont(font2)

        self.pisteteksti = wx.StaticText(panel, -1, "Piste: ", pos=(10, 165))
        self.pisteteksti.SetFont(font2)

        # pistenimiteksti näyttää valitusta hankkeesta valitun pisteen
        self.pistenimiteksti = wx.StaticText(panel, -1, ">pisteen nimi<", pos=(100, 165))
        self.pistenimiteksti.SetFont(font2)

        # ohjelmanimiteksti näyttää valitusta ohjelmanappulasta käytössäolevan ohjelman
        self.ohjelmateksti = wx.StaticText(panel, -1, "Ohjelma:", pos=(230, 210))
        self.ohjelmateksti.SetFont(font1)

        self.ohjelmaarvoteksti = wx.StaticText(panel, -1, "><", pos=(315, 200))
        self.ohjelmaarvoteksti.SetFont(font2)

        # alkukairausteksti päivittyy käyttäjän valinnan mukaan
        self.alkukairausteksti = wx.StaticText(panel, -1, "AL:", pos=(230, 245))
        self.alkukairausteksti.SetFont(font1)

        self.alkukairausarvoteksti = wx.StaticText(panel, -1, "><", pos=(260, 235))
        self.alkukairausarvoteksti.SetFont(font2)

        self.alkusyvyysteksti = wx.StaticText(panel, -1, "A-syv:", pos=(230, 280))
        self.alkusyvyysteksti.SetFont(font1)

        self.alkusyvyysarvoteksti = wx.StaticText(panel, -1, "><", pos=(295, 270))
        self.alkusyvyysarvoteksti.SetFont(font2)

        # alatekstien alustus
        self.syvyysteksti = wx.StaticText(panel, -1, "Syvyys", pos=(10, 315))
        self.syvyysteksti.SetFont(font1)

        # syvyysarvoteksti päivittyy alkusyvyys + listeneriltä tuleva syvyys
        self.syvyysarvoteksti = wx.StaticText(panel, -1, "><", pos=(15, 345))
        self.syvyysarvoteksti.SetFont(font2)

        self.voimateksti = wx.StaticText(panel, -1, "Voima", pos=(85, 315))
        self.voimateksti.SetFont(font1)

        # voima-arvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.voimaarvoteksti = wx.StaticText(panel, -1, "><", pos=(95, 345))
        self.voimaarvoteksti.SetFont(font2)

        self.puolikierroksetteksti = wx.StaticText(panel, -1, "P-kierr", pos=(165, 315))
        self.puolikierroksetteksti.SetFont(font1)

        # puolikierroksetarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.puolikierroksetarvoteksti = wx.StaticText(panel, -1, "><", pos=(170, 345))
        self.puolikierroksetarvoteksti.SetFont(font2)


        self.nopeusteksti = wx.StaticText(panel, -1, "Nopeus", pos=(235, 315))
        self.nopeusteksti.SetFont(font1)

        # nopeusarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.nopeusarvoteksti = wx.StaticText(panel, -1, "><", pos=(240, 345))
        self.nopeusarvoteksti.SetFont(font2)

        self.maalajiteksti = wx.StaticText(panel, -1, "Maalaji", pos=(315, 315))
        self.maalajiteksti.SetFont(font1)

        # maalajiarvoteksti päivittyy käyttäjän valitessa maalaji
        self.maalajiarvoteksti = wx.StaticText(panel, -1, "><", pos=(320, 345))
        self.maalajiarvoteksti.SetFont(font2)

        self.iskuteksti = wx.StaticText(panel, -1, "Isku", pos=(455, 315))
        self.iskuteksti.SetFont(font1)

        # iskuarvoteksti päivittyy käyttäjän valitessa isku
        self.iskuarvoteksti = wx.StaticText(panel, -1, "OFF", pos=(445, 345))
        self.iskuarvoteksti.SetFont(font2)

        self.tankoteksti = wx.StaticText(panel, -1, "Tanko", pos=(515, 315))
        self.tankoteksti.SetFont(font1)

        # iskuarvoteksti päivittyy käyttäjän valitessa isku
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
            if uusivastaus == wx.ID_NO:
                return None
            else:
                self.data.iluopiste(self.data.hanke)
                self.pistenimiteksti.SetLabelText(self.data.piste)

    # kysyy käyttäjältä alkusyvyyttä, joka tallennetaan
    # windowclassin.data luokkaan
    def aloitaalkukairaus(self, event):
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
                print("lähetä tieto kks alkukairaus ohitetaan")
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
                alkusyvyys.Destroy()
                print("lähetetään kkssälle: työnumero, kairausvalinta, piste, pvm(timestä?)")
                # print("lähetetään kkssälle: työnumero(hanke?), {}, {}, pvm(timestä?)".format(kairausvalinta)
                #       , self.data.piste)

    def lopetakairaus(self, event):
        os.chdir(self.data.root)
        z = []
        with open("kairausloppu.txt", "r") as textfile:
            for line in textfile:
                if len(line) > 1:
                    z.append(line.rsplit(" ")[1].strip("\n"))
        textfile.close()
        kairausvalinta = wx.SingleChoiceDialog(None, "Valitse lopetussyy", "Kairauksen lopetus", z, wx.CHOICEDLG_STYLE)
        if kairausvalinta.ShowModal() == wx.ID_OK:
            kairausvalinta = kairausvalinta.GetStringSelection()
            print("lähetetään kkssälle tieto kairaus lopetettiin syvyydellä {} syystä {}"
                  .format(self.data.haesyvyys(), kairausvalinta))
            os.chdir("GEOXX")
            with open("{}.txt".format(self.data.hanke), 'a') as textfile:
                textfile.write("lopetus: {} syvyydellä {}".format(self.data.syvyys, kairausvalinta))
                textfile.close()
            os.chdir(self.data.root)
        else:
            return None

    def tanko(self, event):
        if self.tankoarvolaatikko.GetBackgroundColour() == 'red':
            self.tankoarvolaatikko.SetBackgroundColour('green')
            self.tankoarvolaatikko.Refresh()
        elif self.tankoarvolaatikko.GetBackgroundColour() == 'green':
            self.tankoarvolaatikko.SetBackgroundColour('red')
            self.tankoarvolaatikko.Refresh()
        return None

    def lataapiste(self, event):
        if self.pistenimiteksti.GetLabel() == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.piste = self.pistenimiteksti.GetLabel()
            self.update()

    # kutsuu päivityksiä arvoteksteille ja paneelille
    def update(self):
        # print(self.listener)
        self.data.ikuuntele()
        self.updatepiste(self.data)
        self.updatetextpanel(self.data)

    # päivittää tekstipaneelin yläpuolella olevat arvotekstit com-listenerin tietojen mukaan
    def updatepiste(self, data):
        self.voimaarvoteksti.SetLabelText(str(data.voima))
        self.puolikierroksetarvoteksti.SetLabelText(str(data.puolikierrokset))
        self.nopeusarvoteksti.SetLabelText(str(data.nopeus))
        if self.data.alkusyvyys != 0:
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys+data.alkusyvyys))
        else:
            self.syvyysarvoteksti.SetLabelText(str(data.syvyys))

    # kirjoittaa tekstipaneelille uuden elementin data-luokan tiedoista
    def updatetextpanel(self, data):
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
    def alustatiedot(self, event):
        self.hankenimiteksti.SetLabelText(">tiedoston nimi<")
        self.pistenimiteksti.SetLabelText(">pisteen nimi<")
        self.alkusyvyysarvoteksti.SetLabelText("><")
        self.syvyysarvoteksti.SetLabelText("><")
        self.voimaarvoteksti.SetLabelText("><")
        self.puolikierroksetarvoteksti.SetLabelText("><")
        self.nopeusarvoteksti.SetLabelText("><")
        self.maalajiarvoteksti.SetLabelText("><")
        self.ohjelmaarvoteksti.SetLabelText("><")
        self.data = TiedonKasittely()
        self.scrolled_panel.ScrollLines(150)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()
        for i in range(20):
            line = ""
            new_text = wx.StaticText(self.scrolled_panel, -1, line, size=(550, 30))
            self.spSizer.Add(new_text)
            self.scrolled_panel.ScrollLines(10)
            self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
            self.scrolled_panel.Layout()
            self.scrolled_panel.Refresh()
        new_text = wx.StaticText(self.scrolled_panel, -1, "----------------", size=(550, 30))
        font = new_text.GetFont()
        font.SetPointSize(15)
        new_text.SetFont(font)
        self.spSizer.Add(new_text)
        new_text = wx.StaticText(self.scrolled_panel, -1, "Tiedot tyhjennetty", size=(550, 40))
        font = new_text.GetFont()
        font.SetPointSize(25)
        new_text.SetFont(font)
        self.spSizer.Add(new_text)
        new_text = wx.StaticText(self.scrolled_panel, -1, "----------------", size=(550, 30))
        font = new_text.GetFont()
        font.SetPointSize(15)
        new_text.SetFont(font)
        self.spSizer.Add(new_text)
        self.scrolled_panel.ScrollLines(250)
        self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
        self.scrolled_panel.Layout()
        self.scrolled_panel.Refresh()
        self.ba.plt.clf()

    def graafinpiirto(self, event):
        # if ba.fig == None:
        #     graafi.show()
        ba.main(self.data)
        print("lululu noob noob")

    def valitseohjelma(self, event):
        ohjelma = self.data.ivalitseohjelma()
        self.ohjelmaarvoteksti.SetLabelText(ohjelma)

    def hallintamenu(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            varoitus = wx.MessageDialog(None, "Valitse ensin hanke ja piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            varoitus.ShowModal()
            varoitus.Destroy()
        elif self.pistenimiteksti.GetLabel() == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
        else:
            hallinta = self.data.ihallinta()

    # käyttäjä valitsee listalta maalajin, joka tallennetaan data-luokkaan
    def valitsemaalaji(self, event):
        self.data.iluemaalajit()
        print("tägättiin maalaji{} syvyydelle {}".format(self.data.haemaalaji(), self.data.haesyvyys()))
        tagi = self.data.haemaalaji()
        os.chdir(self.data.root)
        with open("maalajit.txt", "r", encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    lineparts = line.replace("\n", "").strip("\t")
                    if lineparts.__contains__("-{}".format(tagi)):
                        lyhenne = lineparts.rsplit(' ')[0].replace(',', "")
                        self.maalajiarvoteksti.SetLabelText(lyhenne)

        textfile.close()

# tietojenkäsittely luokka
# tämä tallentaa käyttäjän ja communicationin syöttämän datan ja syöttää sen eteenpäin windowclass luokalle
# ja tallennettaviin tietoihin
class TiedonKasittely(object):
    def __init__(self, hanke = None, piste=None, maalaji="", alkusyvyys=0, syvyys=0, voima=0,
                 puolikierrokset=0, nopeus=0, figure=None, ROOT_DIR = os.path.dirname(os.path.abspath(__file__))):
        super(TiedonKasittely, self).__init__()

        self.hanke = hanke
        self.piste = piste
        self.maalaji = maalaji
        self.alkusyvyys = alkusyvyys
        self.syvyys = syvyys
        self.voima = voima
        self.puolikierrokset = puolikierrokset
        self.nopeus = nopeus
        self.figure = figure
        self.root = ROOT_DIR
        self.config = configparser.ConfigParser()

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
        os.chdir("GEOXX")
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
                    file.write(self.config["DEFAULT"]["fo"])
                    file.write("\n"+self.config["DEFAULT"]["kj"])
                    file.write("\n"+self.config["DEFAULT"]["om"])
                    file.write("\n"+self.config["DEFAULT"]["ml"])
                    file.write("\n"+self.config["DEFAULT"]["org"])
                    file.close()
                    self.ituhoatempconfig()
                    os.chdir(self.root)
            else:
                os.chdir(self.root)
                return None
        else:
            os.chdir(self.root)
            hankenimi.Destroy()
            print("hanketta ei luotu")
            return None

    # luodaan piste käyttäjän antamalla nimellä
    # estetään ylikirjoitus try-exceptillä
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
                file.write("\n" + "PISTENIMI: {}".format(nimi))
                file.write("\n" + self.config["DEFAULT"]["ty"])
                file.write("\n" + self.config["DEFAULT"]["pk"])
                file.write("\n" + self.config["DEFAULT"]["la"])
                self.config.read("TUTKIMUSTIEDOT.ini")
                file.write("\n" + self.config["DEFAULT"]["tt"])
                file.write("\n" + self.config["DEFAULT"]["tx"])
                file.write("\n" + self.config["DEFAULT"]["xy"])
                file.write("\n" + self.config["DEFAULT"]["ln"] + "\n")
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
            os.chdir("GEOXX")
            with open("{}.txt".format(self.hanke), 'a') as textfile:
                textfile.write("{} syvyydellä {}".format(self.syvyys, ohjelmavalinta))
                textfile.close()
            os.chdir(self.root)
            with open("tutkimustavat.txt", "r", encoding="utf-8-sig") as textfile:
                for line in textfile:
                    if line.__contains__(ohjelmavalinta):
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
                return None
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
                    os.chdir("GEOXX")
                    textfile = open("{}.txt".format(self.hanke), 'a')
                    textfile.write("{} syvyydellä {}".format(maalaji, self.syvyys))
                    textfile.close()
                    os.chdir(self.root)
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
                    os.chdir("GEOXX")
                    textfile = open("{}.txt".format(self.hanke), 'a')
                    textfile.write("{} syvyydellä {}".format(maalaji, self.syvyys))
                    textfile.close()
                    os.chdir(self.root)
                    self.asetamaalaji(maatyyppi)
                    return None

    # luetaan tiedot tekstitiedostosta, mockup communication listenistä
    def ikuuntele(self):
        z = []
        with open("data0.txt", 'r', encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    lineparts = line.replace('\n', '').split('\t')
                    if lineparts[0][:4]==("#MIT"):
                        self.iparsitiedot(lineparts)

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
    def iparsitiedot(self, line):
        print(line)
        line_sanoma = line[0].rpartition(":")[0]
        syvyys = int(line[0].rpartition(":")[2])
        self.asetasyvyys(syvyys)
        voima = int(line[1])
        self.asetavoima(voima)
        puolikierrokset = int(line[2])
        self.asetapuolikierrokset(puolikierrokset)
        nopeus = int(line[3])
        self.asetanopeus(nopeus)
        # if line_sanoma =="TAL":
            #lätä takasin
        # if line_sanoma == "MIT":
            #printtaa

    def ihallinta(self):
        self.iluotempconfig()
        x = [config.replace(".ini", "") for config in os.listdir(os.curdir) if config.endswith(".ini")]
        valinta = wx.SingleChoiceDialog(None, "Valitse muokattavat tiedot", "Hallinta", x,  wx.CHOICEDLG_STYLE)
        if valinta.ShowModal() == wx.ID_OK:
            muokattava = valinta.GetStringSelection()
            valinta.Destroy()
            if muokattava == "HANKETIEDOT":
                self.ihankeheader()
            if muokattava == "PISTETIEDOT":
                self.ipisteheader()
            if muokattava == "TUTKIMUSTIEDOT":
                self.itutkimusheader()

    def ihankeheader(self):
        self.config.read("HANKETIEDOT.ini")
        uusifo = wx.TextEntryDialog(None, "FO", "{} hanketiedot".format(self.hanke),
                                    self.config["DEFAULT"]["fo"])
        if uusifo.ShowModal() == wx.ID_OK:
            uusifo = uusifo.GetValue()

        uusikj = wx.TextEntryDialog(None, "KJ", "{} hanketiedot".format(self.hanke),
                                    self.config["DEFAULT"]["KJ"])
        if uusikj.ShowModal() == wx.ID_OK:
            uusikj = uusikj.GetValue()

        uusiom = wx.TextEntryDialog(None, "OM", "{} hanketiedot".format(self.hanke),
                                    self.config["DEFAULT"]["OM"])
        if uusiom.ShowModal() == wx.ID_OK:
            uusiom = uusiom.GetValue()

        uusiml = wx.TextEntryDialog(None, "ML", "{} hanketiedot".format(self.hanke),
                                    self.config["DEFAULT"]["ML"])
        if uusiml.ShowModal() == wx.ID_OK:
            uusiml = uusiml.GetValue()

        uusiorg = wx.TextEntryDialog(None, "ORG", "{} hanketiedot".format(self.hanke),
                                     self.config["DEFAULT"]["ORG"])
        if uusiorg.ShowModal() == wx.ID_OK:
            uusiorg = uusiorg.GetValue()

        sa = saving.Saving()
        sa.asetaHanketiedot(uusifo, uusikj, uusiml, uusiom, uusiorg)

    def ipisteheader(self):
        self.config.read("PISTETIEDOT.ini")
        uusity = wx.TextEntryDialog(None, "TY", "{} pisteen {} tiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["TY"])
        if uusity.ShowModal() == wx.ID_OK:
            uusity = uusity.GetValue()

        uusipk = wx.TextEntryDialog(None, "PK",  "{} pisteen {} tiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["PK"])
        if uusipk.ShowModal() == wx.ID_OK:
            uusipk = uusipk.GetValue()

        uusila = wx.TextEntryDialog(None, "LA",  "{} pisteen {} tiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["LA"])
        if uusila.ShowModal() == wx.ID_OK:
            uusila = uusila.GetValue()

        sa = saving.Saving()
        sa.asetaPistetiedot(uusity, uusipk, uusila)

    def itutkimusheader(self):
        self.config.read("TUTKIMUSTIEDOT.ini")
        uusitt = wx.TextEntryDialog(None, "TT", "{} pisteen {} tutkimustiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["TT"])
        if uusitt.ShowModal() == wx.ID_OK:
            uusitt = uusitt.GetValue()

        uusitx = wx.TextEntryDialog(None, "TX", "{} pisteen {} tutkimustiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["TX"])
        if uusitx.ShowModal() == wx.ID_OK:
            uusitx = uusitx.GetValue()

        uusixy = wx.TextEntryDialog(None, "XY", "{} pisteen {} tutkimustiedot".format(self.hanke, self.piste),
                                    self.config["DEFAULT"]["XY"])
        if uusixy.ShowModal() == wx.ID_OK:
            uusixy = uusixy.GetValue()

        uusiln = wx.TextEntryDialog(None, "LN", "{} pisteen {} tutkimustiedot".format(self.hanke, self.piste),
                                        self.config["DEFAULT"]["LN"])
        if uusiln.ShowModal() == wx.ID_OK:
            uusiln = uusiln.GetValue()

        sa = saving.Saving()
        sa.asetaTutkimustiedot(uusitt, uusitx, uusixy, uusiln)

    def iluotempconfig(self):
        os.chdir(self.root)
        shutil.copy('HANKETIEDOT.ini', 'GEOXX')
        shutil.copy('PISTETIEDOT.ini', 'GEOXX')
        shutil.copy('TUTKIMUSTIEDOT.ini', 'GEOXX')
        os.chdir("GEOXX")
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
    app.MainLoop()

if __name__ == '__main__':
    main()

#tiedontallennukset saving.py palautaTalpolku tallennuspolku, avaustiedosto jne


