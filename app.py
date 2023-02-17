import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from model import prediction

app = dash.Dash(__name__)
server = app.server


def get_stock_price_fig(df):
    fig = px.line(
        df, x="Date", y=["Close", "Open"], title="Closing and Opening price vs Date"
    )
    return fig


def get_indicator_fig(df):
    df["EWA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    fig = px.scatter(
        df, x="Date", y="EWA_20", title="Exponential Moving Average vs Date"
    )
    return fig


item1 = html.Div(
    [
        html.P("Welcome to Stock Dash!", className="start"),
        html.Div(
            [
                html.P("Input stock code:"),
                dcc.Input(id="dropdown_tickers", type="text"),
                html.Button("Submit", id="submit")
                # Stock code input
            ]
        ),
        html.Div(
            [
                dcc.DatePickerRange(id="my-date-picker-range")
                # Date range picker input
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Button("Stock Price", id="stock"),
                        html.Button("Indicators", id="indicators"),
                    ],
                    className="menu",
                ),
                html.Div(
                    [
                        dcc.Input(placeholder="Number of days", id="n_days"),
                        html.Button("Forecast", id="forecast"),
                    ]
                )
                # Stock price button
                # Indicators button
                # Number of days of forecast input
                # Forecast button
            ],
            className="main-menu",
        ),
    ],
    className="nav",
)

item2 = html.Div(
    [
        html.Div(
            [html.Img(id="logo"), html.Label(id="ticker")],
            className="header",
        ),
        html.Div(
            # Description
            id="description",
            className="description_ticker",
        ),
        html.Div(
            [
                # Stock price plot
            ],
            id="graphs-content",
        ),
        html.Div(
            [
                # Indicator plot
            ],
            id="main-content",
        ),
        html.Div(
            [
                # Forecast plot
            ],
            id="forecast-content",
        ),
    ],
    className="content",
)

app.layout = html.Div([item1, item2], className="container")


# Callback for company info.
@app.callback(
    [
        Output("description", "children"),
        Output("logo", "src"),
        Output("ticker", "children"),
        Output("stock", "n_clicks"),
        Output("forecast", "n_clicks"),
    ],
    [Input("submit", "n_clicks")],
    [State("dropdown_tickers", "value")],
)
def update_data(n, val):
    if n == None:
        return (
            "Scrip code not found.",
            "https://picsum.photos/100/100.jpg",
            "404",
            None,
            None,
        )

    if val == None:
        raise PreventUpdate
    else:
        ticker = yf.Ticker(val)
        inf = ticker.info
        if inf == None:
            return (
                "Scrip code not found.",
                "https://picsum.photos/100/100.jpg",
                "404",
                None,
                None,
            )
        df = pd.DataFrame().from_dict(inf, orient="index").T
        df[["logo_url", "shortName", "longBusinessSummary"]]

    return (
        df["longBusinessSummary"].values[0],
        df["logo_url"].values[0],
        df["shortName"].values[0],
        None,
        None,
    )


# Callback for stock graphs
@app.callback(
    [Output("graphs-content", "children")],
    [
        Input("stock", "n_clicks"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
    [State("dropdown_tickers", "value")],
)
def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]


# Callback for indicators
@app.callback(
    [Output("main-content", "children")],
    [
        Input("indicators", "n_clicks"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
    [State("dropdown_tickers", "value")],
)
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date != None:
        df = yf.download(val, str(start_date), str(end_date))
    else:
        df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_indicator_fig(df)
    return [dcc.Graph(figure=fig)]


@app.callback(
    [Output("forecast-content", "children")],
    [Input("forecast", "n_clicks")],
    [State("n_days", "value"), State("dropdown_tickers", "value")],
)
def forecast(n, n_days, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    fig = prediction(val, int(n_days) + 1)
    return [dcc.Graph(figure=fig)]


if __name__ == "__main__":
    app.run_server(debug=True)
