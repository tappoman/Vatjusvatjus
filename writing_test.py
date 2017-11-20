import random

testitiedosto = open("testfile.txt", "w")

def luo_satunnaiset_puolikierrokset():
    satunnaispuolikierrokset =  random.randint(0, 100)
    return satunnaispuolikierrokset


def luo_satunnaisvoima():
    satunnaisarvo = random.randint(0,5)
    if satunnaisarvo >= 4:
        satunnaisvoima = random.randint(0,50)
        return satunnaisvoima
    else:
        return False


arvojen_maara = range(15)
syvyys_alku = 20

for i in arvojen_maara:
    puolikierrokset_kirjoita = luo_satunnaiset_puolikierrokset()
    voima_kirjoita = luo_satunnaisvoima()
    if voima_kirjoita == False:
        print("syvyys:"+str(syvyys_alku)+",","toinen_arvo:"+str(puolikierrokset_kirjoita)+'\n')
        testitiedosto.write(str(syvyys_alku))
        testitiedosto.write("," + str(puolikierrokset_kirjoita) + '\n')
        syvyys_alku = syvyys_alku + 20

    else:
        print("syvyys:" + str(syvyys_alku) + ",", "puolikierrokset:" + str(puolikierrokset_kirjoita)+ ",", "voima:" + str(voima_kirjoita) + '\n')
        testitiedosto.write(str(syvyys_alku))
        testitiedosto.write(","+str(puolikierrokset_kirjoita))
        testitiedosto.write(","+str(voima_kirjoita)+'\n')
        syvyys_alku = syvyys_alku+20


testitiedosto.close()
