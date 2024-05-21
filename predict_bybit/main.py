import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from bybit_api.Market import Market
import json
import pandas as pd
from actions.times import get_date_from_time, get_time_from_data
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


class GradientBoostingRegressorPredict:

    def __init__(self, symbol: str, interval: str):
        self.symbol = symbol
        self.interval = interval
        data_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        market = Market.get_kline(start=get_time_from_data("2024-01-01 00:00:00"),
                                  end=get_time_from_data(data_now), interval=self.interval, symbol=self.symbol)
        market = json.loads(market)
        data = pd.DataFrame(market['result']['list'],
                            columns=["startTime", "openPrice", "highPrice", "lowPrice", "closePrice", "volume",
                                     "turnover"])
        data['startTime'] = data['startTime'].apply(lambda x: get_date_from_time(x, "%Y-%m-%d %H:%M:%S"))
        # Подготовка данных для модели
        df = data[["openPrice", "highPrice", "lowPrice", "volume", "turnover", "closePrice"]].copy()
        df['openPrice'] = df['openPrice'].astype(float)
        df['highPrice'] = df['highPrice'].astype(float)
        df['lowPrice'] = df['lowPrice'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df['turnover'] = df['turnover'].astype(float)
        df['closePrice'] = df['closePrice'].astype(float)
        self.df = df

    def predict(self) -> float:
        df = self.df
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        # Обучение модели
        model = GradientBoostingRegressor(random_state=0)
        model.fit(X_train, y_train)
        # Создание DataFrame для анализа
        db = pd.DataFrame(X_test, columns=["openPrice", "highPrice", "lowPrice", "volume", "turnover"])
        db['Analise'] = y_test
        db['Predict'] = model.predict(X_test)
        # Оценка модели
        score = model.score(X_test, y_test)
        print("R^2 score:", score)
        MAE = mean_absolute_error(db['Predict'], y_test)
        print("MAE:", MAE)
        MSE = mean_squared_error(db['Predict'], y_test)
        print("MSE:", MSE ** 0.5)
        # Прогнозирование на новых данных
        get_predict = Market.get_tickers(category="spot", symbol=self.symbol)
        get_predict = json.loads(get_predict)
        openPrice = get_predict['result']['list'][0]['lastPrice']
        highPrice = get_predict['result']['list'][0]['highPrice24h']
        lowPrice = get_predict['result']['list'][0]['lowPrice24h']
        volume = get_predict['result']['list'][0]['volume24h']
        turnover = get_predict['result']['list'][0]['turnover24h']
        new_data = np.array([openPrice, highPrice, lowPrice, volume, turnover]).reshape(1, -1)
        result = model.predict(new_data)
        return result



