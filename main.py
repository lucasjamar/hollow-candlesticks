import numpy as np
import pandas_datareader.data as web
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data():
    ohlc = web.DataReader(
        "GE",
        "yahoo",
        start='2022-01-01',
        end='2022-03-01'
    )
    ohlc["previousClose"] = ohlc["Close"].shift(1)
    ohlc["color"] = np.where(ohlc["Close"] > ohlc["previousClose"], "green", "red")
    ohlc["fill"] = np.where(ohlc["Close"] > ohlc["Open"], "rgba(255, 0, 0, 0)", ohlc["color"])
    ohlc["Percentage"] = ohlc["Volume"]*100/ohlc["Volume"].sum()
    price_bins = ohlc.copy()
    price_bins["Close"] = price_bins["Close"].round()
    price_bins = price_bins.groupby("Close", as_index=False)["Volume"].sum()
    price_bins["Percentage"] = price_bins["Volume"]*100/price_bins["Volume"].sum()
    return ohlc, price_bins


def hollow_candlesticks(ohlc: pd.DataFrame) -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=2,
        shared_xaxes="columns",
        shared_yaxes="rows",
        column_width=[0.8, 0.2],
        row_heights=[0.8, 0.2],
        horizontal_spacing=0,
        vertical_spacing=0,
        subplot_titles=["Candlestick", "Price Bins", "Volume", ""]
    )
    showlegend = True
    for index, row in ohlc.iterrows():
        color = dict(fillcolor=row["fill"], line=dict(color=row["color"]))
        fig.add_trace(
            go.Candlestick(
                x=[index],
                open=[row["Open"]],
                high=[row["High"]],
                low=[row["Low"]],
                close=[row["Close"]],
                increasing=color,
                decreasing=color,
                showlegend=showlegend,
                name="GE",
                legendgroup="Hollow Candlesticks"
            ),
            row=1,
            col=1
        )
        showlegend = False
    fig.add_trace(
        go.Bar(
            x=ohlc.index,
            y=ohlc["Volume"],
            text=ohlc["Percentage"],
            marker_line_color=ohlc["color"],
            marker_color=ohlc["fill"],
            name="Volume",
            texttemplate="%{text:.2f}%",
            hoverinfo="x+y",
            textfont=dict(color="white")
        ),
        col=1,
        row=2,
    )
    fig.add_trace(
        go.Bar(
            y=price_bins["Close"],
            x=price_bins["Volume"],
            text=price_bins["Percentage"],
            name="Price Bins",
            orientation="h",
            marker_color="yellow",
            texttemplate="%{text:.2f}% @ %{y}",
            hoverinfo="x+y"
        ),
        col=2,
        row=1,
    )
    fig.update_xaxes(
        rangebreaks=[dict(bounds=["sat", "mon"])],
        rangeslider_visible=False,
        col=1
    )
    fig.update_xaxes(
        showticklabels=True,
        showspikes=True,
        showgrid=True,
        col=2,
        row=1
    )
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        title_text="Hollow Candlesticks"
    )
    fig.show("browser")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ohlc, price_bins = load_data()
    hollow_candlesticks(ohlc)
