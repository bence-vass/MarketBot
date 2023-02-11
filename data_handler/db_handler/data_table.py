import datetime

import pandas as pd


class Ticker:
    def __init__(self, path: str, filename: str,
                 from_date=None, to_date=None
                 ):
        extension = filename.split(".")[-1]
        self._ticker = "".join(filename.split(".")[:-1])
        self._df = None
        if extension == 'csv':
            self._df = pd.read_csv(path + '/' + filename)

        self.standard_naming(data_format='ohlcav')
        self._real_frequency = None
        if self._real_frequency is None:
            self.measure_frequency()
        self.standard_indexing()

        self._from_date = self.str_to_date(from_date)
        self._to_date = self.str_to_date(to_date)

    def standard_indexing(self, col_index=0):
        self._df.set_index(self._df.columns[col_index], inplace=True, drop=True)

    def standard_naming(self, data_format, data_col=0):
        standard_names = ['open', 'high', 'low', 'close']
        match data_format:
            case 'ohlc':
                pass
            case 'ohlcv':
                standard_names.append('volume')
            case 'ohlcav':
                standard_names.extend(['adj_close', 'volume'])
        standard_names.insert(data_col, 'date')
        self._df = self._df.set_axis(standard_names, axis=1)
        self._df.date = pd.to_datetime(self._df.date)

    def measure_frequency(self, date_col='date'):
        self._real_frequency = self._df[date_col].diff().mean()

    @property
    def df(self):
        return self._df

    @property
    def ticker(self):
        return self._ticker

    @property
    def frequency(self):
        return self._real_frequency

    @property
    def index(self):
        return self._df.index

    @property
    def to_date(self):
        return self._to_date

    @to_date.setter
    def to_date(self, v):
        self._to_date = self.str_to_date(v)

    @property
    def from_date(self):
        return self._from_date

    @from_date.setter
    def from_date(self, v):
        self._from_date = self.str_to_date(v)

    def __repr__(self):
        return "Table()"

    def __str__(self):
        sample = str(self.get_period() if self._to_date or self._from_date else self._df.tail())
        return "======\t" + self._ticker + "\t======\n" \
            + "Frequency: " + str(self._real_frequency) \
            + "\n" + sample

    def __getitem__(self, item):
        return self._df[item]

    @staticmethod
    def str_to_date(date):
        if date:
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        else:
            return None

    def get_period(self, from_date=None, to_date=None, use_ticker_period=True):
        b_f, b_t = None, None
        if use_ticker_period:
            b_f = self._from_date
            b_t = self._to_date
        f = self.str_to_date(from_date) if from_date else b_f
        t = self.str_to_date(to_date) if to_date else b_t
        df = self._df
        if f:
            df = df[df.index >= f]
        if t:
            df = df[df.index <= t]
        return df
