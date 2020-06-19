import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('Job1.csv', header=[0,1])
df.index = df['Questions']
df.drop(['Questions'], axis=1, inplace=True)

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

colors = {'background':'rgb(30,30,30)', 'text':'rgb(250,250,250'}

# Age bar chart to be embedded into dash 
age_bar = dcc.Graph(id='age',
                  figure={'data': [
                                  go.Bar(
                                          x=df['Question 1'].columns.values,
                                          y=df.iloc[-1, :]['Question 1'])],
                        'layout':
                                 go.Layout(title=dict(text ='Age',
                                                       font = dict(size=14,
                                                                   color = 'white')),
                                           paper_bgcolor='rgb(50,50,55)',
                                           plot_bgcolor='rgb(60,60,75)',
                                           xaxis=dict(tickfont=dict(color='white')
                                                      ),
                                           yaxis=dict(tickfont=dict(color='white'),
                                                      dtick=1, # No decimals
                                                      gridcolor='rgb(70,70,70)'), # gridlines
                                           ) 
                        })

# Ethnicity pie chart to be embedded into dash 
ethnic_pie = dcc.Graph(id='ethnicity',
                  figure={'data': [
                                  go.Pie(
                                          labels=df['Question 5'].columns.values,
                                          values=df.iloc[-1, :]['Question 5'],
                                          hole=0.4)],
                         'layout':
                                  go.Layout(title=dict(text ='Ethnicity',
                                                       font = dict(size=14,
                                                                   color = 'white'),
                                                       y=0.9),
                                            paper_bgcolor='rgb(50,50,55)',
                                            plot_bgcolor='white',
                                            legend=dict(x=-0.5,
                                                        y=-1,
                                                        font = dict(color='white',
                                                                    size=10)
                                                        ),
                                            margin=dict(l=100,
                                                        r=100,
                                                        t=100,
                                                        b=100)
                                            )
                        },
                )

orientation_pie = dcc.Graph(id='orientation',
                  figure={'data': [
                                  go.Pie(
                                          labels=df['Question 7'].columns.values,
                                          values=df.iloc[-1, :]['Question 7'],
                                          hole=0.4)],
                         'layout':
                                  go.Layout(title=dict(text ='Orientation',
                                                       font = dict(size=14,
                                                                   color = 'white'),
                                                       y=0.9),
                                            paper_bgcolor='rgb(50,50,55)',
                                            plot_bgcolor='white',
                                            legend=dict(x=-0.5,
                                                        y=-1,
                                                        font = dict(color='white',
                                                                    size=10)
                                                        ),
                                            margin=dict(l=100,
                                                        r=100,
                                                        t=100,
                                                        b=100)
                                            )
                        },
                )

# First row of dashboard
row1 = html.Div(
        [
            dbc.Row(
                    [
                     dbc.Col(html.Div(age_bar), width=8),
                     dbc.Col(html.Div(ethnic_pie), width=4),
                     ]
                     )
        ])

# Second row of dashboard
row2 = html.Div(
        [
            dbc.Row(
                    [
                     dbc.Col(html.Div('Col 1, Row 2'), width=8),
                     dbc.Col(html.Div(orientation_pie), width=4),
                     ]
                     )
        ])

# App layout
app.layout = dbc.Container([
                    dbc.Row(dbc.Col(html.H1('E&D Dashboard Template'), width=dict(size=6,
                                                                       offset=4)
                            )),
                    html.Hr(), # Break for padding
                    row1,
                    html.Hr(), # Break for padding
                    row2,
                        ])
                                          
if __name__ == '__main__':
    app.run_server()