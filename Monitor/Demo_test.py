from fetchdata.fetch_ticker_data import TicKer
from fetchdata.indicator import EMA_whole_cal, MACD
from Monitor.Analysis import demoIndicator
import pandas as pd
import  json
PATH = __file__.split('Monitor')[0]


def retrieve_data(ticker, period):
    path = '{}data/{}/{}'.format(PATH, ticker, period[0])
    print(path)
    try:
        data = pd.read_csv('{}/data.csv'.format(path)).set_index('Datetime')
        macd = pd.read_csv('{}/MACD.csv'.format(path)).set_index('Datetime')
        ema = pd.read_csv('{}/EMA.csv'.format(path)).set_index('Datetime')
    except:
        data = pd.read_csv('{}/data.csv'.format(path)).set_index('Unnamed: 0')
        macd = pd.read_csv('{}/MACD.csv'.format(path)).set_index('Unnamed: 0')
        ema = pd.read_csv('{}/EMA.csv'.format(path)).set_index('Unnamed: 0')

    return data, macd, ema


period = {'D': ['5d', '1m'], 'W': ['1mo', '5m'], '3W': ['3mo', '1h'], 'M': ['6mo', '60m']}
# p = period['W']
ticker = 'spy'

data, M, E = retrieve_data(ticker, period['3W'])
ema_list = [20, 50, 200]
time = pd.to_datetime(data.index)
macd = {'title': ['MACD', 'Single Line'], 'data': [M['MACD'].to_numpy(), M['Single Line'].to_numpy()],
        'domain': [-1, 2]}
ema = {'title': ema_list, 'data': [E[str(day)] for day in ema_list]}
price = {'title': ['price'], 'data': [data['Close'].to_numpy()]}
volume = {'title': ['Volume'], 'data': [data['Volume'].to_numpy()]}
adj = {'title': ['Adj Close'], 'data': [data['Adj Close'].to_numpy()]}
Indicators = [price, ema, macd]
dataForm = {'Ticker': ticker, 'Indicators': Indicators}

demoIndicator(dataForm,time)