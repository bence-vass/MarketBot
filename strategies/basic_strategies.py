from data_handler.db_handler import Ticker


def crossover(ticker: Ticker, ma_name='SMA', long_trading=True, short_trading=False):
    df = ticker.df
    df['over'] = df.apply(lambda r: r['close'] > r[ma_name], axis=1)
    df['turn'] = df['over'].diff()
    for index, row in ticker.get_period().iterrows():
        if row['turn']:
            if row['over']:
                if long_trading:
                    print("BUY-LONG\tfor: " +
                          str(row['close']) + "\tat: " + str(index))
                    if short_trading:
                        print("SELL_SHORT --- at:" + str(index))
            else:
                if long_trading:
                    print("SELL-LONG --- at:" + str(index))
                if short_trading:
                    print("BUY-SHORT --- at:" + str(index))
