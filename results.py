
from dash import dcc, html
import dash_bootstrap_components as dbc
from layouts import DROPDOWN_STYLE
import logging

### Layout 2
results = html.Div(
    [
        html.H2('Results'),
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        html.Div([
                            dcc.Dropdown(id='dropdown-run-number')
                        ], style=DROPDOWN_STYLE),
                        html.Hr(),
                    ],
                ),
                dbc.Row(
                    [
                        html.H4('Call activity'),
                        html.Div([
                            dcc.Graph(id='ooo-call-volume')
                        ]),
                    ]
                ),
                dbc.Row(
                    [
                        html.H4('Patient demographics'),
                        html.Div([
                            dcc.Graph(id='age-dist')
                        ]),
                    ]
                ),
                dbc.Row(
                    [
                        html.H4('Another row of results'),
                        html.Hr(),
                    ]
                ),
            ]
        )
    ])
