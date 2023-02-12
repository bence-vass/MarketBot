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


def trend_line(fig: go.Figure, ticker: Ticker, ):
    df = ticker.get_period()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['SMA']
        )
    )
    return fig


def buy_sell_points(fig: go.Figure, ticker: Ticker):
    df = ticker.get_period()
    l_buys = df[df['long_buy']]
    l_sells = df[df['long_sell']]
    fig.add_trace(go.Scatter(
        x=l_buys.index,
        y=l_buys['close'],
        name='Buy Long',
        mode='markers',
        marker=dict(
            color='blue',
            size=12,
            line=dict(
                width=2,
                color='DarkSlateGrey'
            )
        ),
    ))
    fig.add_trace(go.Scatter(
        x=l_sells.index,
        y=l_sells['close'],
        name='Sell Long',
        mode='markers',
        marker=dict(
            color='pink',
            size=12,
            line=dict(
                width=2,
                color='DarkSlateGrey'
            )
        ),
    ))

    return fig
