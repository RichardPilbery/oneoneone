from dash import html, Input, Output
from app import app
import logging
from oneoneonedes import parallelProcess, prepStartingVars

buttonClickCount = 0

# Sim configuration callback
@app.callback(
    Output('status_message', 'value'),
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

        return "Simulation has run"
    else:
        return ""


@app.callback(
    Output('submit_button', 'style'),
    Output('sim_run_button', 'style'),
    Output('trigger_sim', 'value'),
    Input('run_sim', 'n_clicks')
)
def buttonToggle(run_sim):
    global buttonClickCount

    logging.debug(f"Button clicked and run_sim is {run_sim} and buttonClickCount is {buttonClickCount}")
    if run_sim > buttonClickCount:
        buttonClickCount = run_sim
        return  [{'display':'none'}, {'display:block'}, 1]
    else:
        return  [{'display':'block'}, {'display:none'}, 0]


