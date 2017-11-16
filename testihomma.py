#!/usr/bin/env python
import numpy as np
import wx
import gui
import collections
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
 FigureCanvasWxAgg as FigCanvas,\
 NavigationToolbar2WxAgg as NavigationToolbar
class MyFrameSub(gui.MainFrame):
 def showpanel(self,p):
  for K in self.labels:
   self.buttons[K].Hide()
  self.buttons[p].Show()
  self.Layout()
 def clickbutton(self,event):
  btn=event.GetEventObject().GetLabelText()
  self.showpanel(btn)
  event.Skip()
 def __init__(self,parent):
  self.labels=collections.OrderedDict([("TIEDOSTO","red"),("PISTE","blue"),("OHJELMA","black"),("HALLINTA","orange"),("MAALAJI","yellow")])
  self.menuButton={}
  self.buttons={}
  gui.MainFrame.__init__(self,parent)
  self.CreatePlot()
  self.showpanel('TIEDOSTO')
  return
 def CreatePlot(self):
  self.figure=Figure(figsize=(7,8),dpi=80,frameon=False)
  self.axes=self.figure.add_axes([0,0,1,1])
  x=np.arange(0,6,.01)
  y=np.sin(x ** 3) * np.exp(-x)
  self.axes.plot(x,y)
  self.canvas=FigCanvas(self.buttons["TIEDOSTO"],wx.ID_ANY,self.figure)
  size=self.buttons["TIEDOSTO"].GetSize()
  self.SetMinSize((size[0] / 1,size[1] / 1))
  return
 def OnCalculate(self,event):
  print ("%s" % self.m_value1.GetValue())
  return
app=wx.App()
window=MyFrameSub(None)
window.Show(True)
app.MainLoop()
