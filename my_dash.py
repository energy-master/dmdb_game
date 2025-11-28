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


import vizro

from dash_data import *




# ------------ COMPONENETS ------------------

def build_op_list_table():

    my_rows = []
    # build the rows
    for op_id, op_data in application_data.op_data.items():
        row = html.Tr([html.Td(op_id)])
        my_rows.append(row)
   

    table_body = [html.Tbody(my_rows)]

    table = dbc.Table(
        # using the same table as in the above example
        table_body,
        bordered=True,
        color="light",
        hover=True,
        responsive=True,
        striped=True,
        size='sm',
        class_name = "big-table"
    )
    return (table)

badge = dbc.Button(
    [
        "Notifications",
        dbc.Badge("4", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

title = html.Div(
    className = 'title-div',
    children = [
        html.H2('IDent Learn | ', className="float-left"),
        html.H5('Powered by', className="float-left"),
        html.H2('brahma',  className="brahma-title")
    ]
    )

   

# ========= LAYOUT ==============


def render_ov_plots():
    """render_ov_plots Build a grid of plots
    """
    
    grid = None
    rows = []
    number_cols = 3
    col_id = 1
    cols = []
    for op_id, op_data in application_data.op_data.items():
        
        col = dbc.Col(html.Div([dcc.Graph(id = f"{op_id}_ov_fitness")]))
        cols.append(col)
        
        if col_id % number_cols == 0:
            row = dbc.Row(cols)
            rows.append(row)
            cols = []
            col_id = 1
            continue
            
           
        
        col_id += 1 
    
   
    grid = html.Div(children = rows, id="ov-fitness-plots")
    
    return grid
    

def build_landing_page(app_data=None):
    
    layout = html.Div(
        [
        create_navbar(),
       
        html.Br(),
        dbc.Row(build_op_list_table(), className="big-table"),
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
    
def renderPage(app=None, layout=None):
    
    
    
    # app.layout = dbc.Container(html.Div([
        
    #     html.Br(),
    #     html.H1("IDent Learn Dash"),
    #     html.Div('Powered by brahma ML framework for acoustic signals'),
    #     html.H4(id='optimisation-id-title'),
    #     (dcc.Dropdown(app_data.optimisation_ids, '72001696', id='optimisation-id-dropdown')),
    #     dcc.Graph(id = "live-update-graph"),
    #     dbc.Row(build_table()),
        
    #     dcc.Interval(
    #         id='interval-component', 
    #         interval=1*5000, # in milliseconds
    #         n_intervals=0
    #     )
    # ]))
    
    app.layout = layout


# ======= CALL BACKS ==============

@callback(Output('ov-fitness-plots', 'children'),Input('interval-component', 'n_intervals'))
def update_plots(n_intervals):
    print('Updating plots')
    application_data.GetOpIds()
    application_data.BuildFrameworkOverview()
    
    rows = []
    cols = []
    col_id = 1
    number_cols = 3
    for op_id, op_data in application_data.op_data.items():
        
    
        df = pd.DataFrame(dict(
            generation = application_data.op_data[op_id].gen_num,
            fitness = application_data.op_data[op_id].best_fitness
        ))
       
        fig = px.line(df, x='generation', y='fitness', title=f'Best Fitness Profile {op_id}')

        col = dbc.Col(html.Div([dcc.Graph(id = f"{op_id}_ov_fitness", figure=fig)]))
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
    
@callback(
    Output('optimisation-id-title', 'children'),
    Input('optimisation-id-dropdown', 'value')
    ) 
def optimisation_id_selected(value):
    application_data.SetActiveOptimisation(optimisation_id=value)
    return (f'ID: {value}')



if __name__=="__main__":
    
    
    application_data = IDentData()
    application_data.GetOpIds()
    application_data.SetActiveOptimisation(optimisation_id=application_data.optimisation_ids[0])
    application_data.BuildFrameworkOverview()
    
    layout = build_landing_page(application_data)
    # app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
    app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
    renderPage(app, layout=layout)
    
    app.run(port=4040, debug=True)
    
    
