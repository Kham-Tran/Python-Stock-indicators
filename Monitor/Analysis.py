import matplotlib.pyplot as plt
import datetime


def trimData(data):
    for row in data.iterrows():
        print(type(row[0]))


def cutData(data, begin, end):
    arr = []
    for n in data:
        if n == begin:
            arr.append(data.index(n))
        if n == end:
            arr.append(data.index(n))
            break
    return arr


def drawIndicator(ax, data, time):
    for n in range(len(data['title'])):
        ax.plot(time, data['data'][n])
    if data['title'][0] == 'MACD':
        ax.axhline(y=0, color='k')
        ax.axhline(y=data['domain'][0], color='r')
        ax.axhline(y=data['domain'][1], color='r')
    ax.legend(tuple(tuple(data['title'])), bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)


def demoIndicator(dataform, time):
    fig, axs = plt.subplots(len(dataform['Indicators']))
    fig.suptitle(dataform['Ticker'], fontsize=20)
    for n in range(0, len(dataform['Indicators'])):
        drawIndicator(axs[n], dataform['Indicators'][n], time)
    plt.subplots_adjust(bottom=0.04, right=0.952, top=0.976, left=0.036)
    plt.show()
