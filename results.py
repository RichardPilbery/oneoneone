
from dash import dcc, html
import dash_bootstrap_components as dbc
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
                        html.H4('Age distribution of patients'),
                        dcc.Dropdown(id='age-dist-run-number'),
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
