from dash import html, Input, Output
from app import app
import logging

buttonClickCount = 0

logging.basicConfig(format='%(asctime)s %(message)s', filename='simconfig.log', encoding='utf-8', level=logging.DEBUG)

# Sim configuration callback
@app.callback(
    Output('config', 'children'),
    Input('sim_duration', 'value'),
    Input('warm_up_time', 'value'),
    Input('number_of_runs', 'value'),
    Input('run_sim', 'n_clicks')
)
def configSim(sim_duration, warm_up_time, number_of_runs, run_sim):
    global buttonClickCount

    if(run_sim > buttonClickCount):
        # Run the sim
        output = f"Sim duration: {sim_duration}<br/>Warm-up time: {warm_up_time}</br>Number of runs: {number_of_runs}"
        logging.debug("Data submitted")
        logging.debug(output)
        buttonClickCount = run_sim
        return html.P(output)
