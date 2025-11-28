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

class ViewBotPage(object):
    def __init__(self, application_data,app, bot_id):
        self.application_data = application_data
        self.app = app
        self.benchmark_data = None
        self.bot_id = bot_id


    def build_benchmark_ov_table(self, filter={}):
        number_rows = 0
        my_rows = []
        # build the rows
        for bot_bm_data in self.benchmark_data.rank_data['bot_runs'][self.bot_id]:
            success_rate = 0.0
            # if (int(bot_bm_data['success'])+int(bot_bm_data['fail'])) > 0:
            #     success_rate = (float(int(bot_bm_data['success']))/(int(bot_bm_data['success'])+int(bot_bm_data['fail']))) * 100
            
            
            if int(bot_bm_data['number_success']) >  int(bot_bm_data['number_fail']):
                row = html.Tr([html.Td(html.P(bot_bm_data['filename'],style={'color':'white'})) ,html.Td(html.P(bot_bm_data['target'],style={'color':'green'})),html.Td(dbc.Progress(value=float(bot_bm_data['precision']),color="success")) , html.Td(dbc.Progress(value=bot_bm_data['accuracy'],color="success")), html.Td(dbc.Progress(value=bot_bm_data['recall'],color="success"),style={'color':'green'}),html.Td(html.P(bot_bm_data['number_success'],style={'color':'green'})) , html.Td(html.P(bot_bm_data['number_fail'],style={'color':'green'})),html.Td(html.P(bot_bm_data['number_frames'],style={'color':'green'})),html.Td(html.A("View Bot", href=viewBotURL(self.bot_id), target="_blank",style={'color':'white'})),html.Td(html.A("Energy", href=viewRunURL(bot_bm_data['filename'], bot_bm_data['run_id'], self.bot_id, "energy"), target="_blank",style={'color':'white'})), html.Td(html.A("Decisions", href=viewRunURL(bot_bm_data['filename'], bot_bm_data['run_id'], self.bot_id, "decisions"), target="_blank",style={'color':'white'}))])
            else:
                 row = html.Tr([html.Td(html.P(bot_bm_data['filename'],style={'color':'white'})) ,html.Td(html.P(bot_bm_data['target'],style={'color':'red'})) ,html.Td(dbc.Progress(value=float(bot_bm_data['precision']),color="error")),html.Td(dbc.Progress(value=bot_bm_data['accuracy'],color="error")),html.Td(dbc.Progress(value=bot_bm_data['recall'],color="error")),html.Td(html.P(bot_bm_data['number_success'],style={'color':'red'})),html.Td(html.P(bot_bm_data['number_fail'],style={'color':'red'})) , html.Td(html.P(bot_bm_data['number_frames'],style={'color':'red'})),html.Td(html.A("View Bot", href=viewBotURL(self.bot_id), target="_blank",style={'color':'white'})),html.Td(html.A("Energy", href=viewRunURL(bot_bm_data['filename'], bot_bm_data['run_id'], self.bot_id, "energy"), target="_blank",style={'color':'white'})),html.Td(html.A("Decisions", href=viewRunURL(bot_bm_data['filename'], bot_bm_data['run_id'], self.bot_id, "decisions"), target="_blank",style={'color':'white'}))])
            my_rows.append(row)

            number_rows+=1
            if number_rows > 300:
                break


        table_header = [html.Thead(html.Tr([html.Th("Filename"), html.Th("Target"),  html.Th("Precision"),html.Th("Accuracy"), html.Th("Recall"), html.Th("Success"), html.Th("Fail"), html.Th("Number Frames"), html.Th("Details") ]))]
        table_body = [html.Tbody(my_rows)]

        table = dbc.Table(
            
            # using the same table as in the above example
            table_header + table_body,
            id="ov-table",
            bordered=True,
            
            hover=True,
            
            responsive=False,
            striped=True,
            size='sm',
            # style={"background-color":"black"},
            color="dark",
            # class_name = "big-table"
        )
        return (table)

    def build_card(self,title, value):
        
        card = dbc.Card(
            [
                # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                dbc.CardBody(
                    [
                        html.H4(title, className="card-title", style={'color' : 'white'}),
                        html.P(
                            value,
                            className="card-text",
                            style={'color' : 'whitesmoke', 'font-size':'20px'}
                        ),
                        # dbc.Button("Go somewhere", color="primary"),
                    ]
                ),
            ],
            style={"width": "18rem", "backgroud-color":"black"},
            color="black"
        )
        
        return card

    def build_bot_page(self, filter = {}):
        
        # build benchmark data
        # if self.benchmark_data == None:
        #     self.benchmark_data = BenchmarkOverviewData()
        #     self.benchmark_data.build_data()
        
        self.benchmark_data = BenchmarkOverviewData()
        self.benchmark_data.load_data()
       
        layout = html.Div(
            [
            create_navbar(self.app),
            html.Br(),
            # benchmark overview
            html.H2(f'{self.bot_id}'),
            html.Hr(),
            html.Br(),
            html.H3("Overview"),
            html.Br(),
            dbc.Row([
                
                
                dbc.Col(self.build_card("Number Frames", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["number_frames"])),
                dbc.Col(self.build_card("Number Labels", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["number_labels"])),
                dbc.Col(self.build_card("Number Files", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["number_labels"])),
                dbc.Col(self.build_card("Number Label Hit", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["number_labels_hit"]))
                
                
            ]),
            dbc.Row([
                dbc.Col(self.build_card("Number Decisions", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["number_decisions"])),
                dbc.Col(self.build_card("Accuracy (%)", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["accuracy"])),
                dbc.Col(self.build_card("Precision (%)", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["precision"])),
                dbc.Col(self.build_card("Recall (%)", self.benchmark_data.rank_data['bot_ov'][self.bot_id]["recall"])) 
            ]),
            html.Br(),
            # table
            html.H3("IDent Bots"),
            html.Br(),
            dbc.Row([html.Div(self.build_benchmark_ov_table())])
            ]
        )
        
        return layout
