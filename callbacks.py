from dash import html, Input, Output, DashLogger
from app import app

buttonClickCount = 0

# Sim configuration callback
@app.callback(
    Output('config', 'children'),
    Input('sim_duration', 'value'),
    Input('warm_up_time', 'value'),
    Input('number_of_runs', 'value'),
    Input('run_sim', 'n_clicks')
)
def configSim(sim_duration, warm_up_time, number_of_runs, run_sim, logger: DashLogger):
    global buttonClickCount

    if(run_sim > buttonClickCount):
        # Run the sim
        output = f"Sim duration: {sim_duration}<br/>Warm-up time: {warm_up_time}</br>Number of runs: {number_of_runs}"
        logger.info("Data submitted")
        logger.info(output)
        buttonClickCount = run_sim
        return html.P(output)
