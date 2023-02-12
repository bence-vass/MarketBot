from dotenv import load_dotenv

from data_handler import api_handler
from data_handler import db_handler

load_dotenv('./dev.env')
TICKER_TO_SEARCH = [
    'AAPL',
    'MSFT',
]


def app(
        api_service: str = None,
        api_key: str = None,

        db_path: str = None,
        db_file: str = None,
):
    if api_service and api_key:
        client = api_handler.connect_client(api_service, api_key)

    elif db_path and db_file:
        ticker_AAPL = db_handler.Ticker(path=db_path, filename=db_file)

        from strategies import basic_strategies
        from orders import strategy_simulator
        from charts import create_candlestick
        from market_indicators.moving_average import simple_moving_average

        dataset = ticker_AAPL
        portfolio = strategy_simulator.Portfolio(cash=1000)
        strategy = basic_strategies.Crossover(dataset, portfolio)
        from_date = '2020-06-01'
        # to_date = '2023-01-01'
        to_date = None
        strategy.evaluate_hist(from_date=from_date, to_date=to_date, flip=True)

        # basic_strategies.crossover(ticker_AAPL)
        ticker_AAPL.from_date = from_date
        ticker_AAPL.to_date = to_date
        ticker_AAPL = simple_moving_average(ticker_AAPL, 50)

        fig = create_candlestick.create_candlestick_chart(ticker_AAPL)
        fig = create_candlestick.trend_line(fig, ticker_AAPL)
        fig = create_candlestick.buy_sell_points(fig, ticker_AAPL)
        fig.show()

        print(portfolio)

    else:
        raise Exception('No input data_handler provided')


if __name__ == '__main__':
    # app(api_service='polygon.io', api_key=os.getenv('POLYGON_API_KEY'))
    app(db_path='./historical_data_sample', db_file='AAPL.csv')
