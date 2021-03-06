from dash import dcc, html 
import dash_bootstrap_components as dbc
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE


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
                            1,
                            10,
                            step=1,
                            value=3,
                            marks=None,
                            id='number_of_runs',
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        html.Div(
                            id="submit_button",
                            children=[
                                dbc.Button(
                                    "Run Simulation", id="run_sim", className="me-2", outline=True, color="primary",
                                    n_clicks = 0,
                                ),
                            ],
                            style = SHOW_BUTTON_STYLE
                        ),
                        html.Div(
                            id="sim_run_button",
                            children=[
                                dbc.Button(
                                    [dbc.Spinner(size="sm"), " Simulation running..."],
                                    id="sim_running",
                                    color="primary",
                                    disabled=True,
                                ),
                            ],
                            style = HIDE_BUTTON_STYLE
                        ),

                        html.Div(
                            id="sim_block",
                            children=[
                                dcc.Input(
                                    id="sim_running", 
                                    type="hidden", 
                                    value=0,
                                ),
                                dcc.Input(
                                    id="sim_complete", 
                                    type="hidden", 
                                    value=0,
                                ),
                                dcc.Input(
                                    id="toggle_button", 
                                    type="hidden", 
                                    value=0,
                                )
                            ],
                            style = {'display':'none'}
                        ),


                    ],
                    width=6 #half page
                )
                
            ],
        ), 
    ]),
])
