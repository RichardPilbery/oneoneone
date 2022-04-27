from dash import html, Input, Output
from app import app
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE
import logging
from oneoneonedes import parallelProcess, prepStartingVars

buttonClickCount = 0

# Sim configuration callback
@app.callback(
    Output('sim_complete', 'value'),
    Input('sim_duration', 'value'),
    Input('warm_up_time', 'value'),
    Input('number_of_runs', 'value'),
    Input('trigger_sim', 'value')
)
def configSim(sim_duration, warm_up_time, number_of_runs, trigger_sim):
    if trigger_sim == 1:
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
        return 0


@app.callback(
    Output('submit_button', 'style'),
    Output('sim_run_button', 'style'),
    Output('trigger_sim', 'value'),
    Input('run_sim', 'n_clicks'),
    Input('sim_complete', 'value')
)
def buttonToggle(run_sim, sim_complete):
    global buttonClickCount

    logging.debug(f"Button clicked and run_sim is {run_sim} and buttonClickCount is {buttonClickCount} and statusMessage is {sim_complete}")

    if run_sim > buttonClickCount:
        buttonClickCount = run_sim
        return  HIDE_BUTTON_STYLE, SHOW_BUTTON_STYLE, 1
    else:
        return  SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, 0


