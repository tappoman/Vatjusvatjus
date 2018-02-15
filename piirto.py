from numpy import arange, sin, pi, linspace
#import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('WXAgg')

import time
import os

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
#from matplotlib import style

#style.use('fivethirtyeight')

import wx
import configparser

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #self.figure = Figure()
        self.figure = plt.figure()
        #self.hanke = hanke
        self.config = configparser.ConfigParser()

        #interactive mode
        #plt.ion()

        self.axes = self.figure.add_subplot(111)
        plt.axes(xlim=(-120, 120), ylim=(0, 20))
        plt.subplots_adjust(left=0.1, right=0.85, bottom=0.10, wspace=0.2, hspace=0.2)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        #kopsattu vanhasta
        plt.gca().invert_yaxis()
        plt.axvline(0, color='k')


    def setValues(self, hanke, piste):
        self.config.read("USECONTROL.ini")
        self.polku = self.config["DEFAULT"]["polku"]
        self.tiedosto = hanke
        self.piste = piste
        self.tutkimustapa = ""

        print(self.polku, self.tiedosto, self.piste)

        self.fullpath = os.path.join(self.polku, self.tiedosto + ".txt")

        #if self.piste in open(self.fullpath).read():
         #   print("***LOYTYI***")
        self.muisti = False
        haluttupiste = "TY " + self.piste
        print(haluttupiste)

        with open(self.fullpath, 'r') as textfile:
            for line in textfile:
                #print(len(line))
                if len(line) > 2:
                    #if "TY" in line:
                    if line.startswith("TY"):
                        #print("line: ", line.strip(), "haluttu: ", haluttupiste.strip());
                        #Tutkitaan onko tyonumero teklassa sama kuin annetussa hankeessa ja pisteessa
                        if line.strip() == haluttupiste.strip():
                            print("oikea TY: ", line.strip())
                            self.muisti = True
                        else:
                            self.muisti = False
                            print("vaara TY: ", line.strip())

                    #kun oikessa pisteessa
                    if self.muisti:
                        #tutkitaan teklasta kyseisen pisteen kairaustapa
                        #if "TT" in line:
                        if line.startswith("TT"):
                            apu = line.split(" ")
                            self.tutkimustapa = str(apu[1]).strip()
                            print("TUTKIMUSTAPA: ", self.tutkimustapa)

                        #Splittaillaan arvot
                        lineparts = line.replace('\n', '').split('\t')

                        #JOS PAINOKAIRAUS (PA) --> muotoillaan chart ja arvot
                        if self.tutkimustapa == "PA":
                            if lineparts[0][:1] == "":
                                #print("linepartsit: ", lineparts)
                                #print ("LP_LENGTH: ", len(lineparts))

                                self.syvyys = lineparts[1][:4]

                                if len(lineparts) > 3:
                                    self.x2 = lineparts[2][:3]
                                    self.x1 = lineparts[3][:4]

                                    print(self.syvyys, " : ", self.x1, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('voima / puolikierrokset')

                                    if int(self.x1) != 0:
                                        plt.barh(float(self.syvyys), width=float(self.x1),
                                                 height=0.2, linewidth=1, color='b', edgecolor='k')
                                    else:
                                        plt.barh(float(self.syvyys), width=float(self.x1),
                                                 height=0.2, linewidth=1, color='b', edgecolor='k')
                                        plt.barh(float(self.syvyys), width=-float(self.x2),
                                                 height=0.2, linewidth=1, color='g', edgecolor='k')
                                    self.figure.canvas.draw()

                                else:
                                    pass


                        # JOS HEIJARIK (HE) --> muotoillaan chart ja arvot
                        elif self.tutkimustapa == "HE":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]
                                self.x2 = lineparts[2][:3]
                                #self.x1 = lineparts[3][:4]

                                print(self.syvyys, " : ", self.x2)

                                plt.ylabel("syvyys")
                                plt.xlabel('heijari / isku')

                                plt.barh(float(self.syvyys), width=-float(self.x2),
                                         height=0.1, linewidth=1, color='g', edgecolor='k')
                                self.figure.canvas.draw()

                        # JOS PORAK (PO) --> muotoillaan chart ja arvot
                        #PORAK ANTAA DATAA MUODOSSA ['#MIT:61      0    1.7   30']
                        #TAL KUITENKIN _AINA_ MUODOSSA ['#TAL:60      0    ']
                        #LAITETAAN NYT SYVYYS NÄKYVIIN ARVOILLA self.x1=10, self.x2=10
                        elif self.tutkimustapa == "PO":
                            if lineparts[0][:1] == "":
                                self.syvyys = lineparts[1][:4]
                                #self.x2 = lineparts[2][:3]
                                #self.x1 = lineparts[3][:4]

                                self.x1 = 10
                                self.x2 = 10

                                print(self.syvyys, " : ", self.x2)

                                plt.ylabel("syvyys")
                                plt.xlabel('aika')

                                plt.barh(float(self.syvyys), width=float(self.x1),
                                         height=0.1, linewidth=1, color='b', edgecolor='k')

                                plt.barh(float(self.syvyys), width=-float(self.x2),
                                         height=0.1, linewidth=1, color='g', edgecolor='k')
                                self.figure.canvas.draw()

                        # JOS TARYK (TK) --> muotoillaan chart ja arvot
                        #vain syvyytta, miten muotoillaan etta nakyy selkeästi
                        #TARYKAIRAUS EI ANNA TAL SANOMAA: EI VOIDA NÄYTTÄÄ
                        if self.tutkimustapa == "TR":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]
                                self.x2 = 10
                                self.x1 = 10

                                print(self.syvyys, " : ", self.x2)

                                plt.ylabel("syvyys")
                                plt.xlabel('')

                                plt.barh(float(self.syvyys), width=float(self.x1),
                                         height=0.1, linewidth=1, color='b', edgecolor='k')

                                plt.barh(float(self.syvyys), width=-float(self.x2),
                                         height=0.1, linewidth=1, color='g', edgecolor='k')
                                self.figure.canvas.draw()

                        # JOS PURISTIHEIJARI (PH) --> muotoillaan chart ja arvot
                        # Vaikuttaisi tulevan vain yksi arvo #TAL sanomassa = syvyys
                        if self.tutkimustapa == "PH":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]
                                self.x2 = 10
                                self.x1 = 10

                                print(self.syvyys, " : ", self.x2)

                                plt.ylabel("syvyys")
                                plt.xlabel('')
                                plt.barh(float(self.syvyys), width=float(self.x1),
                                         height=0.1, linewidth=1, color='b', edgecolor='k')

                                plt.barh(float(self.syvyys), width=-float(self.x2),
                                         height=0.1, linewidth=1, color='g', edgecolor='k')
                                self.figure.canvas.draw()


    def addValues(self, syvyys, voima, puolikierrokset):
        pass


    def draw(self):
        self.figure.canvas.draw()
