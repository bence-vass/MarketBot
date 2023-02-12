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

        from market_indicators import moving_average
        from strategies import basic_strategies
        from orders import strategy_simulator

        ticker_AAPL = moving_average.simple_moving_average(ticker_AAPL, 15)
        ticker_AAPL.from_date = "2022-06-01"

        ma_strategy = basic_strategies.Strategy(basic_strategies.crossover)
        portfolio = strategy_simulator.Portfolio(cash=1000)

        # simulation = strategy_simulator.MarketSimulation(portfolio, ma_strategy)

        # simulation.run(verbose=True)

        # basic_strategies.crossover(ticker_AAPL)

        # fig = create_candlestick.create_candlestick_chart(ticker_AAPL)
        # fig = create_candlestick.create_line(fig, ticker_AAPL)
        # fig.show()

    else:
        raise Exception('No input data_handler provided')


if __name__ == '__main__':
    # app(api_service='polygon.io', api_key=os.getenv('POLYGON_API_KEY'))
    app(db_path='./historical_data_sample', db_file='AAPL.csv')
