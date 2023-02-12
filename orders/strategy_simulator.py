import datetime

from data_handler.db_handler.data_table import Ticker
from strategies.basic_strategies import Strategy
from utils.parser import str_to_date


class Portfolio:
    def __init__(self, cash=0., stocks=None):
        self._cash = cash
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
    def buy_stock(self, ticker: Ticker, date: str | datetime.datetime, num_shares: str | float = None,
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
            print('No sufficient coverage for this transaction')

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

    # TODO early stage
    def check_portfolio_settings(self, ticker, num_shares):
        if ticker in self._stocks:
            if self._stocks[ticker] < num_shares:
                print("You are taking a short position...")
            else:
                pass
        else:
            print("You are taking a short position...")
        return True


class MarketSimulation:
    def __init__(self,
                 portfolio: Portfolio,
                 strategy: Strategy,
                 start_date=None,
                 end_date=None,
                 ):
        self._portfolio = portfolio
        self._strategy = strategy
        self._start_date = start_date
        self._end_date = end_date

    def run(self, verbose=False):
        print("Begin simulation...")
        print(self._portfolio)
