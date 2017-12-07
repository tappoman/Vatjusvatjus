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
import communication
import guioperations
import threading
import serial


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
        self.com = communication
        self.gui = guioperations
        self.listener = self.com.Communication("com3", 9600)
        t1 = threading.Thread(target=self.com.Communication.readValues(self.listener))
        t1.start()
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

        # tiedosto
        # avaa hankkeen listalta
        self.tiedostobutton = wx.Button(panel, label="Tiedosto", pos=(5, 10), size=(110, 110))
        self.tiedostobutton.SetFont(font1)
        self.tiedostobutton.Bind(wx.EVT_BUTTON, self.tiedostonavaus)

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
        self.tiedostoteksti = wx.StaticText(panel, -1, "Tiedosto: ", pos=(10, 120))
        self.tiedostoteksti.SetFont(font2)

        # tiedostonimiteksti näyttää valitun hankkeen nimen
        self.tiedostonnimiteksti = wx.StaticText(panel, -1, ">tiedoston nimi<", pos=(220, 120))
        self.tiedostonnimiteksti.SetFont(font2)

        self.pisteteksti = wx.StaticText(panel, -1, "Piste: ", pos=(10, 165))
        self.pisteteksti.SetFont(font2)

        # pistenimiteksti näyttää valitusta hankkeesta valitun pisteen
        self.pistenimiteksti = wx.StaticText(panel, -1, ">pisteen nimi<", pos=(150, 165))
        self.pistenimiteksti.SetFont(font2)

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
        self.nopeusarvoteksti = wx.StaticText(panel, -1, "><", pos=(325, 345))
        self.nopeusarvoteksti.SetFont(font2)

        self.maalajiteksti = wx.StaticText(panel, -1, "Maalaji", pos=(410, 315))
        self.maalajiteksti.SetFont(font1)

        # maalajiarvoteksti päivittyy käyttäjän valitessa maalaji
        self.maalajiarvoteksti = wx.StaticText(panel, -1, "SaSi", pos=(390, 345))
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

    def tiedostonavaus(self, event):
        if self.tiedostonnimiteksti.GetLabel() != ">tiedoston nimi<":
            os.chdir("..")
            self.tiedosto = TiedonKasittely.iavaatiedosto(self)
            self.tiedostonnimiteksti.SetLabelText(self.tiedosto)
            self.pistenimiteksti.SetLabelText(">pisteen nimi<")
            self.syvyysarvoteksti.SetLabelText("><")
            self.voimaarvoteksti.SetLabelText("><")
            self.puolikierroksetarvoteksti.SetLabelText("><")
            self.nopeusarvoteksti.SetLabelText("><")
            os.chdir(os.path.join(os.path.abspath(os.path.curdir), windowClass.tiedostonnimiteksti))
        else:
            self.tiedosto = TiedonKasittely.iavaatiedosto(data)
            windowClass.tiedostonnimiteksti = self.tiedosto
            self.tiedostonnimiteksti.SetLabelText(self.tiedosto)
            self.pistenimiteksti.SetLabelText(">pisteen nimi<")
            os.chdir(os.path.join(os.path.abspath(os.path.curdir), windowClass.tiedostonnimiteksti))

    def pisteenavaus(self, event):
        if self.tiedostonnimiteksti == ">tiedoston nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin tiedosto", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.piste = TiedonKasittely.iavaapiste(self)
            windowClass.pistenimiteksti = self.piste
            parsittu = os.path.splitext(self.piste)[0]
            self.pistenimiteksti.SetLabelText(parsittu)

    # kysyy käyttäjältä alkusyvyyttä, joka tallennetaan
    # windowclassin.data luokkaan
    def asetaalkusyvyys(self, event):
        alkusyvyys = wx.TextEntryDialog(None, 'Aseta alkusyvyys:',"alkusyvyys","",
                style=wx.OK)
        alkusyvyys.ShowModal()
        windowClass.alkusyvyysarvoteksti = self.alkusyvyysarvoteksti
        windowClass.alkusyvyysarvoteksti.SetLabelText(alkusyvyys.GetValue())
        self.data.asetaalkusyvyys(int(alkusyvyys.GetValue()))
        alkusyvyys.Destroy()

    def lataapiste(self, event):
        if self.pistenimiteksti == ">pisteen nimi<":
            warning = wx.MessageDialog(None, "Valitse ensin piste", "Varoitus", wx.OK | wx.ICON_INFORMATION)
            warning.ShowModal()
            warning.Destroy()
        else:
            self.piste = self.pistenimiteksti.GetLabel()
            TiedonKasittely.iluetiedot(self.data)
            windowClass.update(self, wx.Timer)

    # kutsuu päivityksiä arvoteksteille ja paneelille
    def update(self, event):
        # print(self.listener)
        windowClass.updatepiste(self, self.data)
        windowClass.updatetextpanel(self, self.data)
        print("update")

    # päivittää tekstipaneelin yläpuolella olevat arvotekstit com-listenerin tietojen mukaan
    def updatepiste(self, data):
        self.data.iluetiedot()
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
        self.tiedostonnimiteksti.SetLabelText(">tiedoston nimi<")
        self.pistenimiteksti.SetLabelText(">pisteen nimi<")
        self.alkusyvyysarvoteksti.SetLabelText("><")
        self.syvyysarvoteksti.SetLabelText("><")
        self.voimaarvoteksti.SetLabelText("><")
        self.puolikierroksetarvoteksti.SetLabelText("><")
        self.nopeusarvoteksti.SetLabelText("><")
        self.maalajiarvoteksti.SetLabelText("SaSi")
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
        print("Ohjelman valinta")

    def hallintamenu(self, event):
        print("hallitsijat hallitsee")

    # käyttäjä valitsee listalta maalajin, joka tallennetaan data-luokkaan
    def valitsemaalaji(self, event):
        valinta = self.data.ivalitsemaalaji()
        print("tägättiin maalaji {} syvyydelle {}".format(valinta, self.data.haesyvyys()))
        self.maalajiarvoteksti.SetLabelText(valinta)

# Tiedonkasittely luokka
# tämä tallentaa käyttäjän ja communicationin syöttämän datan ja syöttää sen windowclass luokalle
class TiedonKasittely(object):
    def __init__(self, maalaji="SaSi", alkusyvyys=0, syvyys=0, voima=0, puolikierrokset=0, nopeus=0, figure=None):
        super(TiedonKasittely, self).__init__()

        self.maalaji = maalaji
        self.alkusyvyys = alkusyvyys
        self.syvyys = syvyys
        self.voima = voima
        self.puolikierrokset = puolikierrokset
        self.nopeus = nopeus
        self.figure = figure

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


    def iavaatiedosto(self):
        z = [nimi for nimi in alusta_tiedot.tiedostot]
        tiedostonvalinta = wx.SingleChoiceDialog(None, "Valitse tiedosto", "Tiedostot", z, wx.CHOICEDLG_STYLE)
        if tiedostonvalinta.ShowModal() == wx.ID_OK:
            self.tiedosto = tiedostonvalinta.GetStringSelection()
            tiedostonvalinta.Destroy()
            return self.tiedosto

    def iavaapiste(self):
        x = [nimi for nimi in os.listdir(os.curdir)]
        pistevalinta = wx.SingleChoiceDialog(None, "Valitse piste", "Pisteet", x, wx.CHOICEDLG_STYLE)
        if pistevalinta.ShowModal() == wx.ID_OK:
            self.piste = pistevalinta.GetStringSelection()
            pistevalinta.Destroy()
            return self.piste

    # valitaan luokalle maalaji listalta
    def ivalitsemaalaji(self):
        maavalinta = wx.SingleChoiceDialog(None, "Valitse maalaji", "", ['SaSi', 'Bedrock', 'Parquet'],
                                           wx.CHOICEDLG_STYLE)
        if maavalinta.ShowModal() == wx.ID_OK:
            TiedonKasittely.maalaji = maavalinta.GetStringSelection()
            TiedonKasittely.asetamaalaji(self, maavalinta)
            maavalinta.Destroy()
            return maavalinta.GetStringSelection()

    # luetaan tiedot tekstitiedostosta, mockup communication listenistä
    def iluetiedot(self):
        with open("data0.txt", 'r') as textfile:
            for line in textfile:
                if len(line) > 1:
                    # line = line.rpartition("#MIT:")[2]
                    lineparts = line.replace('\n', '').split('\t')
                    TiedonKasittely.iparsitiedot(self, lineparts)
                    # self.syvyys = line_s
                    # self.voima = line_v
                    # self.puolikierrokset = line_pk
                    # self.nopeus = line_n
            textfile.close()

    # parsitaan data merkittävään muotoon
    def iparsitiedot(self, line):
        line_sanoma = line[0].rpartition(":")[0]
        syvyys = int(line[0].rpartition(":")[2])
        TiedonKasittely.asetasyvyys(self, syvyys)
        voima = int(line[1])
        TiedonKasittely.asetavoima(self, voima)
        puolikierrokset = int(line[2])
        TiedonKasittely.asetapuolikierrokset(self, puolikierrokset)
        nopeus = int(line[3])
        TiedonKasittely.asetanopeus(self, nopeus)
        print("sanoma:{} syvyys:{} voima:{} pk:{} nopeus:{}".format(line_sanoma,
                                                                    self.haesyvyys(),
                                                                    self.haevoima(),
                                                                    self.haepuolikierrokset(),
                                                                    self.haenopeus()))
        # if line_sanoma =="TAL":
        # if line_sanoma == "MIT":

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


#update arvot ja piirros yhdeltä riviltä

