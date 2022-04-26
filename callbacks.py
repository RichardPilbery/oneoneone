from dash import html, Input, Output
from app import app
import logging
from oneoneonedes import parallelProcess, prepStartingVars

buttonClickCount = 0

# Sim configuration callback
@app.callback(
    Output('submit_button', 'style'),
    Output('sim_run_button', 'style'),
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

        prepStartingVars(
            number_of_runs = number_of_runs, 
            warm_up_time = warm_up_time, 
            sim_duration = sim_duration
        )
        parallelProcess()

        return {'display:block'}, {'display':'none'}


@app.callback(
    Output('submit_button', 'style'),
    Output('sim_run_button', 'style'),
    Input('run_sim', 'n_clicks')
)
def configSim(run_sim):

    return  {'display':'none'}, {'display:block'}



