import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('1.csv')

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard"),
    
    # Dropdown for selecting variables
    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': 'X Axis', 'value': 'x'},
            {'label': 'Y Axis', 'value': 'y'},
            {'label': 'Z Axis', 'value': 'z'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all',  # Default value
        multi=False
    ),
    
    # Input for selecting the number of samples
    html.Label('Number of samples to display:'),
    dcc.Input(id='num-samples', type='number', value=len(df)),
    
    # Graph for displaying the data
    dcc.Graph(id='gyroscope-graph'),
    
    # Buttons for navigating data samples
    html.Button('Previous', id='prev-button'),
    html.Button('Next', id='next-button'),

    # Table for displaying statistical summary
    html.Div(id='stats-summary')
])

@app.callback(
    [Output('gyroscope-graph', 'figure'),
     Output('stats-summary', 'children')],
    [Input('variable-dropdown', 'value'),
     Input('num-samples', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')]
)
def update_graph(selected_var, num_samples, prev_clicks, next_clicks):
    # Logic to handle the current sample range
    start_idx = 0  # Replace with logic to handle sample range
    end_idx = num_samples

    if selected_var == 'all':
        fig = px.line(df.iloc[start_idx:end_idx], x='timestamp', y=['x', 'y', 'z'])
    else:
        fig = px.line(df.iloc[start_idx:end_idx], x='timestamp', y=selected_var)
    
    # Generate a statistical summary (mean, min, max)
    summary = df.iloc[start_idx:end_idx][['x', 'y', 'z']].describe().to_dict()
    summary_table = html.Table([
        html.Tr([html.Th(col) for col in summary.keys()]),
        html.Tr([html.Td(summary[col]['mean']) for col in summary.keys()]),
        html.Tr([html.Td(summary[col]['min']) for col in summary.keys()]),
        html.Tr([html.Td(summary[col]['max']) for col in summary.keys()])
    ])

    return fig, summary_table

if __name__ == '__main__':
    app.run_server(debug=True)
