from dash import html, Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager
from app import app
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE
import logging
from oneoneonedes import parallelProcess, prepStartingVars



# 3. When trigger sim is set to value = 1, then simulation will run
# When it has finished, sim_complete is set to 1
@app.long_callback(
    outputs = Output('sim_complete', 'value'),
    inputs = Input('run_sim', 'n_clicks'),
    states = [
        State('sim_duration', 'value'),
        State('warm_up_time', 'value'),
        State('number_of_runs', 'value'),
    ],
    running = [
        (Output('submit_button', 'style'), HIDE_BUTTON_STYLE, SHOW_BUTTON_STYLE),
        (Output('sim_run_button', 'style'), SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE),
    ]
)
def configSim(submit_button_style, sim_duration, warm_up_time, number_of_runs):
    if submit_button_style == HIDE_BUTTON_STYLE:
        # Run the sim
        output = f"Sim duration: {sim_duration}; Warm-up time: {warm_up_time}; Number of runs: {number_of_runs}"
        logging.debug("Data submitted")
        logging.debug(output)
        
        prepStartingVars(
            number_of_runs = number_of_runs, 
            warm_up_time = warm_up_time, 
            sim_duration = sim_duration
        )
        parallelProcess()

        return 1
    else:
        logging.debug('configSim triggered and returning 0')
        return 0

