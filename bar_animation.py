import matplotlib.pyplot as plt

x = []
y = []

def linesplitter(line):

    line_x = line[0]
    line_y = line[1]
    return line_x, line_y

with open("testfile.txt", "r") as testfile:

    for line in testfile:
        lineparts = line.replace('\n', '').split(',')
        line_x, line_y = linesplitter(lineparts)
        x.append(line_x)
        y.append(line_y)
    print("x-akselille: "+str(x))
    print("y-akselille: "+str(y))

fix, ax = plt.subplots()

fig = plt.barh(x, y)

plt.gca().invert_yaxis()
ax.set_xticks(range(0,100,20))


plt.show()

