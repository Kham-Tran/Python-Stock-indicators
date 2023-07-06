import json

import requests

url = 'http://192.168.1.8:8000/getticker'

from rest_framework import serializers


class tickerInfor:
    def __init__(self, ticker, data, macd, ema) -> None:
        self.ticker = ticker
        self.data = data
        self.macd = macd
        self.ema = ema


class tickerSerializer(serializers.Serializer):
    ticker = serializers.CharField()
    data = serializers.JSONField()
    macd = serializers.JSONField()
    ema = serializers.JSONField()

payload = {'ticker':'spy', 'period':'1mo'}
d = requests.get(url=url,params=payload)
n = d.content.decode('utf-8')
data = json.loads(n)
print(data['Macd'])
print(d.url)
