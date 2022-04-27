from dash import Dash
import dash_bootstrap_components as dbc
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename='model.log', encoding='utf-8', level=logging.DEBUG)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
