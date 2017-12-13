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

# import saving
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
        self.ohjelmabutton = wx.Button(panel, label="Ohjelma", pos=(235, 10), size=(110, 110))
        self.ohjelmabutton.SetFont(font1)
        self.ohjelmabutton.Bind(wx.EVT_BUTTON, self.valitseohjelma)

        # hallinta
        # hallitaan valtakuntaa
        self.hallintabutton = wx.Button(panel, label="Hallinta", pos=(350, 10), size=(110, 110))
        self.hallintabutton.SetFont(font1)
        self.hallintabutton.Bind(wx.EVT_BUTTON, self.hallintamenu)

        # maalaji
        # käyttäjä asettaa maalajin listalta
        self.maalajibutton = wx.Button(panel, label="Maalaji", pos=(465, 10), size=(110, 110))
        self.maalajibutton.SetFont(font1)
        self.maalajibutton.Bind(wx.EVT_BUTTON, self.valitsemaalaji)

        # piirto
        # käyttäjä voi valita piirtonäkymän
        self.graphbutton = wx.Button(panel, label="Piirto", pos=(10, 215), size=(200, 100))
        self.graphbutton.SetFont(font1)
        self.graphbutton.Bind(wx.EVT_BUTTON, self.graafinpiirto)

        # hae
        # communications listenerin mockup
        self.loadbutton = wx.Button(panel, label="Hae", pos=(220, 215), size=(50, 50))
        self.loadbutton.SetFont(font1)
        self.loadbutton.Bind(wx.EVT_BUTTON, self.lataapiste)

        # alusta
        # tyhjentää paneelin ja asettaa arvot alkuarvoiksi
        self.alustabutton = wx.Button(panel, label="Alusta", pos=(220, 265), size=(75, 50))
        self.alustabutton.SetFont(font1)
        self.alustabutton.Bind(wx.EVT_BUTTON, self.alustatiedot)

        # alkusyvyys
        # käyttäjä voi valita alkusyvyyden, joka lisätään listenerin syvyys arvoon
        self.alkusyvyysbutton = wx.Button(panel, label="a-syv", pos=(300, 215), size=(100,100))
        self.alkusyvyysbutton.SetFont(font1)
        self.alkusyvyysbutton.Bind(wx.EVT_BUTTON, self.asetaalkusyvyys)

        # tietotekstien alustus
        self.hanketeksti = wx.StaticText(panel, -1, "Hanke: ", pos=(10, 120))
        self.hanketeksti.SetFont(font2)

        # tiedostonimiteksti näyttää valitun hankkeen nimen
        self.hankenimiteksti = wx.StaticText(panel, -1, ">hankkeen nimi<", pos=(220, 120))
        self.hankenimiteksti.SetFont(font2)

        self.pisteteksti = wx.StaticText(panel, -1, "Piste: ", pos=(10, 165))
        self.pisteteksti.SetFont(font2)

        # pistenimiteksti näyttää valitusta hankkeesta valitun pisteen
        self.pistenimiteksti = wx.StaticText(panel, -1, ">pisteen nimi<", pos=(150, 165))
        self.pistenimiteksti.SetFont(font2)

        # ohjelmanimiteksti näyttää valitusta ohjelmanappulasta käytössäolevan ohjelman
        self.ohjelmateksti = wx.StaticText(panel, -1, "Ohjelma:", pos=(410, 215))
        self.ohjelmateksti.SetFont(font1)

        self.ohjelmaarvoteksti = wx.StaticText(panel, -1, "><", pos=(500, 215))
        self.ohjelmaarvoteksti.SetFont(font1)

        # alatekstien alustus
        self.alkusyvyysteksti = wx.StaticText(panel, -1, "A-syv", pos=(5, 315))
        self.alkusyvyysteksti.SetFont(font1)

        # alkusyvyysarvoteksti päivittyy käyttäjän valinnan mukaan
        self.alkusyvyysarvoteksti = wx.StaticText(panel, -1, "><", pos=(5, 345))
        self.alkusyvyysarvoteksti.SetFont(font2)


        self.syvyysteksti = wx.StaticText(panel, -1, "Syvyys", pos=(70, 315))
        self.syvyysteksti.SetFont(font1)

        # syvyysarvoteksti päivittyy alkusyvyys + listeneriltä tuleva syvyys
        self.syvyysarvoteksti = wx.StaticText(panel, -1, "><", pos=(75, 345))
        self.syvyysarvoteksti.SetFont(font2)

        self.voimateksti = wx.StaticText(panel, -1, "Voima", pos=(150, 315))
        self.voimateksti.SetFont(font1)

        # voima-arvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.voimaarvoteksti = wx.StaticText(panel, -1, "><", pos=(160, 345))
        self.voimaarvoteksti.SetFont(font2)

        self.puolikierroksetteksti = wx.StaticText(panel, -1, "P-kierr", pos=(230, 315))
        self.puolikierroksetteksti.SetFont(font1)

        # puolikierroksetarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.puolikierroksetarvoteksti = wx.StaticText(panel, -1, "><", pos=(240, 345))
        self.puolikierroksetarvoteksti.SetFont(font2)


        self.nopeusteksti = wx.StaticText(panel, -1, "Nopeus", pos=(310, 315))
        self.nopeusteksti.SetFont(font1)

        # nopeusarvoteksti päivittyy listeneriltä tulevan voiman mukaan
        self.nopeusarvoteksti = wx.StaticText(panel, -1, "><", pos=(315, 345))
        self.nopeusarvoteksti.SetFont(font2)

        self.maalajiteksti = wx.StaticText(panel, -1, "Maalaji", pos=(390, 315))
        self.maalajiteksti.SetFont(font1)

        # maalajiarvoteksti päivittyy käyttäjän valitessa maalaji
        self.maalajiarvoteksti = wx.StaticText(panel, -1, "><", pos=(390, 345))
        self.maalajiarvoteksti.SetFont(font2)

        self.iskuteksti = wx.StaticText(panel, -1, "Isku", pos=(515, 315))
        self.iskuteksti.SetFont(font1)

        # iskuarvoteksti päivittyy käyttäjän valitessa isku
        self.iskuarvoteksti = wx.StaticText(panel, -1, "OFF", pos=(515, 345))
        self.iskuarvoteksti.SetFont(font2)

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
        uusikysymys = wx.MessageDialog(None, "Luodaanko uusi hanke?","Hanke", wx.YES_NO)
        uusivastaus = uusikysymys.ShowModal()
        uusikysymys.Destroy()
        if uusivastaus == wx.ID_NO:
            if self.hankenimiteksti.GetLabel() != ">hankkeen nimi<":
                os.chdir(self.data.root)
                self.hanke = self.data.iavaahanke()
                self.hankenimiteksti.SetLabelText(self.data.hanke)
                self.pistenimiteksti.SetLabelText(">pisteen nimi<")
                self.syvyysarvoteksti.SetLabelText("><")
                self.voimaarvoteksti.SetLabelText("><")
                self.puolikierroksetarvoteksti.SetLabelText("><")
                self.nopeusarvoteksti.SetLabelText("><")
                os.chdir(os.path.join(os.path.abspath(os.path.curdir), self.data.hanke))
            else:
                self.hanke = self.data.iavaahanke()
                self.hankenimiteksti.SetLabelText(self.hanke)
                self.pistenimiteksti.SetLabelText(">pisteen nimi<")
                os.chdir(os.path.join(os.path.abspath(os.path.curdir), self.data.hanke))
        else:
            self.luohanke()

    # luodaan hanke käyttäjän antamalla nimellä
    # estetään ylikirjoitus try-exceptillä
    def luohanke(self):
        os.chdir(self.data.root)
        hankenimi = wx.TextEntryDialog(None, "Anna uudelle hankkeelle nimi", "Uuden hankkeen luonti")
        if hankenimi.ShowModal() == wx.ID_OK:
            hankenimi = hankenimi.GetValue()
            varmistus = wx.MessageDialog(None, "Luodaan hanke {}".format(hankenimi), "Luodaan..", wx.YES_NO)
            luo = varmistus.ShowModal()
            if luo == wx.ID_YES and os.curdir==".":
                try:
                    os.mkdir(hankenimi)
                    self.hankenimiteksti.SetLabelText(hankenimi)
                    os.chdir(hankenimi)
                    self.luopiste(hankenimi)
                except FileExistsError:
                    warning = wx.MessageDialog(None, "Hanke {} on jo olemassa".format(hankenimi), "Varoitus", wx.OK | wx.ICON_INFORMATION)
                    warning.ShowModal()
                    warning.Destroy()

    def pisteenavaus(self, event):
        if self.hankenimiteksti.GetLabel() == ">hankkeen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin hanke", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:

            uusikysymys = wx.MessageDialog(None, "Luodaanko uusi piste hankkeelle {}?".format(self.hanke), "Piste",
                                           wx.YES_NO)
            uusivastaus = uusikysymys.ShowModal()
            uusikysymys.Destroy()
            if uusivastaus == wx.ID_NO:
                piste, header = self.data.iavaapiste()
                parsittu = os.path.splitext(piste)[0]
                for i in header:
                    self.scrolled_panel.ScrollLines(1)
                    self.scrolled_panel.SetupScrolling(scrollToTop=False, scrollIntoView=False)
                    self.scrolled_panel.Layout()
                    self.scrolled_panel.Refresh()
                    new_text = wx.StaticText(self.scrolled_panel, -1, i, size=(550, 30))
                    font = new_text.GetFont()
                    font.SetPointSize(15)
                    new_text.SetFont(font)
                    self.spSizer.Add(new_text)
                self.pistenimiteksti.SetLabelText(parsittu)
            else:
                self.luopiste(self.hanke)

    # luodaan piste käyttäjän antamalla nimellä
    # estetään ylikirjoitus try-exceptillä
    def luopiste(self, hanke):
        print(os.getcwd())
        print("luodaan pistettä hankkeeseen {}".format(hanke))
        pistenimi = wx.TextEntryDialog(None, "Anna hankkeen {} uudelle pisteelle nimi".format(hanke),
                                       "Uuden pisteen luonti hankkeelle {}".format(hanke))
        if pistenimi.ShowModal() == wx.ID_OK:
            pistenimi = pistenimi.GetValue()
            varmistus = wx.MessageDialog(None, "Luodaan piste {} hankkeelle {}".format(pistenimi, hanke)
                                         , "Luodaan..", wx.YES_NO)
            luo = varmistus.ShowModal()
            if luo == wx.ID_YES and os.curdir == ".":
                try:
                    file = open("{}.txt".format(pistenimi), "r")
                    file.close()
                    warning = wx.MessageDialog(None, "Piste {} on jo olemassa".format(pistenimi), "Varoitus",
                                               wx.OK | wx.ICON_INFORMATION)
                    warning.ShowModal()
                    warning.Destroy()
                except FileNotFoundError:
                    file = open("{}.txt".format(pistenimi), "w", encoding="utf-8")
                    file.close()
                    self.pistenimiteksti.SetLabelText(pistenimi)

    # kysyy käyttäjältä alkusyvyyttä, joka tallennetaan
    # windowclassin.data luokkaan
    def asetaalkusyvyys(self, event):
        alkusyvyys = wx.TextEntryDialog(None, 'Aseta alkusyvyys',"Alkusyvyys","",
                style=wx.OK)
        alkusyvyys.ShowModal()
        self.alkusyvyysarvoteksti.SetLabelText(alkusyvyys.GetValue())
        self.data.asetaalkusyvyys(int(alkusyvyys.GetValue()))
        alkusyvyys.Destroy()

    def lataapiste(self, event):
        if self.pistenimiteksti.GetLabel() == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.piste = self.pistenimiteksti.GetLabel()
            self.data.ikuuntele()
            self.update()

    # kutsuu päivityksiä arvoteksteille ja paneelille
    def update(self):
        # print(self.listener)
        self.updatepiste(self.data)
        self.updatetextpanel(self.data)

    # päivittää tekstipaneelin yläpuolella olevat arvotekstit com-listenerin tietojen mukaan
    def updatepiste(self, data):
        self.data.ikuuntele()
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
        z = [nimi for nimi in next(os.walk('.'))[1] if not nimi.endswith("_")]
        tiedostonvalinta = wx.SingleChoiceDialog(None, "Valitse hanke", "Hankkeet", z, wx.CHOICEDLG_STYLE)
        if tiedostonvalinta.ShowModal() == wx.ID_OK:
            self.hanke = tiedostonvalinta.GetStringSelection()
            tiedostonvalinta.Destroy()
            return self.hanke

    def iavaapiste(self):
        x = [nimi.replace(".txt","") for nimi in os.listdir(os.curdir) if nimi.endswith(".txt")]
        pistevalinta = wx.SingleChoiceDialog(None, "Valitse piste", "Pisteet", x, wx.CHOICEDLG_STYLE)
        if pistevalinta.ShowModal() == wx.ID_OK:
            self.piste = pistevalinta.GetStringSelection()
            pistevalinta.Destroy()
            pisteheader = self.iparsiheader()
            return self.piste, pisteheader

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
        ohjelmavalinta = wx.SingleChoiceDialog(None, "Valitse piste", "Pisteet", z, wx.CHOICEDLG_STYLE)
        if ohjelmavalinta.ShowModal() == wx.ID_OK:
            ohjelmavalinta = ohjelmavalinta.GetStringSelection()
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

    # luetaan tiedot tekstitiedostosta, mockup communication listenistä
    def ikuuntele(self):
        with open("data0.txt", 'r', encoding="utf-8") as textfile:
            for line in textfile:
                if len(line) > 1:
                    lineparts = line.replace('\n', '').split('\t')
                    if lineparts.__contains__("#"):
                        self.iparsitiedot(lineparts)
            textfile.close()
        return None

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
        return None

    def ihallinta(self):
        self.iluotempconfig()
        x = [config.replace(".ini", "") for config in os.listdir(os.curdir) if config.endswith(".ini")]
        valinta = wx.SingleChoiceDialog(None, "Valitse muokattavat tiedot", "Hallinta", x,  wx.CHOICEDLG_STYLE)
        if valinta.ShowModal() == wx.ID_OK:
            muokattava = valinta.GetStringSelection()
            valinta.Destroy()
            if muokattava == "HANKETIEDOT":
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

            with open("{}.txt".format(self.piste), 'r', encoding="utf-8") as textfile:
                for line in textfile:
                    if len(line) > 1:
                        print(line)
        return None

    def iluotempconfig(self):
        os.chdir(self.root)
        shutil.copy('HANKETIEDOT.ini', '{}'.format(self.hanke))
        shutil.copy('PISTETIEDOT.ini', '{}'.format(self.hanke))
        shutil.copy('TUTKIMUSTIEDOT.ini', '{}'.format(self.hanke))
        os.chdir(self.hanke)
        print("temp tiedostot luotu hankkeelle {}".format(self.hanke))
        return None

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


