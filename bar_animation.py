import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

puolikierrokset =  []
voima = []
syvyys =  []
fig, ax = plt.subplots()

# jaetaan tuleva data akseleille
def linesplitter(line):

        linex = int(line[0])
        liney = int(line[1])
        liney2 = int(line[2])
        if liney2 is None:
            liney2 = 0
            return linex, liney, liney2
        else:
            return linex, liney, liney2

# höpöhöpöä, ehkä käyttistä kun saadaan oikeannäköstä dataa
# def get_values(i):
#     if voima[i] != 0:
#         return syvyys[i], voima[i]
#     else:
#         return syvyys[i], puolikierrokset[i]

# luetaan data tekstitiedostosta ja lisätään piirrettäviin arvoihin
def read_values():
    with open("testfile.txt", "r") as testfile:
        for line in testfile:
            if len(line) > 1:
                lineparts = line.replace('\n', '').split(',')
                if len(lineparts) == 2:
                    lineparts.append(0)
                line_s, line_pk, line_v = linesplitter(lineparts)
                puolikierrokset.append(line_pk)
                voima.append(-line_v)
                syvyys.append(line_s)

        #print("syvyys: " + str(syvyys))
        #print("pkierr: " + str(puolikierrokset))
        #print("voima: " + str(voima))

# vanha datan piirto, akselit toimii paremmin kun horisontaalisella
# def chart_setup_vertical():
#     #fig, ax = plt.subplots()
#
#     # x_labels = range(0, 500, 20)
#     ax.axhline(syvyys == 0, color='k')
#
#     plt.xlabel('syvyys')
#     plt.ylabel('voima           puolikierrokset')
#
#     # ax.set_xticklabels(syvyys, rotation = 90)
#     ax.xaxis.label.set_rotation(90)
#     for label in ax.xaxis.get_ticklabels():
#         label.set_rotation(90)
#     for label in ax.yaxis.get_ticklabels():
#         label.set_rotation(90)
#     plt.subplots_adjust(left = 0.12, bottom = 0.3, right = 0.94, top = 0.90, wspace = 0.2, hspace = 0)


def chart_setup_horizontal():

    plt.gca().invert_yaxis()
    ax.axvline(syvyys == 0, color='k')
    plt.ylabel('syvyys           ')
    plt.xlabel('voima        puolikierrokset')
    ax.yaxis.label.set_rotation(360)
    plt.subplots_adjust(left = 0.25, bottom = 0.15, right = 0.94, top = 0.90, wspace = 0.2, hspace = 0.2)

# datan piirto ilman animaatiota
# def draw_graph():
#
#     p = 0
#     for s in syvyys:
#         if voima[p] != 0:
#             ax.bar(syvyys[p], voima[p], width=5, align='center', color='g', label='voima')
#             p = p + 1
#         else:
#             ax.bar(syvyys[p], puolikierrokset[p], width=5, align='center', color='b', label='puolikierrokset')
#             p = p + 1

#datan animointi, arvo i= intervalli joka annetaan mainissa.
def animate_horizontal(i):

    read_values()
    p = 0
    for s in syvyys:
        if voima[p] != 0:
            ax.barh(syvyys[p], width=voima[p], height=10, color='g')
            p = p + 1
        else:
            ax.barh(syvyys[p], width=puolikierrokset[p], height=10, color='b')
            p = p + 1


# vanha animointi, ehkä käyttistä ehkä ei
# def animate_vertical(i):
#
#     read_values()
#     p = 0
#     for s in syvyys:
#         if voima[p] != 0:
#
#             ax.bar(syvyys[p], voima[p], width=5, align='center', color='g')
#             p = p + 1
#         else:
#             ax.bar(syvyys[p], puolikierrokset[p], width=5, align='center', color='b')
#             p = p + 1


def main():

    #vertical
    #chart_setup_vertical()
    #anim = animation.FuncAnimation(fig, animate_vertical, interval=2000)


    #horizontal
    chart_setup_horizontal()
    anim = animation.FuncAnimation(fig, animate_horizontal, interval=2000)
    plt.show()


main()