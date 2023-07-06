import time
import datetime
import pandas as pd
from monitor import monitor as monitor

# period = {'D': ['5d', '1m'], 'W': ['1mo', '5m'], 'M': ['6mo', '60m']}
period = {'D': ['5d', '1m'], 'W': ['1mo', '5m'], '3W': ['3mo', '1h'], 'M': ['6mo', '1h']}
list_ticker = {}
ticker = {}


def big_loop(period):
    try:
        for n in list_ticker.values():
            n.monitoring(period)
    except:
        print('this part is error')


def decode_ticker(data):
    return data[0], [data[1], data[2]], data[3], data[4]


def create_monitor(data):
    arr = data.to_numpy()
    for n in arr:
        ticker, domain, time, update = decode_ticker(n)
        if ticker not in list_ticker:
            list_ticker[ticker] = monitor(ticker, domain)
        else:
            pass


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
        return 23400 + (86400 - Today.hour * 60 * 60 + Today.minute * 60 + Today.second)
    elif Today.hour < 6:
        return 23400 - Today.hour * 60 * 60 + Today.minute * 60 + Today.second


hour = 1
min = 1
data = pd.read_csv('Ticker.csv')
create_monitor(data)
while True:
    try:
        if is_time():
            start = time.perf_counter()
            if hour == 12:
                big_loop(period['3W'])
                big_loop(period['M'])
                big_loop(period['W'])
                hour = 1
            else:
                big_loop(period['W'])
                hour += 1
                # min = 1
            # else:
            #     big_loop(period['D'])
            #     min += 1
            #     hour += 1
            end = time.perf_counter()
            lap = end - start
            time.sleep(300 - lap)
        else:
            print("waiting back soon")
            time.sleep(convert_second())
    except ConnectionError:
        time.sleep(300)
