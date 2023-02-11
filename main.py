import os
from data_handler import api_handler
from data_handler import db_handler
from dotenv import load_dotenv

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
        table = moving_average.simple_moving_average(ticker_AAPL)
        print(table)

    else:
        raise Exception('No input data_handler provided')


if __name__ == '__main__':
    # app(api_service='polygon.io', api_key=os.getenv('POLYGON_API_KEY'))
    app(db_path='./historical_data_sample', db_file='AAPL.csv')
