# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct 18 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Vatjus 3000", pos = wx.DefaultPosition, size = wx.Size( 540,960 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.fileButton = wx.Button( self, wx.ID_ANY, u"TIEDOSTO", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer2.Add( self.fileButton, 1, wx.ALL, 5 )
		
		self.pisteButton = wx.Button( self, wx.ID_ANY, u"PISTE", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer2.Add( self.pisteButton, 1, wx.ALL, 5 )
		
		self.ohjelmaButton = wx.Button( self, wx.ID_ANY, u"OHJELMA", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer2.Add( self.ohjelmaButton, 1, wx.ALL, 5 )
		
		self.ctrlButton = wx.Button( self, wx.ID_ANY, u"HALLINTA", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer2.Add( self.ctrlButton, 1, wx.ALL, 5 )
		
		self.maaButton = wx.Button( self, wx.ID_ANY, u"MAALAJI", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer2.Add( self.maaButton, 1, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.fileIndikaattori = wx.StaticText( self, wx.ID_ANY, u"FILE: 1234A579-JK", wx.Point( -1,-1 ), wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self.fileIndikaattori.Wrap( -1 )
		self.fileIndikaattori.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.fileIndikaattori.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer5.Add( self.fileIndikaattori, 1, wx.ALL|wx.EXPAND, 16 )
		
		
		bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"PISTE: PK 1234", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_staticText10, 1, wx.ALL, 16 )
		
		self.nayttoButton = wx.Button( self, wx.ID_ANY, u"NÄYTTÖ", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer6.Add( self.nayttoButton, 1, wx.ALL, 5 )
		
		self.tankoButton = wx.Button( self, wx.ID_ANY, u"TANKO", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer6.Add( self.tankoButton, 1, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_panel3.SetMaxSize( wx.Size( 540,-1 ) )
		
		bSizer7.Add( self.m_panel3, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		gSizer2 = wx.GridSizer( 2, 5, 0, 0 )
		
		self.syvyys_Label = wx.StaticText( self, wx.ID_ANY, u"SYVYYS", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.syvyys_Label.Wrap( -1 )
		self.syvyys_Label.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.syvyys_Label, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.voimaLabel = wx.StaticText( self, wx.ID_ANY, u"VOIMA", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.voimaLabel.Wrap( -1 )
		self.voimaLabel.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.voimaLabel, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.puolikLabel = wx.StaticText( self, wx.ID_ANY, u"PUOLIK", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.puolikLabel.Wrap( -1 )
		self.puolikLabel.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.puolikLabel, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.maaLabel = wx.StaticText( self, wx.ID_ANY, u"MAALAJI", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.maaLabel.Wrap( -1 )
		self.maaLabel.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.maaLabel, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.iskuLabel = wx.StaticText( self, wx.ID_ANY, u"ISKU", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.iskuLabel.Wrap( -1 )
		self.iskuLabel.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.iskuLabel, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.syvyysArvo = wx.StaticText( self, wx.ID_ANY, u"295", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.syvyysArvo.Wrap( -1 )
		self.syvyysArvo.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.syvyysArvo, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.voimaArvo = wx.StaticText( self, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.voimaArvo.Wrap( -1 )
		self.voimaArvo.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.voimaArvo, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.puolikArvo = wx.StaticText( self, wx.ID_ANY, u"13", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.puolikArvo.Wrap( -1 )
		self.puolikArvo.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.puolikArvo, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.maaArvo = wx.StaticText( self, wx.ID_ANY, u"SaSi", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.maaArvo.Wrap( -1 )
		self.maaArvo.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.maaArvo, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.iskuArvo = wx.StaticText( self, wx.ID_ANY, u"OFF", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.iskuArvo.Wrap( -1 )
		self.iskuArvo.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		gSizer2.Add( self.iskuArvo, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer7.Add( gSizer2, 0, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer7, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

