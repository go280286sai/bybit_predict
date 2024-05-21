import requests

from bybit_api.Bybit import Bybit


class Market(Bybit):

    @staticmethod
    # get server time
    def get_bybit_server_time():
        req = Bybit.base_url + "/v5/market/time"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

    # get kline
    # category: linear, inverse, spot
    # interval: 1, 3, 5, 15, 30, 1, 2, 4, 6, 8, 12, 1, 3, 1, 1
    # symbol: BTCUSDT, ETHUSDT ...
    # limit: 5, 30, 60, 120, 240, 360, 720, W, M, D,
    # start ...
    # end ...
    @staticmethod
    def get_kline(category="spot", interval=30, symbol="BTCUSDT", start=1671062400000, end=1671064400000):
        req = Bybit.base_url + f"/v5/market/kline?category={category}&symbol={symbol}&interval={interval}&start={start}&end={end}&limit=1000"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

    # Get Mark Price Kline
    # category: linear, inverse
    # interval: 1, 3, 5, 15, 30, 1, 2, 4, 6, 8, 12, 1, 3, 1, 1
    # symbol: BTCUSDT, ETHUSDT ...
    # limit: 5, 30, 60, 120, 240, 360, 720, W, M, D,
    # start ...
    # end ...
    @staticmethod
    def get_mark_price_kline(category="linear", interval=30, symbol="BTCUSDT", limit=30, start=1671062400000,
                             end=1671064400000):
        if category != "linear" and category != "inverse":
            raise ValueError("category must be linear or inverse")
        req = Bybit.base_url + f"/v5/market/mark-price-kline?category={category}&symbol={symbol}&interval={interval}&start={start}&end={end}&limit={limit}"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

    # get orderbook
    # category: linear, inverse, spot, option
    # symbol: BTCUSDT, ETHUSDT ...
    # spot：1-50，default：1. linear&inverse：1-200，default：25. option：1-25，default
    @staticmethod
    def get_orderbook(category="spot", symbol="BTCUSDT", limit=30):
        req = Bybit.base_url + f"/v5/market/orderbook?category={category}&symbol={symbol}&limit={limit}"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

    # get tickers
    # category: linear, inverse, spot
    # symbol: BTCUSDT, ETHUSDT ...
    @staticmethod
    def get_tickers(category="spot", symbol="BTCUSDT"):
        req = Bybit.base_url + f"/v5/market/tickers?category={category}&symbol={symbol}"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text
