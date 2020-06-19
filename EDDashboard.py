import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('Job1.csv', header=[0,1])
df.index = df['Questions']
df.drop(['Questions'], axis=1, inplace=True)

age = df['Question 1']

app = dash.Dash()

colors = {'background':'rgb(30,30,30)', 'text':'rgb(250,250,250'}

app.layout = html.Div(children=[
                        html.H1('Dashboard for : ', style={'textAlign':'center',
                                                           'color':colors['text'],
                                                           'font':'Arial'}),

                        
                        html.Div(dcc.Graph(id='age',
                                      figure={'data': [
                                                      go.Bar(
                                                              x=df['Question 1'].columns.values,
                                                              y=df.iloc[-1, :]['Question 1'])],
                                            'layout':
                                                     go.Layout(title='Age',
                                                               paper_bgcolor='rgb(40,40,40)',
                                                               plot_bgcolor='rgb(60,60,60)')
                                            },
                                    ),
                                style={'width':'49%'}
                                ),
                                                      
                        html.Div(dcc.Graph(id='ethnicity',
                                      figure={'data': [
                                                      go.Pie(
                                                              labels=df['Question 5'].columns.values,
                                                              values=df.iloc[-1, :]['Question 5'],
                                                              hole=0.4)],
                                             'layout':
                                                      go.Layout(title='Ethnicity',
                                                                paper_bgcolor='rgb(40,40,40)',
                                                                plot_bgcolor='white')
                                            },
                                    ),
                                style={'width':'49%'}
                                ),
                        
                        dcc.Graph()
                                ],
                        style={'backgroundColor': colors['background']}
)

if __name__ == '__main__':
    app.run_server()