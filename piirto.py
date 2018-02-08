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
        plt.axes(xlim=(-120, 150), ylim=(0, 5))
        plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.2, hspace=0.2)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        #kopsattu vanhasta
        plt.gca().invert_yaxis()
        plt.axvline(0, color='k')

        #plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.2, hspace=0.2)

        #self.figure.gca().invert_yaxis()

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
        haluttupiste = "ty = " + self.piste
        #print(haluttupiste)

        with open(self.fullpath, 'r') as textfile:
            for line in textfile:
                #print(len(line))
                if len(line) > 2:
                    if "ty = " in line:
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
                        if "tt = " in line:
                            apu = line.split("=")
                            self.tutkimustapa = str(apu[1]).strip()
                            print("TUTUTKTKTKT: ", self.tutkimustapa)

                        #Splittaillaan arvot
                        lineparts = line.replace('\n', '').split('\t')

                        #JOS PAINOKAIRAUS (PA) --> muotoillaan chart ja arvot
                        if self.tutkimustapa == "PA":
                            if lineparts[0][:1] == "":
                                #print(lineparts)
                                self.syvyys = lineparts[1][:4]
                                self.x2 = lineparts[2][:3]
                                self.x1 = lineparts[3][:4]

                                print(self.syvyys, " : ", self.x1, " : ", self.x2)

                                plt.ylabel("syvyys")
                                plt.xlabel('voima / puolikierrokset')

                                plt.barh(float(self.syvyys), width=float(self.x1),
                                         height=0.1, linewidth=1, color='b', edgecolor='k')
                                plt.barh(float(self.syvyys), width=-float(self.x2),
                                         height=0.1, linewidth=1, color='g', edgecolor='k')
                                self.figure.canvas.draw()

                        # JOS HEIJARIK (HE) --> muotoillaan chart ja arvot
                        if self.tutkimustapa == "HE":
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
                        #LAITETAAN NYT SYVYYS NÄKYVIIN ARVOILLA self.x1=-1, self.x2=1
                        if self.tutkimustapa.strip() == "P0":
                            print(lineparts)
                            if lineparts[0][:1] == "":
                                print(lineparts)
                                print("pPoraklrara")
                                self.syvyys = lineparts[1][:4]
                                #self.x2 = lineparts[2][:3]
                                #self.x1 = lineparts[3][:4]

                                self.x1 = 10
                                self.x2 = -10

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
                                self.x2 = -10
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
                                self.x2 = -10
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



        ''' with open(self.fullpath, 'r', encoding="utf-8") as textfile:
#           for line in textfile:
            line = textfile.read()
            if len(line) > 1:
                if line is self.piste   
                lineparts = line.replace('\n', '').split('\t')'''


    def draw(self):
        self.figure.canvas.draw()
        #DATA
        #t = arange(0.0, 3.0, 0.01)
        #s = sin(2 * pi * t)

        #Piirto
        #self.axes.plot(t, s, '-b')

        #x = linspace(0, 10 * pi, 100)
        #y = sin(x)

        puolikierrokset = 0
        voima = 0
        syvyys = 10
        arvo = 0

        #line1, = self.axes.plot(voima, syvyys, 'b-')

        #line1 = self.axes.bar(syvyys, arvo, height=10, color='b')
        #line1, = self.axes.plot(x, y, 'b-')

        #for i in range(10):
            #line1.set_ydata(sin(0.5 * x + phase))


            #plt.barh(i, width=puolikierrokset, height=10, color='b')
            #plt.barh(i, width=-voima, height=10, color='g')

            #plt.barh(i, width=self.x1, height=10, color='b')
            #plt.barh(i, width=-self.x2, height=10, color='g')

            #self.figure.canvas.draw()

            #puolikierrokset = puolikierrokset + 1
            #voima = voima + 2

            #plt.draw()
'''
        for phase in linspace(0, 10 * pi, 100):
            line1.set_ydata(sin(0.5 * x + phase))
            self.figure.canvas.draw() 
'''

'''
if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.draw()
    fr.Show()
    app.MainLoop()
'''