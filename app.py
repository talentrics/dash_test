import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#server = app.server

tsne_2d = pd.read_csv('static/onet_tsne.csv')
dis_activities = pd.read_csv('static/dis_activities.csv')

pick_list = list(tsne_2d.occ)

top5 = {}

for occ in dis_activities:
    
    temp = dis_activities['occ'].sort_values().reset_index().merge(
        tsne_2d.groupby('occ')[['dim_0','dim_1','emp_2018','wage','sqrt_emp'
                           ]].mean(),on='occ',how='inner').head(11)
    top5[occ] = temp

print(top5)

app.layout = html.Div([
    
    html.H2('Testing my app - choose an occupation to get nearest neighbors'),

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
    
    

    new_neighbors = top5[option_slctd]

    fig = px.scatter(new_neighbors,x='dim_0',y='dim_1',
                 hover_data={'sqrt_emp':False,'dim_0':False,
                            'dim_1':False,'emp_2018':False},
                 hover_name='occ',size='wage',
                 title='Occupational Landscape',width=500, height=350)

    fig.update_layout(hoverlabel={'bgcolor':'white','font_size':12,'font_family':'Rockwell'})

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=False)