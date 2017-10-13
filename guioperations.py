#Class which pass all the commands from gui to communication class

#TODO: hoida vastausten parsinnat täällä jos tarvitsee

class guiOperations (object):

	def __init__(self):
	"""luodaan communication olio com ja avataan yhteys sovittimelle"""
		com = communications():
		com.openConnection()


	
	"""GETTERIT"""
	
	def tiedusteleTila(self):
		"""Tiedustelee ja palauttaa tilan"""
		return = com.setCommand("STATE")
		
	def tiedusteleAika(self):		
		"""Tiedustelee ja palauttaa kalenterin ja ajan muodossa #RTC:pp.kk.vvvv-tt.mm.ss """
		return com.setCommand("RTC:?")
	
	def tiedusteleTapa(self):
	"""#?TAPA			palauta tutkimustavan #TAPA:ccc-cc:"""
		return com.setCommand("?TAPA")





	"""SETTERIT"""
	
	def asetaAika(self, aika):
	""""asettaa ajan muodossa hh:mm:sss ja palauttaa 1"""
		return com.setCommand("RTC:T:" + aika)
		
	def asetaPaiva(self, paiva):
	"""asettaa paivan muodossa pp.kk.vvvv ja palauttaa 1"""
		return com.setCommand("RTC:D" + paiva)

	def tallennaPaiva(self):
	"""#RTC:M 		PVM � tallennus KKS:ssa	"""
		return com.setCommand("RTC:M")

	def asetaHanke(self, tyonumero, hanke):
	"""#HANKE:nnn..n:		HANKE Ty�numero, hanke"""
	"""palauttaa #1"""
		return com.setCommand("HANKE:" + tyonumero + ".." + hanke)

	def asetaPiste(self, piste, kohdemuuttuja)
	"""#PISTE:ss..s:		kohdemuuttuja. palauttaa #1"""
		return com.setCommand("PISTE" + piste + ".." + kohdemuuttuja)

	def asetaTapa(self, tapa):
	"""#TAPA:ccc-cc:		Tutkimustapa (TEK-PA,TEK-HE,TEK-PH,TEK-PO ...). palauttaa (SGF-PA,SGF-HE,SGF-PH,SGF-PO ...)"""
		return com.setCommand(tapa)

	
	
	"""KUITTAUKSET"""

	def kuittaaTanko(self):
	"""#TANKO			kuittaa nostotila pois. palauttaa #1"""
		return com.setCommand("TANKO")


	
	"""TILASIIRTYMAT"""
	
	def aloitaAlkukairaus(self):
		ret
 #ALKUK:1		aloita alkukairaus



 #JATKA

!!!!



 #M-ODOTUS		mene mittauksen odotustilaan

			Tilaan tulo			< - - - - - -  	 #MIT_ODOTUS

 

 -- HW-asetus/testaus--

 #SYV-PV:nn.n:		syvyyden pulssivakion asetus

							< - - - - - -  	 #1 

 #PK-PV:nn:		puolikierrosten pulssivakion asetus

							< - - - - - -  	 #1 



 #?PULVA		anna SYV-PV ja PK-PV -vakiot

 							< - - - - - -  	 #PV:nnn.n-nn



 #?AKKU			Anna akkujen j�nnitteet, AN0.

							< - - - - - -  	 #AN0:nn.n:n.n

 #AN1N:nnn:		Aseta AN1 -kanavan nolla-arvo	< - - - - - -  	 #1

 #AN1K:n.nnn:		Aseta AN1 -kanavan kerroin	< - - - - - -  	 #1

 #?AN1S			Anna AN1 kanavan asetukset	< - - - - - -  	 #AN1:N123:K1.123

 #?AN1			Anna AN1 kanavan tieto		< - - - - - -  	 #AN1:2567:2222  (mitattu,skaalattu)



 #AN2N:nnn:		AN2 -kanavan nolla-arvo

 #AN2K:n.nnn:		AN2 -kanavan kerroin

 #?AN2S			Anna AN2 kanavan asetukset

 #?AN2D			Anna AN2 kanavan tieto



 #AN3N:nnn:		AN3 -kanavan nolla-arvo

 #AN3K:n.nnn:		AN3 -kanavan kerroin

 #?AN3S			Anna AN3 kanavan asetukset

 #?AN3D			Anna AN3 kanavan tieto



 #AN4N:nnn:		AN1 -kanavan nolla-arvo

 #AN4K:n.nnn:		AN1 -kanavan kerroin

 #?AN4S			Anna AN4 kanavan asetukset

 #?AN4D			Anna AN4 kanavan tieto



 #AN5N:nnn:		AN5 -kanavan nolla-arvo

 #AN5K:n.nnn:		AN5 -kanavan kerroin

 #?AN5S			Anna AN5 kanavan asetukset

 #?AN5D			Anna AN5 kanavan tieto







=======================

ALKUKAIRAUSTILAN:

=======================

			Tilaan tulo			< - - - - - -  	 #ALKUKAIRAUS



 #STATE			Tilan tiedustelu

							< - - - - - -  	 #MIT_ODOTUS



			nosto kuitattu KKS:ssa		< - - - - - -  	 #NOSKU



			nosto asetettu KKS:ssa		< - - - - - -  	 #NOSTO	



 #HOME			palaa alkutilaan

 #ALKUK:0		Lopeta alkukairaus. Odota mittausta

 #ALKUSYV:nnn:		kairauksen alkusyvyys, n.. cm





=======================

MITTAUKSEN ODOTUSTILA:

=======================

			Tilaan tulo			< - - - - - -  	 #MIT_ODOTUS



 #STATE			Tilan tiedustelu

   							< - - - - - -  	 #MIT_ODOTUS

 #START			aloita mittaus



 #SYVYYS:n..nn:		kairaus jatkuu syvyydess� n..nn

							< - - - - - -  	 #1

 #HOME			keskeytt�� odotustilan --> alkutilan





=======================

MITTAUSTILA:

=======================

			Tilaan tulo			< - - - - - -  	 #KAIRAUS





								KKS:n mittaussanomia mittaustilassa, kun kairaus etenee:

			HE-heijarikairauksen mittaussanoma 0.5/1 s:n v�lein	

							< - - - - - -  	 #MIT:123   15       	'syvyys/cm, heijari/isku



			TR-t�rykairauksen mittaussanoma 0.5/1 s:n v�lein	

							< - - - - - -  	 #MIT:123           	'syvyys



			PA-painokairauksen mittaussanoma 0.5/1 s:n v�lein	

							< - - - - - -  	 #MIT:123   100  25  	'syvyys, voima, puolikierros



			PO-porakonekairauksen mittaussanoma 0.5/1 s:n v�lein	

							< - - - - - -  	 #MIT:123   12  	'syvyys, aika/s



			PH-puristi/heijari -kairauksen mittaussanoma 0.5/1 s:n v�lein	

							< - - - - - -  	 #MIT:123   100  85  P	'syvyys, voima(paine MP), v��nt�/Nm, vaihe

										. . .

							< - - - - - -  	 #MIT:123   25   65  H	'syvyys, iskut, v��nt�, vaihe

										. . .





		

			HE-tallennussanoma 20cm:n v�lein (muut samoin rakenteensa mukaisesti)	

							< - - - - - -  	 #TAL:123   15  	'syvyys, heijari







 #STATE			Tilan tiedustelu

							< - - - - - -  	 #KAIRAUS

 #TANKO			lis�tangon kuittaus

							< - - - - - -  	 #1



 #STOP			kairauksen pys�ytys, odotustilaan

							< - - - - - -  	 #MIT_ODOTUS





			

									KKS -painike [x]

							< - - - - - -  	 #Kx



 #SYVYYS:n..nn:		kairaus jatkuu syvyydess� n..nn

							< - - - - - -  	 #1

 #TIMER:n		Sekuntiaskellus n=1/0 on/off

							< - - - - - -  	 #1



 #END			kairauksen lopetus, alkutilaan

			tai [END]-painike. Tablet kysyy lopetuksen syyn (luettelo)

							< - - - - - -  	 #END:123   15  'vajaan p�tk�n arvot

 							< - - - - - -  	 #ALKUTILA



=======================

NOSTOTILA:

=======================

			Tilaan tulo			< - - - - - -  	 #NOSTO



 #STATE			Tilan tiedustelu

							< - - - - - -  	 #NOSTO

 #TANKO			tangon kuittaus

							< - - - - - -  	 #NOSKU

			Kuittaus [Fn] painikkeella

							< - - - - - -  	 #NOSTO


