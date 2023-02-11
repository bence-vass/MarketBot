import pandas as pd


class Ticker:
    def __init__(self, path: str, filename: str):
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

    def __repr__(self):
        return "Table()"

    def __str__(self):
        return "======\t" + self._ticker + "\t======\n" \
            + "Frequency: " + str(self._real_frequency) \
            + "\n" + str(self._df.tail())

    def __getitem__(self, item):
        return self._df[item]
