#!/usr/bin/python3

import os, glob
import dash 
from dash import callback, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import time as t
import json
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash import dash_table
from common_components import *
import dash_daq as daq
from dash_data import *

class OverviewPage(object):
    def __init__(self, application_data,app):
        self.application_data = application_data
        self.app = app
        
    def build_op_list_table(self):
        
        my_rows = []
        # build the rows
        for op_id, op_data in self.application_data.op_data.items():
            if op_data.number_bots_saved > 0:
                row = html.Tr([html.Td(html.P(op_id),style={'color':'green'}),html.Td(html.P(op_data.number_gen,style={'color':'green'})) ,html.Td(html.P(op_data.number_bots_saved,style={'color':'green'})),html.Td(html.P(op_data.best_life,style={'color':'green'})) ])
            else:
                row = html.Tr([html.Td(html.P(op_id,style={'color':'red'})),html.Td(html.P(op_data.number_gen,style={'color':'red'})) ,html.Td(html.P(op_data.number_bots_saved,style={'color':'red'})),html.Td(html.P(op_data.best_life,style={'color':'red'})) ])
            my_rows.append(row)



        table_header = [html.Thead(html.Tr([html.Th("Game ID"), html.Th("Generation"), html.Th("Successful Bots"), html.Th("Best Life")]))]
        table_body = [html.Tbody(my_rows)]

        table = dbc.Table(
            
            # using the same table as in the above example
            table_header + table_body,
            id="ov-table",
            bordered=True,
            color="dark",
            hover=True,
            
            # responsive=False,
            striped=True,
            size='sm',
            # style={'background-color':'black'}
            class_name = "big-table"
        )
        return (table)


    def build_overview(self):
        
        layout = html.Div(
            [
            create_navbar(self.app),
       
            html.Br(),
            dbc.Row([
                dbc.Col([html.Div(html.H4("Current Game Results")),html.Div(self.build_op_list_table())],className="big-table"),
                dbc.Col([daq.Gauge(id='my-gauge-1',label="Number Bots",value=6, max=10000)]),
                dbc.Col([html.Div(daq.Gauge(id='my-gauge-2',label="Number Games",value=6,max=1000))])
            ]),
            # html.Div([render_ov_plots()])
            html.Br(),
            html.Div(children=[], id="ov-fitness-plots"),
                dcc.Interval(
                id='interval-component', 
                interval=1*2000, # in milliseconds
                n_intervals=0
            )
            ]
        )
        
        return layout

@callback([Output('my-gauge-1', 'value'),Output('my-gauge-2', 'value')], Input('interval-component', 'n_intervals'))
def update_output(value):
    application_data = None
    application_data = IDentData()
    application_data.GetOpIds()
    application_data.SetActiveOptimisation(optimisation_id=application_data.optimisation_ids[0])
    application_data.BuildFrameworkOverview()
    number_games = application_data.number_games
    number_bots = application_data.number_bots_total
    
    return [number_bots,number_games]

@callback(Output('ov-fitness-plots', 'children'),Input('interval-component', 'n_intervals'))
def update_plots(n_intervals):
    application_data = None
    application_data = IDentData()
    application_data.GetOpIds()
    application_data.SetActiveOptimisation(optimisation_id=application_data.optimisation_ids[0])
    application_data.BuildFrameworkOverview()
    rows = []
    if application_data is not None:
        print('Updating plots')
        
        
        
        cols = []
        col_id = 1
        number_cols = 3
        for op_id, op_data in application_data.op_data.items():
            
        
            if  len(application_data.op_data[op_id].best_fitness) < 10:
                continue
        
            df = pd.DataFrame(dict(
                generation = application_data.op_data[op_id].gen_num,
                fitness = application_data.op_data[op_id].best_fitness
            ))


        
            fig = px.line(df, x='generation', y='fitness', title=f'Best Fitness Profile [ {op_id} ]',template='plotly_dark')
            fig.update_layout(
                    plot_bgcolor="black",  # Color inside the axes
                    paper_bgcolor="black",  # Color outside the axes/entire figure background
                    xaxis=dict(
                        title=None,
                        showgrid=False,
                        showline=False,
                    ), 
                    yaxis=dict(
                        title=None,
                        showgrid=False,
                        showline=False,

                    )
                    
                )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            
            fig.update_traces(line_color='green')
            fig.update_traces(marker_line_width=0)
            info_row = dbc.Row([dbc.Col([html.H5(f'Births [ {op_data.number_bots_saved} ]')]),dbc.Col([html.H5(f'Best Life [ {op_data.best_life} ]')]),dbc.Col([dcc.Link(dbc.Button("View Game", color="success"), href=f"/game?op_id={op_id}")])])
            col = dbc.Col(html.Div([dcc.Graph(id = f"{op_id}_ov_fitness", figure=fig),info_row]))
            cols.append(col)
            
            if col_id % number_cols == 0:
                row = dbc.Row(cols)
                rows.append(row)
                cols = []
                col_id = 1
                
                continue

                
            
                
            
            
            col_id += 1 
            
        
            
    
    return (rows)
    # return plot
        