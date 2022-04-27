from dash import html, Input, Output, State
from app import app, long_callback_manager
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE
import logging
from oneoneonedes import parallelProcess, prepStartingVars



# 3. When trigger sim is set to value = 1, then simulation will run
# When it has finished, sim_complete is set to 1
@app.long_callback(
    output = Output('sim_complete', 'value'),
    inputs = (
        Input('run_sim', 'n_clicks'),
        State('sim_duration', 'value'),
        State('warm_up_time', 'value'),
        State('number_of_runs', 'value'),
    ),
    running = [
        (Output('submit_button', 'style'), HIDE_BUTTON_STYLE, SHOW_BUTTON_STYLE),
        (Output('sim_run_button', 'style'), SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE),
    ],
    manager = long_callback_manager,
    prevent_initial_call = True
)
def configSim(run_sim, sim_duration, warm_up_time, number_of_runs):
        # Run the sim
        logging.debug("Run the sim")
        
        prepStartingVars(
            number_of_runs = number_of_runs, 
            warm_up_time = warm_up_time, 
            sim_duration = sim_duration
        )
        parallelProcess()

        return 1


