from data_handler.db_handler import Ticker


class Strategy:
    def __init__(self, evaluator, long_trading=True, short_trading=False):
        self._evaluator = evaluator
        self._lt = long_trading
        self._st = short_trading


def crossover(ticker: Ticker, buy, sell, ma_name='SMA', long_trading=True, short_trading=False):
    df = ticker.df
    df['over'] = df.apply(lambda r: r['close'] > r[ma_name], axis=1)
    df['turn'] = df['over'].diff()
    for index, row in ticker.get_period().iterrows():
        if row['turn']:
            if row['over']:
                if long_trading:  # buy long
                    buy()
                if short_trading:  # sell short
                    sell()
            else:
                if long_trading:  # sell long
                    sell()
                if short_trading:  # buy short
                    buy()
