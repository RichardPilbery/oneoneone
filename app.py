from dash import Dash
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import logging
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

logging.basicConfig(format='%(asctime)s %(message)s', filename='model.log', encoding='utf-8', level=logging.DEBUG)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
server = app.server
