import matplotlib.pyplot as plt



def plotOccBar(listOfTimes):

    for l in range(len(listOfTimes)):
        ax = plt.axes()
        ax.bar(l, listOfTimes[l], align='center', width=0.5)

    plt.title("Novas Células Ocupadas a cada Ano")
    plt.ylabel("Células ocupadas")
    plt.xlabel("Ano")
    plt.xticks(range(0, 100+1, 10))
    plt.show()


def plot1(data_acc, steps, label, tickX, tickY):
    c = range(len(data_acc))
    fig = plt.figure()
    limit = int(max(data_acc) + int(0.2*max(data_acc)))
    fig.add_subplot(122)
    ax = plt.axes()
    ax.plot(c, data_acc, 'k')
    plt.yticks(range(0, limit, tickY))
    plt.xticks(range(0, steps+1, tickX))
    plt.title(label)
    plt.ylabel("Células ocupadas")
    plt.xlabel("Ano")
    plt.grid()
    plt.show()
