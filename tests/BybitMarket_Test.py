import json
from actions.times import get_time_from_data

from bybit_api.Market import Market

start = get_time_from_data("2024-05-14 00:00:00")
end = get_time_from_data("2024-05-15 00:00:00")


def test_index():
    server_time = Market.get_bybit_server_time()
    obj = json.loads(server_time)
    assert obj['time'] > 1


def test_get_kline():
    kline = Market.get_kline(category="spot", interval=15, symbol="BTCUSDT", limit=30, start=start, end=end)
    obj = json.loads(kline)
    assert len(obj['result']['list']) == 30


def test_get_mark_price_kline():
    kline = Market.get_kline(category="linear", interval=15, symbol="BTCUSDT", limit=30, start=start, end=end)
    obj = json.loads(kline)
    assert len(obj['result']['list']) == 30


def test_get_orderbook():
    orderbook = Market.get_orderbook(category="spot", symbol="BTCUSDT", limit=30)
    obj = json.loads(orderbook)
    assert len(obj['result']['a']) == len(obj['result']['b']) == 30


def test_get_tickers():
    tickers = Market.get_tickers(category="spot", symbol="BTCUSDT")
    obj = json.loads(tickers)
    assert len(obj['result']['list']) > 0
