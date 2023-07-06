import matplotlib.pyplot as plt
import pandas as pd
from fetchdata.fetch_ticker_data import TicKer
from fetchdata.indicator import EMA_whole_cal, EMA_current_Cal, MACD, MACD_current

class Demonstation:
    def __init__(self):
        self.figure, self.ax = plt.subplots(2)

    def graph_MACD(self, DATA, num):
        MACD = DATA['MACD'].to_numpy()
        single_line = DATA['Single Line'].to_numpy()
        time = pd.to_datetime(DATA.index)
        self.ax[num].plot(time, MACD, color='b', label='MACD')
        self.ax[num].plot(time, single_line, color='g', label='Single Line')
        self.ax[num].axhline(y=0, color='k')
        self.ax[num].axhline(y=1, color='r')
        self.ax[num].axhline(y=-1, color='r')
        self.ax[num].axhline(y=2, color='y')
        self.ax[num].axhline(y=-2, color='y')
        self.ax[num].legend(('MACD', 'Single Line'), bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    def graph_EMA(self, DATA, EMA_list, num):
        time = pd.to_datetime(DATA[0].index)
        for ema in DATA:
            self.ax[num].plot(time, ema)
        self.ax[0].legend(tuple(EMA_list), bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    def draw_axe(self, ticker, data, ema_list, ax0, ax1):
        self.clean_fig()
        DATA = TicKer(ticker).get_price_by_period(data[0], data[1])
        EMA = [EMA_whole_cal(DATA['Close'], days) for days in ema_list]
        macd, ema_12, ema_26 = MACD(DATA['Close'])
        self.graph_EMA(EMA, ema_list, ax0)
        self.graph_MACD(macd, ax1)

    def draw_price(self, ticker, data, ax0, ax1):
        DATA = TicKer(ticker).get_price_by_period(data[0], data[1])
        time = pd.to_datetime(DATA.index)
        macd, ema_12, ema_26 = MACD(DATA['Close'])
        self.ax[ax0].plot(time, DATA['Close'], color='g')
        self.ax[ax0].legend(('$'), bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
        self.ax[ax1].plot(time,DATA['Volume'], color='r')
        self.ax[ax1].legend('Volume', bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    def cross_detector(self, data):
        p1 = data[0:1].to_numpy()
        p2 = data[1:2].to_numpy()
        if p1[0] > p2[0] and p1[1] < p2[1] or p1[0] < p2[0] and p1[1] > p2[1]:
            return True
        else:
            return False

    def observe(self, macd, ema, ema_list, num, ax0, ax1):
        self.clean_fig()
        self.graph_MACD(macd[num:], ax1)
        EMA = [n[num:] for n in ema]
        self.graph_EMA(EMA, ema_list, ax0)

    def clean_fig(self):
        self.ax[0].cla()
        self.ax[1].cla()

    def show_graph(self, time):
        plt.pause(time)

    def title(self, ticker):
        self.figure.suptitle(ticker, fontsize=20)

    def close_graph(self):
        plt.close(self.figure)

