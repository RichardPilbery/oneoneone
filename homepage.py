from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app import app


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
                        html.H4('Configure simulation'),

                        html.P('Sim duration in hours', id='sim_duration_label'),
                        dcc.Slider(
                            2880,
                            5760,
                            step=24,
                            value=5760,
                            marks=None,
                            id='sim_duration',
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),

                        html.P('Warm up duration', id='warm_up_duration_label'),
                        dcc.Slider(
                            0,
                            1440,
                            step=24,
                            value=1440,
                            marks=None,
                            id='warm_up_time',
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),

                        html.P('Number of runs', id='number_of_runs_label'),
                        dcc.Slider(
                            0,
                            10,
                            step=1,
                            value=3,
                            marks=None,
                            id='number_of_runs',
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),

                        dbc.Button(
                            "Run Simulation", id="run_sim", className="me-2", outline=True, color="primary",
                            n_clicks = 0
                        ),

                        html.Div(id="config"),

                    ],
                    width=6 #half page
                )
                
            ],
        ), 
    ]),
])

@app.callback(
    Output('config', 'children'),
    [Input('sim_duration', 'value'),
    Input('warm_up_time', 'value'),
    Input('number_of_runs', 'value'),
    Input('run_sim', 'n_clicks')]
)
def configSim(sim_duration, warm_up_time, number_of_runs, run_sim):
    global buttonClickCount

    if(run_sim > buttonClickCount):
        # Run the sim
        buttonClickCount == run_sim
        return html.P(f"Sim duration: {sim_duration}<br/>Warm-up time: {warm_up_time}</br>Number of runs: {number_of_runs}")