import dash
from dash import html
from dash import dcc
from datetime import datetime as dt

app = dash.Dash(__name__)
server = app.server

item1 = html.Div(
    [
        html.P("Welcome to Stock Dash!", className="start"),
        html.Div(
            [
                "Input stock code:",
                html.Br(),  # Could be removed later
                html.Br(),
                dcc.Input(),
                html.Button("Submit")
                # Stock code input
            ]
        ),
        html.Div(
            [
                dcc.DatePickerRange()
                # Date range picker input
            ]
        ),
        html.Div(
            [
                html.Button("Stock Price"),
                html.Button("Indicators"),
                dcc.Input(placeholder="Number of days"),
                html.Button("Forecast")
                # Stock price button
                # Indicators button
                # Number of days of forecast input
                # Forecast button
            ]
        ),
    ],
    className="nav",
)

item2 = html.Div(
    [
        html.Div(
            [
                # Logo
                # Name
            ],
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

app.layout = html.Div([item1, item2])

if __name__ == "__main__":
    app.run_server(debug=True)
