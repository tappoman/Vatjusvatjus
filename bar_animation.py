import matplotlib.pyplot as plt
from matplotlib import style
import gui

style.use('fivethirtyeight')


fig= plt.Figure()
ax = plt.axes(xlim=(-120, 250), ylim=(0, 350))
plt.gca().invert_yaxis()
plt.axvline(0, color='k')
plt.ylabel("syvyys")
plt.xlabel('voima / puolikierrokset')
plt.subplots_adjust(left = 0.12, bottom = 0.12, wspace = 0.2, hspace = 0.2)


def graafi(syvyys, voima, puolikierrokset):

    p = 0
    for i in syvyys:
        ax.barh(syvyys[p], width=puolikierrokset[p], height=10, color='b')
        ax.barh(syvyys[p], width=-voima[p], height=10, color='g')

def main(data):

    l_syvyys = []
    l_voima = []
    l_puolikierrokset = []
    l_syvyys.append(data.haesyvyys())
    l_voima.append(data.haevoima())
    l_puolikierrokset.append(data.haepuolikierrokset())
    print("{}{}{}".format(l_syvyys, l_voima, l_puolikierrokset))
    graph = graafi(l_syvyys, l_voima, l_puolikierrokset)
    plt.show()

if __name__ == '__main__':
    main(gui.TiedonKasittely)