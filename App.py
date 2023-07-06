import yfinance
import os
import pandas
import datetime
import time

PATH = __file__.split('App.py')[0]
Period = {'D': ['5d', '1m'], 'W': ['1mo', '5m'], '3W': ['3mo', '1h'], 'M': ['6mo', '1h']}
list_ticker = {}
ticker = {}


class Monitor:
    def __init__(self, ticker, domain):
        self.ticker = ticker
        self.domain = domain
        self.Indicators = {
            'EMA': {
                'list': [10, 12, 20, 26, 50, 100, 150, 200],
                'data': None
            },
            'macd': {
                'data': None,
                'macd': None,
                'Single Line': None,
                'ema12': None,
                'ema26': None
            }
        }

    def merge(self, list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    def fetch_data(self, period):
        data = yfinance.download(tickers=self.ticker, period=period[0], interval=period[1])
        macd = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
        Signle_line = macd.ewm(span=9, adjust=False).mean()
        ema = [data['Close'].ewm(span=ema, adjust=False).mean() for ema in self.Indicators['EMA']['list']]
        self.Indicators['macd']['data'] = pandas.DataFrame({'MACD': macd, 'Single Line': Signle_line})
        self.Indicators['EMA']['data'] = pandas.DataFrame(
            {num: value for num, value in self.merge(self.Indicators['EMA']['list'], ema)})
        length = macd.shape[0]
        path = '{}data/{}'.format(PATH, self.ticker)
        try:
            if not os.path.exists(path):
                os.mkdir(path)
            path2 = path + '/{}'.format(period[0])
            if not os.path.exists(path2):
                os.mkdir(path2)
                self.Indicators['macd']['data'].to_csv('{}/{}'.format(path2, 'MACD.csv'))
                self.Indicators['EMA']['data'].to_csv('{}/{}'.format(path2, 'EMA.csv'))
                data.to_csv('{}/{}'.format(path2, 'data.csv'))
            else:
                length = self.Indicators['macd']['data'].shape[0]
                self.Indicators['macd']['data'][length - 1:].to_csv('{}/{}'.format(path2, 'MACD.csv'), mode='a',
                                                                    header=False)
                self.Indicators['EMA']['data'][length - 1:].to_csv('{}/{}'.format(path2, 'EMA.csv'), mode='a',
                                                                   header=False)
                data[length - 1:].to_csv('{}/{}'.format(path2, 'data.csv'), mode='a',
                                         header=False)
        except ConnectionError:
            self.to_log(pandas.DataFrame([{'Type': 'Connection error', 'detail': 'Can not connect to server'}]), 'Log',
                        'Error.csv')


def is_time():
    today = datetime.datetime.now()
    if today.strftime('%A') != 'Sunday' or today.strftime('%A') != 'Saturday':
        if today.hour in range(6, 13):
            return True
        else:
            return False


def convert_second():
    Today = datetime.datetime.now()
    if Today.hour >= 13:
        return round(23400 + (86400 - (Today.hour * 60 * 60 + Today.minute * 60 + round(Today.second, 0))))
    elif Today.hour < 6:
        return round(23400 - ((Today.hour * 60 * 60) + (Today.minute * 60) + round(Today.second, 0)))


def monitor():
    data = pandas.read_csv('Ticker.csv').to_numpy()
    list_ticker = {}
    hour = 1
    min = 1
    # while True:
    #     if is_time():
    #         start = time.perf_counter()
    #         for n in data:
    #             if n[0] not in list_ticker:
    #                 list_ticker[n[0]] = Monitor(n[0], [n[1], n[2]])
    #             else:
    #                 pass
    #         if hour == 12:
    #             for n in list_ticker.values():
    #                 n.fetch_data(Period['3W'])
    #                 n.fetch_data(Period['M'])
    #                 n.fetch_data(Period['W'])
    #             hour = 1
    #         else:
    #             for n in list_ticker.values():
    #                 n.fetch_data(Period['W'])
    #             hour += 1
    #         end = time.perf_counter()
    #         lap = end - start
    #         time.sleep(300 - lap)
    #     else:
    #         print('{}{}'.format(round(convert_second()/60), ' Minutes waiting .... back soon'))
    #         time.sleep(convert_second())


if __name__ == "__main__":
    monitor()
