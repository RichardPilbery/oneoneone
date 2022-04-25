from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import sys
import getopt
import logging
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

data = pd.read_csv("/oneoneone/avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics and stuff innit"),
        html.P(
            children="Analyze the behavior of avocado prices"
            " and the number of avocados sold in the US"
            " between 2015 and 2018",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)
