import yfinance as yf
import pandas as pd
from fetchdata import Time_period as T
import datetime

class TicKer:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_ticker_data_defautl(self):
        return yf.download(self.ticker, T.date_by_month(), T.get_currrent_day())

    def get_current_price(self):
        # return yf.download(self.ticker, period='1m', interval='1m')
        data = yf.download(self.ticker, T.get_date(), T.get_currrent_day())
        current_prince = pd.DataFrame(data.to_numpy(),index=[T.get_timestamp(datetime.datetime.now())], columns=data.columns.to_numpy())
        return current_prince

    def get_price_by_period(self, period, interval):
        return yf.download(tickers=self.ticker, period=period, interval=interval)


