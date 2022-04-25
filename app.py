from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
from oneoneonedes import parallelProcess
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )





if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)
