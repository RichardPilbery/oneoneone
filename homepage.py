from dash import html
import dash_bootstrap_components as dbc


### Layout 1
home = html.Div([
    html.H2("Homepage"),
    html.Hr(),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                            html.H4('Instructions'),
                            #create tabs
                            html.P("This site will enable you run a discrete event simulation to model demand arising from 111 calls triaged with a primary care dispostion. Use the form to configure the simulation.")
                            ]
                        ),
                    ],
                    width=6 #half page
                ),
                
                dbc.Col(
                    [
                        html.H4('Additional Components here'),
                        html.P('Click on graph to display text', id='graph-text')
                    ],
                    width=6 #half page
                )
                
            ],
        ), 
    ]),
])

