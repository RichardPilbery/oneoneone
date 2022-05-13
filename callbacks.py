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
    Input('dropdown-run-number', 'value')
)
def fig_age_dist(run_number = 999):
    # TODO: Handle case when there is no CSV file yet
    df = pd.read_csv('all_results.csv')
    print('Loaded figures python')

    if run_number is None:
        run_number = 999

    print(f"fig_age_dist called and run number is {run_number}")

    thetitle = "Age distribution for mean of all runs"

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
        thetitle = f"Age distribution for run number {run_number + 1}"

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
        template='plotly_white',
        title = thetitle
    )
    fig.layout['yaxis_title'] =  "Number of patients"
    fig.update_traces(marker_line_width=0.5,marker_line_color="#333")
    return fig

# Populate age dropdown based on the number of runs available
@app.callback(
    Output('dropdown-run-number', 'options'), 
    Output('dropdown-run-number', 'value'),
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

    return thelist, 999






# Update figure to show call activity
@app.callback(
    Output('ooo-call-volume', 'figure'), 
    Input('dropdown-run-number', 'value')
)
def fig_call_vol(run_number = 999):
    # TODO: Handle case when there is no CSV file yet
    df = pd.read_csv('all_results.csv')

    if run_number is None:
        run_number = 999

    print(f"fig_age_dist called and run number is {run_number}")

    thetitle = "111 call volume by hour and day of week"

    call_act = (
        df
        .filter(['P_ID', 'run_number', 'day', 'hour'])
        .drop_duplicates()
        .groupby(['run_number','day', 'hour'], as_index=False)
        .count()
    )

    if(run_number < 999):
        # Just return a single run's data

        call_act = (
            df[df['run_number'] == run_number]
            .filter(['P_ID', 'run_number', 'day', 'hour'])
            .drop_duplicates()
            .groupby(['run_number','day', 'hour'], as_index=False)['P_ID']
            .count()
        )
        thetitle = f"111 call volumes for run number {run_number + 1} by hour and day of week"

    fig = px.histogram(
        call_act, 
        x='hour', 
        y='P_ID',
        histfunc='avg',
        nbins=100,
        labels={
            'hour': 'Hour of the day',
            'P_ID' : 'Number of patients'
        },
        color='day',
        template='plotly_white',
        category_orders={"day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        color_discrete_sequence= px.colors.sequential.Viridis_r,
        title=thetitle
    )
    fig.layout['yaxis_title'] =  "Number of patients"
    fig.update_traces(marker_line_width=0.5,marker_line_color="#333")
    fig.update_layout(legend_title_text="Day of week")
    fig.update_xaxes(tickvals=list(range(0, 24, 1)))
    return fig
