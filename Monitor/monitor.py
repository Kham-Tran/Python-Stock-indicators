from fetchdata.fetch_ticker_data import TicKer
import pandas as pd
from fetchdata.indicator import EMA_whole_cal, EMA_current_Cal, MACD, MACD_current
from fetchdata import Time_period as T
import datetime
import os

EMA_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250]


class monitor:
    def __init__(self, ticker, domain):
        self.ticker = ticker
        self.isOn = False
        self.tickerObject = TicKer(self.ticker)
        self.indicators = {}
        self.prepare_data = {}
        self.data = None
        self.is_updated = False
        self.domain = domain
        self.time = None
        self.default_ema = [20,50,200]

    def get_period(self):
        return self.time

    def set_ema(self, ema):
        self.default_ema = ema

    def set_on_off(self, command):
        self.isOn = command

    def merge(self, list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    def cross_detector(self, data):
        p1 = data[0:1].to_numpy()[0]
        p2 = data[1:2].to_numpy()[0]
        if p1[0] > p1[1] and p2[0] < p2[1]:
            return True, 'Down Trend'
        elif p1[0] < p1[1] and p2[0] > p2[1]:
            return True, 'Up Trend'
        else:
            return False, None

    def to_log(self, data, name):
        path = '../data/{}/log'.format(self.ticker)
        if not os.path.exists(path):
            os.mkdir(path)
            data.to_csv('{}/{}'.format(path, name), mode='a', header=False)
        else:
            data.to_csv('{}/{}'.format(path, name), mode='a', header=False)

    def trade_signal(self):
        length = self.indicators['MACD'].shape[0]
        MACD = self.indicators['MACD'][length - 2:]
        EMA = self.indicators['EMA'][self.default_ema][length - 2:]
        signal_M, Trend_M = self.cross_detector(MACD)
        signal_E, Trend_E = self.cross_detector(EMA)
        if signal_M:
            MACD.insert(2, "Trend", [Trend_M, Trend_M], True)
            self.to_log(MACD, 'log_MACD.csv')
        if signal_E:
            EMA.insert(2, "Trend", [Trend_E, Trend_E], True)
            self.to_log(EMA, 'log_EMA.csv')

    def EMA(self, list_ema):
        ema = [EMA_whole_cal(self.data['Close'], number) for number in list_ema]
        return pd.DataFrame({num: value for num, value in self.merge(list_ema, ema)})

    def single_indicators(self, price, list_ema, EMA, ema12, ema26, macd):
        current_macd, ema_12, ema_26 = MACD_current(price, ema12, ema26, macd['Single Line'].to_numpy()[0])
        current_ema = [EMA_current_Cal(price, days, ema) for days, ema in self.merge(list_ema, EMA)]
        ema = self.indicators['EMA']
        macd = self.indicators['MACD']
        self.indicators = {'EMA': pd.concat(
            [ema, pd.DataFrame([current_ema], index=[T.get_timestamp(datetime.datetime.now())], columns=ema.columns)]),
            'MACD': pd.concat([macd, current_macd])}
        return {'list ema': list_ema, 'ema': current_ema, 'ema 12': ema_12,
                'ema 26': ema_26,
                'macd': current_macd}

    def update_indicator(self, prepare_data):
        row = self.tickerObject.get_current_price()
        self.data = pd.concat([self.data, row])
        prepare_data['price'] = row['Close'].to_numpy()[0]
        return self.single_indicators(prepare_data['price'], prepare_data['list ema'], prepare_data['ema'],
                                      prepare_data['ema 12'], prepare_data['ema 26'],
                                      prepare_data['macd'])

    def init_monitoring(self, prepare_data, time):
        self.data = self.tickerObject.get_price_by_period(time[0], time[1])
        ema = self.EMA(EMA_list)
        macd, ema12, ema26 = MACD(self.data['Close'])
        self.indicators = {'EMA': ema, 'MACD': macd}

        return {'list ema': EMA_list, 'ema': ema[ema.shape[0] - 1:].to_numpy()[0],
                'ema 12': ema12[macd.shape[0] - 1:].to_numpy()[0],
                'ema 26': ema26[macd.shape[0] - 1:].to_numpy()[0],
                'macd': macd[macd.shape[0] - 1:]}

    def get_from_file(self):
        path = '../data/{}'.format(self.ticker)
        return pd.read_csv('{}/MACD.csv'.format(path)), pd.read_csv('{}/EMA.csv'.format(path)), pd.read_csv(
            '{}/data.csv'.format(path))

    def to_file_data(self):
        path = '../data/{}'.format(self.ticker)
        if not os.path.exists(path):
            os.mkdir(path)
        path2 = path+'/{}'.format(self.time[0])
        if not os.path.exists(path2):
            os.mkdir(path2)
            self.indicators['MACD'].to_csv('{}/{}/MACD.csv'.format(path,self.time[0]), index_label='Date')
            self.indicators['EMA'].to_csv('{}/{}/EMA.csv'.format(path,self.time[0]), index_label='Date')
            self.data.to_csv('{}/{}/data.csv'.format(path,self.time[0]), index_label='Date')
        else:
            length = self.indicators['MACD'].shape[0]
            MACD = self.indicators['MACD'][length - 1:]
            EMA = self.indicators['EMA'][length - 1:]
            data = self.data[length - 1:]
            MACD.to_csv('{}/{}/MACD.csv'.format(path,self.time[0]), mode='a', index_label='Date', header=False)
            EMA.to_csv('{}/{}/EMA.csv'.format(path,self.time[0]), mode='a', index_label='Date', header=False)
            data.to_csv('{}/{}/data.csv'.format(path,self.time[0]), mode='a', index_label='Date', header=False)

    def get_ticker(self):
        return self.ticker

    def get_data(self):
        return self.indicators['MACD'], self.indicators['EMA'], self.data

    def alert(self):
        length = self.indicators['MACD'].shape[0]
        MACD = self.indicators['MACD'][length - 1:]
        if self.domain[1] <= float(MACD['MACD']) or float(MACD['MACD']) <= self.domain[0]:
            print(self.ticker + " out of domain")

    def monitoring(self, period):
        self.time = period
        path = '../data/{}'.format(self.ticker)
        # if not self.isOn:
        #     self.set_on_off(True)
        #     try:
        #         self.prepare_data = self.init_monitoring(self.prepare_data, self.time)
        #     except:
        #         print('Could not INIT data')
        # else:
        #     try:
        #         self.prepare_data = self.update_indicator(self.prepare_data)
        #     except:
        #         print('Could not UPDATE data')
        #         self.prepare_data = self.init_monitoring(self.prepare_data, self.time)
        self.prepare_data = self.init_monitoring(self.prepare_data, self.time)
        self.to_file_data()
        self.trade_signal()
        self.alert()
        self.time = None
