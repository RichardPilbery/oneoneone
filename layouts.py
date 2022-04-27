from dash import html
import dash_bootstrap_components as dbc

# Mostly stolen from here: https://towardsdatascience.com/callbacks-layouts-bootstrap-how-to-create-dashboards-in-plotly-dash-1d233ff63e30

NAVBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "top":0,
    "margin-top":'2rem',
    "margin-left": "18rem",
    "margin-right": "2rem",
}

SHOW_BUTTON_STYLE = {
    "display": "block"
}

HIDE_BUTTON_STYLE = {
    "display": "block"
}

#####################################
# Create Auxiliary Components Here
#####################################

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
    [
        html.H4("Modelling 111 Demand", className="display-10",style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Start", href="/home",active="exact", external_link=True),
                dbc.NavLink("Results", href="/results", active="exact", external_link=True)
            ],
            pills=True,
            vertical=True
        ),
    ],
    style=NAVBAR_STYLE,
    )  
    return navbar
