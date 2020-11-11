import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

server = app.server

tsne_2d = pd.read_csv('static/onet_tsne.csv')
dis_activities = pd.read_csv('static/dis_activities.csv')
test_case = pd.read_csv('static/test_case.csv')

pick_list = list(tsne_2d.occ)

fig = px.scatter(tsne_2d.dropna().rename(columns={0:'dim_0',1:'dim_1'}),
                 x='dim_0',y='dim_1',hover_data={'sqrt_emp':False,'dim_0':False,
                                                          'dim_1':False,'emp_2018':False},
                 hover_name='occ',size='sqrt_emp',
                 title='Occupational Landscape',width=1000, height=700)
    fig.update_layout(hoverlabel={'bgcolor':'white','font_size':16,'font_family':'Rockwell'})

app.layout = html.Div([
    
    html.H2('Testing my app - choose an occupation to get nearest neighbors'),

    dcc.Graph(fig)

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in pick_list],
        #value='Choreographers',
        style={'width': "50%"}
                                ),
    
    html.Div(id='output_container', children = []),
    
    html.Br(),

    dcc.Graph(id = 'my_plot', figure = {})

    ])

@app.callback([dash.dependencies.Output(component_id='output_container', component_property='children'),
     dash.dependencies.Output(component_id='my_plot', component_property='figure')],
    [dash.dependencies.Input(component_id='dropdown', component_property='value')])

def update_graph(option_slctd):
    
    print(option_slctd)
    print(type(option_slctd))

    container = "The value chosen by user was: {}".format(option_slctd)

    fig2 = px.scatter(test_case,x='dim_0',y='dim_1',
                 hover_data={'sqrt_emp':False,'dim_0':False,
                            'dim_1':False,'emp_2018':False},
                 hover_name='occ',size='wage',
                 title='Occupational Landscape',width=500, height=350)
    fig2.update_layout(hoverlabel={'bgcolor':'white','font_size':12,'font_family':'Rockwell'})

    return container, fig2

if __name__ == '__main__':
    app.run_server(debug=False)