# Прогнозирование цены на бирже Bybit с использованием scikit-learn
1. Взаимодействие с биржей через api
````
 @staticmethod
    def get_kline(category="spot", interval=30, symbol="BTCUSDT", start=1671062400000, end=1671064400000):
        req = Bybit.base_url + f"/v5/market/kline?category={category}&symbol={symbol}&interval={interval}&start={start}&end={end}&limit=1000"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text

 @staticmethod
    def get_tickers(category="spot", symbol="BTCUSDT"):
        req = Bybit.base_url + f"/v5/market/tickers?category={category}&symbol={symbol}"
        payload = {}
        headers = {}
        response = requests.request("GET", req, headers=headers, data=payload)

        return response.text
````
2. Использование scikit-learn GradientBoostingRegressor для прогнозирования непрерывных числовых
значений на основе входных признаков. GradientBoostingRegressor из библиотеки scikit-learn используется для задачи регрессии, то есть для предсказания числовых значений на основе заданного набора признаков. Основные особенности и назначение GradientBoostingRegressor включают:

- Модель ансамбля: Это ансамблевая модель, которая объединяет множество слабых моделей (обычно деревьев решений) для создания сильного прогностического регрессора.
- Пошаговая оптимизация: GradientBoostingRegressor строит деревья решений последовательно, каждое новое дерево корректирует ошибки, допущенные предыдущими деревьями. Это достигается путем минимизации функции потерь, которая обычно является среднеквадратичной ошибкой для задач регрессии.
- Градиентный спуск: Модель использует метод градиентного спуска для минимизации функции потерь, что позволяет модели корректировать предсказания и улучшать точность.
- Обработка сложных зависимостей: Благодаря своей структуре и способности обучаться на ошибках предыдущих моделей, GradientBoostingRegressor хорошо справляется с моделированием сложных нелинейных зависимостей между признаками и целевой переменной.
- Гиперпараметры: Модель имеет несколько гиперпараметров, таких как количество деревьев (n_estimators), глубина деревьев (max_depth), скорость обучения (learning_rate), которые позволяют контролировать процесс обучения и предотвращать переобучение.
````
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
````
3. При запуске система получает данные за указанный период данные по определенной паре
и текущие данные и делает прогноз о цене закрытия.
````
R^2 score: 0.997342040423959
MAE: 511.68598388888626 
MSE: 795.9522602245463
[70786.50238589]
````
где:
- R^2 score точность модели;
- MAE средняя абсолютная ошибка;
- MSE средняя квадратичная ошибка