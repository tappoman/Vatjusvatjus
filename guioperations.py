#Class which pass all the commands from gui to communication class

#TODO: hoida vastausten parsinnat täällä jos tarvitsee:
#KUUNNELLESSA HEADERIIN TULEE VASTAUS JOITA PARSITAAN 
#(NÄMÄ ON TOISINSANOEN KOMENTOJA JOITA ANNETAAN KKS:LTÄ JA NIIHIN PITÄÄ REAGOIDA):
#NOSTO, #KAIRAUS, MITÄ?

class guiOperations (object):

	def __init__(self):
	"""luodaan communication olio com ja avataan yhteys sovittimelle"""
		com = communications():
		com.openConnection()


	
	"""YLEISKÄSKYT"""
	
	def asetaViive(self): 
		"""Aseta viive 1-99 ms, jonka jälkeen vasta tablet (=SOVITIN???)= lähettää vastauksensa. Palauttaa #1"""
		return com.setCommand("DELAY")
		
	def tiedusteleTila(self):
		"""Tiedustelee ja palauttaa tilan"""
		return = com.setCommand("STATE")
		
	def tiedusteleAika(self):		
		"""Tiedustelee ja palauttaa kalenterin ja ajan muodossa #RTC:pp.kk.vvvv-tt.mm.ss """
		return com.setCommand("RTC:?")

	def asetaAika(self, aika):
	""""asettaa ajan muodossa hh:mm:sss ja palauttaa 1"""
		return com.setCommand("RTC:T:" + aika)
		
	def asetaPaiva(self, paiva):
	"""asettaa paivan muodossa pp.kk.vvvv ja palauttaa 1"""
		return com.setCommand("RTC:D" + paiva)

	#def tallennaPaiva(self):
	"""#RTC:M 		PVM � tallennus KKS:ssa	"""
	#	return com.setCommand("RTC:M")


	
	"""PISTEEN ALUSTUS""
	
	def asetaHanke(self, tyonumero, hanke):
	"""#HANKE:nnn..n:		HANKE Ty�numero, hanke"""
	"""palauttaa #1"""
		return com.setCommand("HANKE:" + tyonumero + ".." + hanke)

	def asetaPiste(self, piste)
	"""#PISTE:ss..s:		kohdemuuttuja. palauttaa #1"""
		return com.setCommand("PISTE" + piste)

	def asetaTapa(self, tapa):
	"""#TAPA:ccc-cc:		Tutkimustapa (TEK-PA,TEK-HE,TEK-PH,TEK-PO ...). palauttaa (SGF-PA,SGF-HE,SGF-PH,SGF-PO ...)"""
		return com.setCommand(tapa)

	def tiedusteleTapa(self):
	"""#?TAPA			palauta tutkimustavan #TAPA:ccc-cc:"""
		return com.setCommand("?TAPA")
	
	
	
	"""KAIRAUKSEN VALMISTELU"""

	def kuittaaTanko(self):
	"""#TANKO			kuittaa tila pois. palauttaa #1"""
		return com.setCommand("TANKO")

	def aloitaAlkukairaus(self):
		"""aloittaa alkukairauksen, palauttaa #alkukairaus
		SIIRTYY ALKUKAIRAUSTILAAN -->
		TÄYTYY ALOITTAA KUUNTELU GUI:N PUOLELTA guioperations.kuunteleAlkukairausta() --> POLLAUSVÄLI 1S.
		PARSITAAN MYÖS #NOSKU #NOSTO"""
		return com.setCommand("ALKUK:1")
		
	def aloitaOdotustila(self):
		"""menee mittauksen odotustilaan josta jatketaan kairausta. Palauttaa #MIT_ODOTUS"""
		return com.setCommand("M-ODOTUS")
		
	
	"""ALKUKAIRAUSTILA"""
	
	"""Tilaan tulo	 				< - - - - - -    #ALKUKAIRAUS 
	Alkukairaussyvyys 1s välein. 	< - - - - - -    #SYV:nnn
	Nosto asetettu KKS:ssa.			< - - - - - -    #NOSTO
	Nosto kuitattu KKS:ssa.			< - - - - - -    #NOSKU"""
		
	def kuunteleAlkukairausta(self):
		return com.readValues()
		
	def asetaAlkusyvyys(self, syvyys):
		return com.setCommand("SYV:" + syvyys)
	
	def aloitaAlkutila(self):
		return com.setCommand("HOME")	
	
	def lopetaAlkukairaus(self):
		"""lopettaa alkukairauksen ja siirtyy kairauksen odotustilaan (Saattaa palauttaa MIT_ODOTUS???)"""
		return com.setCommand("ALKUK:0")
	
	
	""""MITTAUKSEN ODOTUSTILA"""
	def asetaKairaussyvyys(self, syvyys):
		return com.setCommand("SYVYYS:" + syvyys + ":")
		
	def aloitaMittaustila(self):
	"""aloittaa mittauksen --> SIIRTYY MITTAUSTILAAN (MITTAUSTILA-2???)"""
		return com.setCommand("START"):
		
	
	"""MITTAUSTILA-2"""
	def pysaytaKairaus(self):
	"""lopettaa kairauksen ja siirtyy odotustilaan"""
		return com.setCommand"STOP")
	
	def asetaSekuntiaskellus(self, askellus):
		return com.setCommand("TIMER:" + askellus + ":")
		
	def lopetaMittaus
		
	"""MITTAUSTILA-1"""
	def aloitaKairaus(self):
		return com.setCommand("KAIRAUS")
	
	def kuunteleKairausta(self):
		return com.readValues()
	
	def lopetaKairaus(self):
	"""lopettaa kairauksen ja palaa alkutilaan
	Palauttaa #END:123 15 vajaan pätkän arvot (mitvit???) ja #ALKUTILA"""
		return com.setCommand("END")
	
	

	"""NOSTOTILA VAIKUTTAA HIEMAN SEKAVALTA"""
	"""tilaan tulaan KKS-Komennolla, lähettää headerin #NOSTO. TULEEKO GUI:n PUOLELLE SIIRTYMÄÄ???"""
"""#STATE 	Tilan tiedustelu.		< - - - - - -   #NOSTO
 #TANKO 	Tangon kuittaus.		(< - - - - - -   #NOSKU)
			Jatkuu kairaustilana. 	< - - - - - -   #MITTAUSTILA
									
Kuittaus [Fn] painikkeella
Jatkuu kairaustilana.
(< - - - - -    #NOSKU)
< - - - - - -   #MITTAUSTILA
 """
