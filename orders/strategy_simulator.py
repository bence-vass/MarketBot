class MarketSimulation:
    def __int__(self,
                positions=None,
                cash=10000,
                start_date=None,
                end_date=None
                ):
        self._positions = positions
        self._cash = cash
        self._start_date = start_date
        self._end_date = end_date
