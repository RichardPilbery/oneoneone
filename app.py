from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
from oneoneonedes import parallelProcess

parallelProcess(4)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
    children=[
        html.H1(children="111 Discrete Event Simulation model"),
        html.P(
            children="Click on the button below to run the simulation",
        ),
    ]),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic', children='Enter a value and press submit')
])

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    parallelProcess(4)
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )




if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)
