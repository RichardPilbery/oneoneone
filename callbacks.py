from dash import html, Input, Output
from app import app
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE
import logging
from oneoneonedes import parallelProcess, prepStartingVars

buttonClickCount = 0


# 1. User clicks 'Run Simulation button'
# Callback updates trigger_sim value
@app.callback(
    Output('toggle_button', 'value'),
    Input('sim_running', 'value'),
    Input('sim_complete', 'value'),
)
def runSimulation(sim_running, sim_complete):

    logging.debug(f"Button clicked and sim_running is {sim_running} and sim_complete is {sim_complete}")

    if sim_running == 0 and sim_complete == 0:
        return 0
    elif sim_running == 1 and sim_complete == 0:
        return 1
    elif sim_running == 0 and sim_complete == 1:
        return 1


# 2. This will run and control button visibility when either 
# trigger_sim or sim_complete values are changed
@app.callback(
    Output('submit_button', 'style'),
    Output('sim_run_button', 'style'),
    Output('sim_running', 'value'),
    Input('run_sim', 'n_clicks'),
    Input('toggle_button', 'value')
)
def clickButton(run_sim, toggle_button):
    if run_sim or toggle_button == 1:
        logging.debug('Button click, time to hide')
        return HIDE_BUTTON_STYLE, SHOW_BUTTON_STYLE, 1
    else:
        logging.debug('Back to normal button behaviour')
        return  SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, 0


# 3. When trigger sim is set to value = 1, then simulation will run
# When it has finished, sim_complete is set to 1
@app.callback(
    Output('sim_complete', 'value'),
    Input('sim_duration', 'value'),
    Input('warm_up_time', 'value'),
    Input('submit_button', 'style'),
)
def configSim(sim_duration, submit_button_style, warm_up_time, number_of_runs, trigger_sim):
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

