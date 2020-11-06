import os
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

tsne_2d = pd.read_csv('static/onet_tsne.csv')
dis_activities = pd.read_csv('static/dis_activities.csv')

pick_list = list(tsne_2d.occ)

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [pick_list]],
        value='Accountants and auditors'
    ),
    html.Div(id='display-value'),
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    
    top5 = {}

    for occ in dis_activities:
        temp = dis_activities[occ].sort_values().reset_index().merge(
            tsne_2d.groupby('occ')[['dim_0','dim_1','emp_2018','wage','sqrt_emp'
                               ]].mean(),on='occ',how='inner').head(11)
        top5[occ] = temp
    
    test_case = top5[value]

    fig = px.scatter(test_case, x='dim_0',y='dim_1',
                 title='Occupational Landscape',width=500, height=350)
    
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)