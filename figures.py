import pandas as pd
import plotly.express as px

df = pd.read_csv('all_results.csv')

def fig_age_dist(run_number = 999):
    global df

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
    return fig.show()