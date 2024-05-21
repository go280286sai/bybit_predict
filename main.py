from predict_bybit.main import GradientBoostingRegressorPredict

obj = GradientBoostingRegressorPredict(symbol="BTCUSDT", interval="D")
print(obj.predict())

