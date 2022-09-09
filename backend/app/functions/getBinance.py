import requests
import json

BINANCE_API = "https://api1.binance.com/api"


def get_binance_specify_symbol_price(symbol):
    URL = BINANCE_API + "/v3/ticker/24hr?symbol=" + symbol
    # https://api1.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT

    r = requests.get(URL)
    data = json.loads(r.text)
    return data
