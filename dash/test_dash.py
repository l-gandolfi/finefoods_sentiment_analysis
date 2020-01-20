import pandas as pd
import base64
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent
import average_review
import topic
import plot
import plotly.graph_objs as go

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

image_filename1 = 'screen.PNG'
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())



dataframe = average_review.create_df_year()
score_year = plot.score_by_year()
topic_df = topic.create_df_topic()

def generate_table(data_frame,max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in data_frame.columns])] +

        # Body
        [html.Tr([
            html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
        ]) for i in range(min(len(data_frame), max_rows))]
    )

# Dash app
app = dash.Dash()
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.layout = html.Div([
    dcc.Tabs(id='tabs', style=tabs_styles, children=[
        dcc.Tab(
            label='Score medio',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                html.H1('Evoluzione degli score medi nel tempo',style={'textAlign': 'center','marginTop': '2%'}
                ),

                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure={
                        'data': [
                            go.Bar(
                                x = ['2000','2001', '2002', '2003', '2004','2005','2006','2007','2008','2009','2010', '2011', '2012'],
                                y = [score_year[0],0,0,score_year[1],score_year[2],
                                    score_year[3],score_year[4],score_year[5],score_year[6],
                                    score_year[7],score_year[8],score_year[9],score_year[10]],
                            )
                        ],
                        'layout': go.Layout(
                            title = {'text': 'Andamento dello score medio distribuito sugli anni'},
                            xaxis = {
                               'nticks': 12,
                               'tick0': 2000,
                               'dtick': 1
                            }
                        )
                    }
                )
        ]),

        dcc.Tab(
            label='Lunghezza review',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                html.H1('Evoluzione lunghezza media review nel tempo',style={'textAlign': 'center','marginTop': '2%'}
                ),

                dcc.Dropdown(
                    id='score-dropdown',
                    options=[{'label': i, 'value': i} for i in dataframe.score.unique()],
                    multi=True,
                    value=['1','2','3','4','5']
                ),

                dcc.Graph(id='timeseries-graph')
        ]),

        dcc.Tab(
            label='LDA',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                html.Div([
                    html.H1('Topic di LDA',style={'textAlign': 'center','marginTop': '2%'}
                    ),

                    html.Iframe(src=app.get_asset_url('lda.html'),
                                                        style=dict(position="absolute", left="5", top="5", width="100%", height="100%"))
                ])
            ]
        ),
        dcc.Tab(
            label='ASUM',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                html.Div([
                    html.H1('Topic di ASUM',style={'textAlign': 'center','marginTop': '2%'}
                    ),

                    html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()),
                                    style={
                                            'height': '40%',
                                            'width': '40%'
                                    }),
                    ], style={'width':'100%', 'marginTop':'2%', 'textAlign': 'center'}),

                    dcc.Dropdown(
                        id='asum-dropdown',
                        options=[{'label': i, 'value': i} for i in topic_df.topic.unique()],
                        value=['coffee']
                    ),
                    dash_table.DataTable(id='asum-table',
                                        columns=[{"name": column, "id": column} for column in topic_df.columns],
                                        data = [],
                                        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                        style_cell={
                                            'minWidth': '0px', 'maxWidth': '550px',
                                            'whiteSpace': 'no-wrap',
                                            'overflow': 'hidden',
                                            'whiteSpace': 'normal',
                                            'textOverflow': 'ellipsis',
                                            'fontSize' : 17,
                                            'font-family' : 'sans-serif',
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white'
                                        },
                                        css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                    )

                ])
            ]
        )
    ])
])


@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('score-dropdown', 'value')])

def update_graph(score_values):
    df = dataframe.loc[dataframe['score'].isin(score_values)]

    return {
        'data': [go.Scatter(
            x=df[df['score'] == score]['year'],
            y=df[df['score'] == score]['mean'],
            mode='lines+markers',
            name=score,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
            #ogni chiave del dizionario è lo score praticamente
        ) for score in df.score.unique()],
        'layout': go.Layout(
            title="Lunghezza media review per anno",
            xaxis={'title': 'Anno'},
            yaxis={'title': 'Lunghezza media review'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('asum-table', 'data'),
    [dash.dependencies.Input('asum-dropdown', 'value')])

def update_rows(selected_value):
    dff = topic_df[topic_df['topic'] == str(selected_value)]
    return dff.to_dict("rows")

if __name__ == '__main__':
    app.run_server(debug=True)
