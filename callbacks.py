from dash import html, Input, Output, State
from app import app, long_callback_manager
from layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE
import logging
from oneoneonedes import parallelProcess, prepStartingVars
import pandas as pd
import plotly.express as px

buttonClickCount = 0

# 3. When trigger sim is set to value = 1, then simulation will run
# When it has finished, sim_complete is set to 1
@app.long_callback(
    output = (
        Output('sim_complete', 'value'),
        Output('store-num-runs', 'data')
    ),
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

        global buttonClickCount

        if run_sim > buttonClickCount:
            logging.debug('run_sum > buttonClickCount')
            buttonClickCount = run_sim
            prepStartingVars(
                number_of_runs = number_of_runs, 
                warm_up_time = warm_up_time, 
                sim_duration = sim_duration
            )
            parallelProcess()

            return 1, number_of_runs
        else:
            return 0, number_of_runs



# Update figure based on run number chosen
@app.callback(
    Output('age-dist', 'figure'), 
    Input('age-dist-run-number', 'value')
)
def fig_age_dist(run_number = 999):
    # TODO: Handle case when there is no CSV file yet
    df = pd.read_csv('all_results.csv')
    print('Loaded figures python')

    if run_number is None:
        run_number = 999

    print(f"fig_age_dist called and run number is {run_number}")

    y_label = "Mean number of patients"

    age_wrangle = (
        df[['run_number','P_ID', 'age', 'sex', 'GP']]
        .drop_duplicates()
        .groupby(['run_number','age'], as_index=False)['P_ID']
        .count()
    )

    if(run_number < 999):
        # Just return a single run's data

        age_wrangle = (
            df[df['run_number'] == run_number]
            .filter(['P_ID','age'])
            .drop_duplicates()
            .groupby(['age'], as_index=False)['P_ID']
            .count()
        )
        y_label = f"Number of patients for run number {run_number}"

    fig = px.histogram(
        age_wrangle, 
        x='age', 
        y='P_ID',
        histfunc='avg',
        nbins=100,
        labels={
            'age': 'Patient age in years',
            'P_ID' : 'Number of patients'
        },
        template='plotly_white'
    )
    fig.layout['yaxis_title'] =  y_label
    fig.update_traces(marker_line_width=0.5,marker_line_color="#333")
    return fig

# Populate age dropdown based on the number of runs available
@app.callback(
    Output('age-dist-run-number', 'options'), 
    Input('url', 'pathname'),
    State('store-num-runs', 'data'),
)
def dropdown_run_number(url, num_runs):
    print('Dropdown run number')

    if num_runs is None:
        num_runs = 1
    else:
        num_runs = int(num_runs)

    keys = list(range(0,num_runs))
    thelist = [{'label': 'mean', 'value': 999}]
    for i in keys:
        thelist.append({'label':i+1, 'value':i})

    return thelist
