'''
Luokka joka toteuttaa piirtamisen KKS-datasta ja tekla-tiedostosta

Kirjastot:
numpy
matplotlib
wxpython
configparser
'''


from numpy import arange, sin, pi, linspace

import time
import os

import matplotlib.ticker
import matplotlib.pyplot as plt

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
#from matplotlib import style

matplotlib.rcParams['figure.figsize'] = (6.0, 6.0)

import wx
import configparser

class CanvasPanel(wx.Panel):
    def __init__(self, parent, gui=None):
        #wx.Panel.__init__(self, parent)
        wx.Panel.__init__(self, parent, size=wx.Size(600, 600), pos=(0,-60))

        self.figure = plt.figure()
        self.config = configparser.ConfigParser()
        self.gui = gui

        self.apu = 0

        #print(wx.DisplaySize());

        self.axes = self.figure.add_subplot(111)
        #plt.axes(xlim=(-120, 120), ylim=(0, 20))
        #plt.gca().xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        xticks = [-100,-50,0,50,100]
        xticklabels = ['100', '50', '0', '50', '100']

        #yticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        #yticklabels = ['0','5','10','15','20','25','30','35','40','45','50']

        if self.gui.syvyysvalinta == 0:
            plt.axes(xlim=(-120, 120), ylim=(0, 20))
            yticks = [0, 5, 10, 15, 20]
            yticklabels = ['0', '5', '10', '15', '20']

        elif self.gui.syvyysvalinta == 1:
            plt.axes(xlim=(-120, 120), ylim=(20, 40))
            yticks = [20, 25, 30, 35, 40]
            yticklabels = ['20','25','30','35','40']

        elif self.gui.syvyysvalinta == 2:
            plt.axes(xlim=(-120, 120), ylim=(40, 60))
            yticks = [40,45,50,55,60]
            yticklabels = ['40','45','50','55','60']

        elif self.gui.syvyysvalinta == 3:
            plt.axes(xlim=(-120, 120), ylim=(60, 80))
            yticks = [60,65,70,75,80]
            yticklabels = ['60','65','70','75','80']

        elif self.gui.syvyysvalinta == 4:
            plt.axes(xlim=(-120, 120), ylim=(80, 100))
            yticks = [80,85,90,95,100]
            yticklabels = ['80','85','90','95','100']

        else:
            plt.axes(xlim=(-120, 120), ylim=(0, 20))
            yticks = [0, 5, 10, 15, 20]
            yticklabels = ['0', '5', '10', '15', '20']

        #yticks = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
        #yticklabels = ['0','5','10','15','20','25','30','35','40','45','50'
        #    ,'55','60','65','70','75','80','85','90','95','100']

        plt.yticks(yticks, yticklabels)

        plt.xticks(xticks, xticklabels)
        #plt.subplots_adjust(left=0.1, right=0.85, bottom=0.10, wspace=0.2, hspace=0.2)


        self.canvas = FigureCanvas(self, -1, self.figure)
        self.Layout()

        #self.panel = wx.Panel(self.canvas, -1, size=(100, 500), style = wx.BORDER_RAISED)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.canvas, 0, flag=wx.ALIGN_TOP)
        #self.sizer.AddStretchSpacer(prop=15)
        #self.sizer.Add(self.canvas, 0, wx.ALL, 5)
        #self.sizer.Add(self.canvas, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        #self.Fit()

        #kopsattu vanhasta
        plt.gca().invert_yaxis()
        plt.axvline(0, color='k')

    def setNewValues(self, values):
        print(values)
        lineparts = values.replace('\n', '').split('\t')

        # JOS PAINOKAIRAUS (PA) --> muotoillaan chart ja arvot
        if self.tutkimustapa == "PA":

            if lineparts[0][:1] == "":
                # print("linepartsit: ", lineparts)
                # print ("LP_LENGTH: ", len(lineparts))

                self.syvyys = lineparts[1][:4]

                if len(lineparts) > 3 and float(self.syvyys) > self.apu:
                    self.apu = float(self.syvyys)

                    self.x2 = lineparts[2][:3]
                    self.x1 = lineparts[3][:4]

                    # print(self.syvyys, " : ", self.x1, " : ", self.x2)

                    plt.ylabel("syvyys")
                    plt.xlabel('voima / puolikierrokset')
                    if int(self.x1) != 0:
                        plt.barh(float(self.syvyys), width=float(self.x1),
                                 height=0.2, linewidth=1, color='g', edgecolor='k')
                    else:
                        plt.barh(float(self.syvyys), width=float(self.x1),
                                 height=0.2, linewidth=1, color='g', edgecolor='k')
                        plt.barh(float(self.syvyys), width=-float(self.x2),
                                 height=0.2, linewidth=1, color='b', edgecolor='k')

                        # self.figure.canvas.draw()

                else:
                    pass

        # JOS HEIJARIK (HE) --> muotoillaan chart ja arvot
        elif self.tutkimustapa == "HE":
            if lineparts[0][:1] == "":
                # print(lineparts)
                self.syvyys = lineparts[1][:4]

                if float(self.syvyys) > self.apu:
                    self.apu = float(self.syvyys)

                    self.x2 = lineparts[2][:3]
                    # self.x1 = lineparts[3][:4]

                    # print(self.syvyys, " : ", self.x2)

                    plt.ylabel("syvyys")
                    plt.xlabel('heijari / isku')

                    plt.barh(float(self.syvyys), width=float(self.x2),
                             height=0.1, linewidth=1, color='b', edgecolor='k')
                    # self.figure.canvas.draw()

        # JOS PORAK (PO) --> muotoillaan chart ja arvot
        # PORAK ANTAA DATAA MUODOSSA ['#MIT:61      0    1.7   30']
        # TAL KUITENKIN _AINA_ MUODOSSA ['#TAL:60      0    ']
        # LAITETAAN NYT SYVYYS NÄKYVIIN ARVOILLA self.x1=10, self.x2=10
        elif self.tutkimustapa == "PO":
            if lineparts[0][:1] == "":
                self.syvyys = lineparts[1][:4]

                if float(self.syvyys) > self.apu:
                    self.apu = float(self.syvyys)

                    self.x2 = lineparts[2][:3]
                    # self.x1 = lineparts[3][:4]

                    # self.x1 = 10
                    # self.x2 = 10

                    # print(self.syvyys, " : ", self.x2)

                    plt.ylabel("syvyys")
                    plt.xlabel('aika')

                    # plt.barh(float(self.syvyys), width=float(self.x1),
                    #         height=0.1, linewidth=1, color='g', edgecolor='k')

                    plt.barh(float(self.syvyys), width=float(self.x2),
                             height=0.1, linewidth=1, color='b', edgecolor='k')
                    # self.figure.canvas.draw()

        # JOS TARYK (TK) --> muotoillaan chart ja arvot
        # vain syvyytta, miten muotoillaan etta nakyy selkeästi
        # TARYKAIRAUS EI ANNA TAL SANOMAA: EI VOIDA NÄYTTÄÄ
        if self.tutkimustapa == "TR":
            if lineparts[0][:1] == "":
                # print(lineparts)
                self.syvyys = lineparts[1][:4]

                if float(self.syvyys) > self.apu:
                    self.apu = float(self.syvyys)

                    self.x2 = 10
                    self.x1 = 10

                    # print(self.syvyys, " : ", self.x2)

                    plt.ylabel("syvyys")
                    plt.xlabel('')

                    plt.barh(float(self.syvyys), width=float(self.x1),
                             height=0.1, linewidth=1, color='b', edgecolor='k')

                    plt.barh(float(self.syvyys), width=-float(self.x2),
                             height=0.1, linewidth=1, color='g', edgecolor='k')
                    # self.figure.canvas.draw()

        # JOS PURISTIHEIJARI (PH) --> muotoillaan chart ja arvot
        # Vaikuttaisi tulevan vain yksi arvo #TAL sanomassa = syvyys
        if self.tutkimustapa == "PH":
            if lineparts[0][:1] == "":
                # print(lineparts)
                self.syvyys = lineparts[1][:4]

                if float(self.syvyys) > self.apu:
                    self.apu = float(self.syvyys)

                    self.x2 = 10
                    self.x1 = 10

                    # print(self.syvyys, " : ", self.x2)

                    plt.ylabel("syvyys")
                    plt.xlabel('')
                    plt.barh(float(self.syvyys), width=float(self.x1),
                             height=0.1, linewidth=1, color='b', edgecolor='k')

                    plt.barh(float(self.syvyys), width=-float(self.x2),
                             height=0.1, linewidth=1, color='g', edgecolor='k')



    def setValues(self, hanke, piste):
        self.config.read("USECONTROL.ini")
        self.polku = self.config["DEFAULT"]["polku"]
        self.tiedosto = hanke
        self.piste = piste
        self.tutkimustapa = ""


        #print(self.polku, self.tiedosto, self.piste)

        self.fullpath = os.path.join(self.polku, self.tiedosto + ".txt")

        #if self.piste in open(self.fullpath).read():
         #   print("***LOYTYI***")
        self.muisti = False
        haluttupiste = "TY " + self.piste
        #print(haluttupiste)

        #tähän vauhtia lisää, skippaillaan linet whilessä jos väärää kamaa
        with open(self.fullpath, 'r') as textfile:
            for line in textfile:
                #print(len(line))
                if len(line) > 2:
                    #if "TY" in line:
                    if line.startswith("TY"):
                        #print("line: ", line.strip(), "haluttu: ", haluttupiste.strip());
                        #Tutkitaan onko tyonumero teklassa sama kuin annetussa hankeessa ja pisteessa
                        if line.strip() == haluttupiste.strip():
                            #print("oikea TY: ", line.strip())
                            self.muisti = True
                        else:
                            self.muisti = False
                            #print("vaara TY: ", line.strip())

                    #kun oikessa pisteessa
                    if self.muisti:
                        #tutkitaan teklasta kyseisen pisteen kairaustapa
                        #if "TT" in line:
                        if line.startswith("TT"):
                            apu = line.split(" ")
                            self.tutkimustapa = str(apu[1]).strip()
                            #print("TUTKIMUSTAPA: ", self.tutkimustapa)

                        #Splittaillaan arvot
                        lineparts = line.replace('\n', '').split('\t')

                        #JOS PAINOKAIRAUS (PA) --> muotoillaan chart ja arvot
                        if self.tutkimustapa == "PA":

                            if lineparts[0][:1] == "":
                                #print("linepartsit: ", lineparts)
                                #print ("LP_LENGTH: ", len(lineparts))

                                self.syvyys = lineparts[1][:4]

                                if len(lineparts) > 3 and float(self.syvyys) > self.apu:
                                    self.apu = float(self.syvyys)

                                    self.x2 = lineparts[2][:3]
                                    self.x1 = lineparts[3][:4]

                                    #print(self.syvyys, " : ", self.x1, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('voima / puolikierrokset')
                                    if int(self.x1) != 0:
                                        plt.barh(float(self.syvyys), width=float(self.x1),
                                                 height=0.2, linewidth=1, color='g', edgecolor='k')
                                    else:
                                        plt.barh(float(self.syvyys), width=float(self.x1),
                                                 height=0.2, linewidth=1, color='g', edgecolor='k')
                                        plt.barh(float(self.syvyys), width=-float(self.x2),
                                                 height=0.2, linewidth=1, color='b', edgecolor='k')

                                    #self.figure.canvas.draw()

                                else:
                                    pass

                        # JOS HEIJARIK (HE) --> muotoillaan chart ja arvot
                        elif self.tutkimustapa == "HE":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]

                                if float(self.syvyys) > self.apu:
                                    self.apu = float(self.syvyys)

                                    self.x2 = lineparts[2][:3]
                                    #self.x1 = lineparts[3][:4]

                                    #print(self.syvyys, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('heijari / isku')

                                    plt.barh(float(self.syvyys), width=float(self.x2),
                                             height=0.1, linewidth=1, color='b', edgecolor='k')
                                    #self.figure.canvas.draw()

                        # JOS PORAK (PO) --> muotoillaan chart ja arvot
                        #PORAK ANTAA DATAA MUODOSSA ['#MIT:61      0    1.7   30']
                        #TAL KUITENKIN _AINA_ MUODOSSA ['#TAL:60      0    ']
                        #LAITETAAN NYT SYVYYS NÄKYVIIN ARVOILLA self.x1=10, self.x2=10
                        elif self.tutkimustapa == "PO":
                            if lineparts[0][:1] == "":
                                self.syvyys = lineparts[1][:4]

                                if float(self.syvyys) > self.apu:
                                    self.apu = float(self.syvyys)

                                    self.x2 = lineparts[2][:3]
                                    #self.x1 = lineparts[3][:4]

                                    #self.x1 = 10
                                    #self.x2 = 10

                                    #print(self.syvyys, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('aika')

                                    #plt.barh(float(self.syvyys), width=float(self.x1),
                                    #         height=0.1, linewidth=1, color='g', edgecolor='k')

                                    plt.barh(float(self.syvyys), width=float(self.x2),
                                             height=0.1, linewidth=1, color='b', edgecolor='k')
                                    #self.figure.canvas.draw()

                        # JOS TARYK (TK) --> muotoillaan chart ja arvot
                        #vain syvyytta, miten muotoillaan etta nakyy selkeästi
                        #TARYKAIRAUS EI ANNA TAL SANOMAA: EI VOIDA NÄYTTÄÄ
                        if self.tutkimustapa == "TR":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]

                                if float(self.syvyys) > self.apu:
                                    self.apu = float(self.syvyys)

                                    self.x2 = 10
                                    self.x1 = 10

                                    #print(self.syvyys, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('')

                                    plt.barh(float(self.syvyys), width=float(self.x1),
                                             height=0.1, linewidth=1, color='b', edgecolor='k')

                                    plt.barh(float(self.syvyys), width=-float(self.x2),
                                             height=0.1, linewidth=1, color='g', edgecolor='k')
                                    #self.figure.canvas.draw()

                        # JOS PURISTIHEIJARI (PH) --> muotoillaan chart ja arvot
                        # Vaikuttaisi tulevan vain yksi arvo #TAL sanomassa = syvyys
                        if self.tutkimustapa == "PH":
                            if lineparts[0][:1] == "":
                                # print(lineparts)
                                self.syvyys = lineparts[1][:4]

                                if float(self.syvyys) > self.apu:
                                    self.apu = float(self.syvyys)

                                    self.x2 = 10
                                    self.x1 = 10

                                    #print(self.syvyys, " : ", self.x2)

                                    plt.ylabel("syvyys")
                                    plt.xlabel('')
                                    plt.barh(float(self.syvyys), width=float(self.x1),
                                             height=0.1, linewidth=1, color='b', edgecolor='k')

                                    plt.barh(float(self.syvyys), width=-float(self.x2),
                                             height=0.1, linewidth=1, color='g', edgecolor='k')
                                    #self.figure.canvas.draw()

    def setOldValues(self, data, kairaustapa):

        if kairaustapa == "PA":

            #if self.syvyys[:-1] < 20:

            floatsyvyys = []
            floatvoima = []
            floatpuolikierrokset = []
            for i in data:
                floatsyvyys.append(float(i[0]))
                floatvoima.append(float(i[1]))
                floatpuolikierrokset.append(float(i[2]))

            plt.ylabel("syvyys")
            plt.xlabel('voima / puolikierrokset')
            s = 0
            while s < len(floatsyvyys):
                if floatvoima[s] != 0:
                    plt.barh(floatsyvyys[s], width=-floatvoima[s],
                             height=0.2, linewidth=1, color='b', edgecolor='k')
                    s = s + 1
                else:
                    plt.barh(floatsyvyys[s], width=-floatvoima[s],
                             height=0.2, linewidth=1, color='b', edgecolor='k')
                    plt.barh(floatsyvyys[s], width=floatpuolikierrokset[s],
                             height=0.2, linewidth=1, color='g', edgecolor='k')
                    s = s + 1

        elif kairaustapa == "HE":
            floatsyvyys = []
            floatisku = []
            for i in data:
                floatsyvyys.append(float(i[0]))
                floatisku.append(float(i[1]))

            plt.ylabel("syvyys")
            plt.xlabel('heijari')
            s = 0
            while s < len(floatsyvyys):
                    plt.barh(floatsyvyys[s], width=floatisku[s],
                             height=0.2, linewidth=1, color='b', edgecolor='k')
                    s = s + 1

        elif kairaustapa == "PO":

            floatsyvyys = []
            floattnknopeus = []
            for i in data:
                floatsyvyys.append(float(i[0]))
                floattnknopeus.append(float(i[1]))

            plt.ylabel("syvyys")
            plt.xlabel('tunkeutumisnopeus')

            s = 0
            while s < len(floatsyvyys):
                    plt.barh(floatsyvyys[s], width=-floattnknopeus[s],
                             height=0.2, linewidth=1, color='b', edgecolor='k')

                    s = s + 1

        elif kairaustapa == "TR":

            plt.axes(xlim=(-10, 10), ylim=(0, 20))
            plt.gca().invert_yaxis()
            floatsyvyys = []
            for i in data:
                floatsyvyys.append(float(i[0]))
            syvin = floatsyvyys.__getitem__(len(floatsyvyys)-1)
            matalin = floatsyvyys[0]

            self.axes.xaxis.set_major_formatter(plt.NullFormatter())
            plt.axis('off')

            plt.text(0.5,0.5,"{}".format(matalin))
            plt.text(0.5,syvin+0.5,"{}(m)".format(syvin))
            plt.bar(x=0,height=syvin, width=0.0001, color='b', edgecolor='k')


        elif kairaustapa == "PH":

            floatsyvyys = []
            floatvoima = []
            floatvaanto = []
            for i in data:
                floatsyvyys.append(float(i[0]))
                floatvoima.append(float(i[1]))
                floatvaanto.append(float(i[2]))

            plt.ylabel("syvyys")
            plt.xlabel('voima / vääntö')
            plt.gca().xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
            xticks = [-100, -50, 0, 50, 100]
            xticklabels = ['100', '50', '0', '50', '100']
            plt.xticks(xticks, xticklabels)

            s = 0
            while s < len(floatsyvyys):
                    plt.barh(floatsyvyys[s], width=-floatvoima[s],
                             height=0.2, linewidth=1, color='b', edgecolor='k')
                    plt.barh(floatsyvyys[s], width=floatvaanto[s],
                             height=0.2, linewidth=1, color='g', edgecolor='k')
                    s = s + 1

        else:
            return None


    def draw(self):
        #self.figure.canvas.draw()
        self.canvas.draw()



