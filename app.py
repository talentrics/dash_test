import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

tsne_2d = pd.read_csv('static/onet_tsne.csv')

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    fig = px.scatter(tsne_2d.dropna().rename(columns={0:'dim_0',1:'dim_1'}),
                 x='dim_0',y='dim_1',hover_data={'sqrt_emp':False,'dim_0':False,
                                                          'dim_1':False,'emp_2018':False},
                 hover_name='occ',size='sqrt_emp',
                 title='Occupational Landscape',width=1000, height=700)
    fig.update_layout(hoverlabel={'bgcolor':'white','font_size':16,'font_family':'Rockwell'})
    return fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)