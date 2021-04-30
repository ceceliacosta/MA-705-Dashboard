## default of all, one or the other, text search for actor


from typing import final
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table
import numpy as np
import ast


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

use = '''Use this dashboard to find information on the Top 250 IMdB Movies based off of the following:'''

#ref = '''Here is a list of data sources and references used in this course project.'''


file = 'https://raw.githubusercontent.com/ceceliacosta/MA-705-Dashboard/main/testing_file.csv'
df = pd.read_csv(file, encoding='Latin-1')

# format links
#def f(row):
 #   l = "[{0}]({0})".format(row["url"])
  #  return l
#df["link"] = df.apply(f, axis=1)

# dropdown categories
genre = df['Genres'].unique().tolist()
final_genres = []
for genres in df['Genres']:
    final_genres = final_genres+ast.literal_eval(genres)
final_genres= list(set(final_genres))
final_genres.sort()

years = df['Year'].unique().tolist()
years.sort()

df['Cast']=df['Cast'].apply(lambda x: (',').join(x.replace("'","").strip("][").split(',')[:10]))
df['Directors']= df['Directors'].apply(lambda x: x.replace("'","").strip("][").split(','))
df['Genres']= df['Genres'].apply(lambda x: (',').join(x.replace("'","").strip("][").split(',')))

PAGE_SIZE = 10

app.layout = html.Div([
    html.Div([],
             style={'width': '5%', 'display': 'inline-block'}),
    html.Div([
        html.Div([html.Br(),
            html.H1('IMdB Top 250 Movies Dashboard', style={'color':'#FFDA33', 'textAlign': 'center'}),
          #  html.H3('Cecelia Costa', style={'textAlign': 'left'}),
            html.H3('About', style={'color':'#FFDA33', 'textAlign': 'center'}),
            html.H6('Use this dashboard to find information on the Top 250 IMdB Movies based off of genre and/or year and see', style={'color':'#949494','textAlign': 'center'}),
            html.H6('Title | Genres | Year | Directors | Cast | Rating', style={'color':'#949494','textAlign': 'center'}),
        ]),

        html.Hr(),

        html.Div([
            html.B('Select a category to display corresponding movies *Default is Top 10 Movies*', style={'color':'#FFDA33', 'textAlign': 'left'})],
            style={'width': '50%'}
        ),
        html.Div([
            html.Br(),
            
            html.Label("Select a genre "),
            dcc.Dropdown(id='genre_filter_dropdown',
                        placeholder='Select genre...',
                        options=[{'label':g, 'value':g} for g in final_genres],
                        style={'color':'#FFDA33', 'textAlign': 'center'}),
            html.Br(),
            html.Label("Select a year "),
            dcc.Dropdown(id='year_filter_dropdown',
                        placeholder='Select year...',
                        options=[{'label':y, 'value':y} for y in years],
                        style={'color':'#FFDA33', 'textAlign': 'center'})],
            style={'width': '25%'}
        ),
        html.Br(),
        dcc.Graph(id='fig_bar'),

        html.Br(),
        html.Hr(),
        html.H3('Movie Information', style={'color':'#FFDA33', 'textAlign': 'center'}),
        html.Div(className="row",
                children=[
                    html.Div(dt.DataTable(
                        style_cell= {'textAlign':'left','whiteSpace':'normal','height': 'auto'}, 
                        id='table-paging-with-graph', 
                        columns=[
                            dict(name='Title', id='Title', type='text'),
                            dict(name='Genres', id='Genres', type='text'),
                            dict(name='Year', id='Year', type='numeric'),
                            dict(name='Directors', id='Directors', type='text'),
                            dict(name='Top 10 Cast Members', id='Cast', type='text'),
                            dict(name='Rating', id='Rating', type='text'),
                        ]
                    ),
                    style={'fontSize': '11', 'textAlign': 'left', 'width': '99%', 'display': 'inline-block', 'overflowY': 'scroll'})
        ]),

        html.Hr(),
        html.B('References:', style={'color': '#FFDA33', 'textAlign': 'left'}),

        html.Section(['- Dash Plotly: ', html.A('http://dash.plotly.com/', href='http://dash.plotly.com/')]),
        html.Br(),
        html.Footer('Cecelia Costa, MA 705, April 2021.')
    ], style={'width': '90%', 'display': 'inline-block'})
])




@app.callback(
    Output('table-paging-with-graph', 'data'),
    Input('genre_filter_dropdown', 'value'),
    Input('year_filter_dropdown', 'value'))
    

def update_table(genre, year):
    if not genre and not year:
        dff=df.head(10)
    elif genre and not year:
        dff= df[df['Genres'].str.contains(genre, na=False)]
    elif year and not genre:
        dff = df[df['Year']==year]
    else:
        dff = df[(df['Year']==year) & (df['Genres'].str.contains(genre, na=False))]

    dff.sort_values('Rating')
    
    return dff.to_dict('records')


@app.callback(
    Output(component_id='fig_bar', component_property='figure'),
    Input('genre_filter_dropdown', 'value'),
    Input('year_filter_dropdown', 'value'))

def update_graph(genre, year):

    if not genre and not year:
        dff= df.head(10)
    elif genre and not year:
        dff= df[df['Genres'].str.contains(genre, na=False)]
    elif year and not genre:
        dff = df[df['Year']==year]
    else:
        dff = df[(df['Year']==year) & (df['Genres'].str.contains(genre, na=False))]
   
    if dff.empty:
        fig = {
            'layout': {
                'xaxis': {
                    'visible': False
                },
                'yaxis': {
                    'visible': False
                },
                'annotations': [
                    {
                        'text': 'No '+ genre + ' movies from ' + str(year) + '  :(',
                        'xref': 'paper',
                        'yref': 'paper',
                        'showarrow': False,
                        'font': {
                            'size': 28
                        }
                    }
                ]
            }
        }
    else:
        fig = px.bar(dff, x=dff['Title'], y= dff['Rating'], color_discrete_sequence=['indianred'])
        fig.update_layout(xaxis_title= 'Movie Title')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)