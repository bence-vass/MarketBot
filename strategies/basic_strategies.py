from data_handler.db_handler import Ticker
from market_indicators import moving_average


class Strategy:
    def __init__(self, database, portfolio, long_trading=True, short_trading=False):
        # TODO evaluate multiple tabel
        self._database = database
        self._portfolio = portfolio
        self._lt = long_trading
        self._st = short_trading

    def preprocessor(self):
        pass

    def evaluator(self):
        pass

    def evaluate_hist(self):
        pass


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


class Crossover(Strategy):

    def preprocessor(self):
        df = self._database.df
        df = moving_average.simple_moving_average(df, 20)
        df['over'] = df.apply(lambda r: r['close'] > r['SMA'], axis=1)
        df['turn'] = df['over'].diff()

    def evaluate_hist(self, from_date=None, to_date=None, flip=False):
        buy = self._portfolio.buy_stock
        sell = self._portfolio.sell_stock
        self.preprocessor()
        ticker = self._database
        ticker.df['long_buy'] = False
        ticker.df['long_sell'] = False
        if self._st:
            ticker.df['short_buy'] = False
            ticker.df['short_sell'] = False
        period = ticker.get_period(from_date=from_date, to_date=to_date)
        verbose = False
        for index, row in period.iterrows():
            if row['turn']:
                can_buy = int(self._portfolio.cash / row['close'])
                can_sell = 0 if ticker not in self._portfolio.stocks else self._portfolio.stocks[ticker]
                over_valued = not row['over'] if flip else row['over']
                if over_valued:
                    if self._lt:  # sell long
                        sell(ticker, index, can_sell, verbose=verbose)
                        ticker.df.at[index, 'long_sell'] = True
                    if self._st:  # buy short
                        buy(ticker, index, can_buy, verbose=verbose)
                        ticker.df.at[index, 'short_buy'] = True
                else:
                    if self._lt:  # buy long
                        buy(ticker, index, can_buy, verbose=verbose)
                        ticker.df.at[index, 'long_buy'] = True
                    if self._st:  # sell short
                        sell(ticker, index, can_sell, verbose=verbose)
                        ticker.df.at[index, 'short_sell'] = True
