import plotly.graph_objects as go

from data_handler.db_handler import Ticker


def create_candlestick_chart(ticker: Ticker):
    df = ticker.get_period()
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close']
            ),

        ]
    )

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends

        ]
    )
    return fig


def create_line(fig: go.Figure, ticker: Ticker, ):
    df = ticker.get_period()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['SMA']
        )
    )
    return fig
