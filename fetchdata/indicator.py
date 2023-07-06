import pandas as pd
from fetchdata import Time_period as T
import datetime


def EMA_current_Cal(price, days, EMA_yesterday):
    constant = 2 / (1 + days)
    return price * constant + EMA_yesterday * (1 - constant)


def EMA_whole_cal(data, days):
    EMA = data.ewm(span=days, adjust=False).mean()
    return EMA


def MACD(data):
    EMA_26 = EMA_whole_cal(data, 26)
    EMA_12 = EMA_whole_cal(data, 12)
    macd = EMA_12 - EMA_26
    Single_line = EMA_whole_cal(macd, 9)
    return pd.DataFrame({'MACD': macd, 'Single Line': Single_line}), EMA_12, EMA_26


def MACD_current(price, ema12, ema26, single_line):
    EMA_26 = EMA_current_Cal(price, 26, ema26)
    EMA_12 = EMA_current_Cal(price, 12, ema12)
    current_MACD = EMA_12 - EMA_26
    Single_line_current = EMA_current_Cal(current_MACD, 9, single_line)
    return pd.DataFrame({'MACD': [current_MACD], 'Single Line': [Single_line_current]},
                        index=[T.get_timestamp(datetime.datetime.now())]), EMA_12, EMA_26


def is_crossed(data):
    lines = data.to_numpy()
    if lines[0][0] < lines[0][1] and lines[1][0] > lines[1][1] \
            or lines[0][0] > lines[0][1] and lines[1][0] < lines[1][1]:
        return ((lines[0][0] + lines[1][0]) /(lines[0][1] + lines[1][1]) )/4


def cross_detector(data):
    return [is_crossed(data[x:x + 2]) for x in range(0, data.shape[0]) if
            x < data.shape[0] - 2 and is_crossed(data[x:x + 2]) is not None]
