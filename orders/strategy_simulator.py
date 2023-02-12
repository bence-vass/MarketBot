import datetime

from data_handler.db_handler.data_table import Ticker
from strategies.basic_strategies import Strategy
from utils.parser import str_to_date


class Order:

    def buy_long(self, price, date):
        print("BUY-LONG\tfor: " + str(price) + "\tat: " + str(date))

    def sell_long(self, price, date):
        print("SELL-LONG\tfor: " + str(price) + "\tat: " + str(date))


class Portfolio:
    def __init__(self, cash=0., credit=0., stocks=None, margin_account=False):
        self._cash = cash
        self._credit = credit
        self._margin_account = margin_account
        self._stocks = {}
        if stocks:
            self.update_stocks(stocks)

    def __str__(self):
        positions = []
        if self._stocks:
            for k, v in self._stocks.items():
                positions.append(k.ticker + ": " + str(v) + " share(s)")
        return "Cash: " + \
            str(self._cash) + " USD\n" + \
            "===================\n" + "\n".join(positions) + \
            ("No positions\n" if not positions else "\n")

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, v):
        self._cash = v

    @property
    def stocks(self):
        return self._stocks

    def update_stocks(self, stocks, mode='set'):
        modes = ['set', 'add', 'remove']
        if mode not in modes:
            raise ValueError("Invalid update mode. Expected: %s" % modes)
        match mode:
            case 'set':
                self._stocks = stocks
            case 'add':
                for k, v in stocks.items():
                    self._stocks[k] = v if k not in self._stocks else self._stocks[k] + v
            case 'remove':
                for k, v in stocks.items():
                    self._stocks[k] = -v if k not in self._stocks else self._stocks[k] - v
        for k, v in list(self._stocks.items()):
            if v == 0.:
                del self._stocks[k]

    def get_position(self, ticker_name):
        if ticker_name in self._stocks.keys():
            print(self._stocks[ticker_name])
            return self._stocks[ticker_name]
        else:
            print("Not in portfolio")
            return None

    # TODO Buy multiple shares
    def buy_stock(self, ticker: Ticker, date: str | datetime.datetime, num_shares: int | float,
                  buy_for_price: float = None, verbose=False):
        if type(date) == str:
            date = str_to_date(date)
        price_t = ticker.df.loc[date]['close']
        if verbose:
            print("BUY-" + ticker.ticker + " for " + str(price_t) + " USD at " + str(date))
            print("Total: " + str(price_t * num_shares) + " USD\n")
        transaction_vol = price_t * num_shares
        if self.check_coverage(transaction_vol):
            self._cash = self._cash - transaction_vol
            self.update_stocks({
                ticker: num_shares
            }, 'add')
        else:
            print('Not sufficient coverage for this transaction')

    def check_coverage(self, transaction_volumen):
        if self._cash >= transaction_volumen:
            return True
        return False

    def sell_stock(self, ticker: Ticker, date: str | datetime.datetime, num_shares: int | float, verbose=False):
        if type(date) == str:
            date = str_to_date(date)
        price_t = ticker.df.loc[date]['close']
        if verbose:
            print("SELL-" + ticker.ticker + " for " + str(price_t) + " USD at " + str(date))
            print("Total: " + str(price_t * num_shares) + " USD\n")
        transaction_vol = price_t * num_shares
        if self.check_portfolio_settings(ticker, num_shares):
            self.update_stocks({
                ticker: num_shares
            }, 'remove')
            self._cash = self._cash + transaction_vol
        else:
            print('Not sufficient coverage for this transaction')

    # TODO early stage
    def check_portfolio_settings(self, ticker, num_shares):
        if ticker in self._stocks:
            if self._stocks[ticker] >= num_shares:
                return True
        print("You are taking a short position...")
        if self._margin_account:
            return True
        print("You require a margin account to take short position")
        return False


class MarketSimulation:
    def __init__(self,
                 database,
                 strategy: Strategy,
                 portfolio: Portfolio,
                 start_date=None,
                 end_date=None,
                 ):
        self._database = database
        self._portfolio = portfolio
        self._strategy = strategy
        self._start_date = start_date
        self._end_date = end_date

    def run(self, verbose=False):
        print("Begin simulation...")
        if verbose:
            print("Initial Portfolio:")
            print(self._portfolio)

        ticker = self._database[0]
        df = ticker.df
        # preprocessor
        from market_indicators import moving_average
        df = moving_average.simple_moving_average(df, 20)
        df['over'] = df.apply(lambda r: r['close'] > r['SMA'], axis=1)
        df['turn'] = df['over'].diff()

        # evaluation

        # TODO add these params to Strategy class
        long_trading = True
        short_trading = False
        buy = self._portfolio.buy_stock
        sell = self._portfolio.sell_stock

        period = ticker.get_period(from_date=self._start_date, to_date='2023-01-01')
        for index, row in period.iterrows():
            if row['turn']:
                can_buy = int(self._portfolio.cash / row['close'])
                can_sell = 0 if ticker not in self._portfolio.stocks else self._portfolio.stocks[ticker]

                if row['over']:
                    if long_trading:  # buy long
                        buy(ticker, index, can_buy, verbose=True)
                    if short_trading:  # sell short
                        sell(ticker, index, can_sell, verbose=True)
                else:
                    if long_trading:  # sell long
                        sell(ticker, index, can_sell, verbose=True)
                    if short_trading:  # buy short
                        buy(ticker, index, can_buy, verbose=True)
