
from dash import html
import dash_bootstrap_components as dbc
from figures import fig_age_dist

### Layout 2
results = html.Div(
    [
        html.H2('Results'),
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        html.H4('Insert results table here'),
                        html.Hr(),
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