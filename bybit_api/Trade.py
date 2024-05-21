import requests

from bybit_api.Bybit import Bybit


class Trade(Bybit):
    @staticmethod
    def get_trade(category="spot", symbol="BTCUSDT", limit=30):
        req = Bybit.base_url + f"/v5/market/trade?category={category}&symbol={symbol}&limit={limit}"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

    @staticmethod
    def get_order_history():
        try:
            req = Bybit.base_url + f"/v5/order/history?category=spot&symbol=BTC"
            payload = {}
            headers = {
                'X-BAPI-API-KEY': '2BQMFvIInyrDZ18u4M',
                'X-BAPI-TIMESTAMP': '1715943238756',
                'X-BAPI-RECV-WINDOW': '20000',
                'X-BAPI-SIGN': '8f5744f0c04a08342b06d267a170472f06afd24035c493c3c0bcc88193af7937'
            }
            response = requests.request("GET", req, headers=headers, data=payload)

            print(response.text)
            print("ok")
        except ValueError as e:
            print(e)

Trade.get_order_history()
