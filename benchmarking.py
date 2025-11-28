#!/usr/bin/python3

import os, glob
import dash 
from dash import callback, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import time as t
from datetime import datetime,timezone
import json
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash import dash_table
from common_components import *
import dash_daq as daq
from dash_data import *

class BenchmarkingPage(object):
    def __init__(self, application_data,app):
        self.application_data = application_data
        self.app = app
        self.benchmark_data = None
        


    def build_benchmark_ov_table(self, filter={}):
        number_rows = 0
        my_rows = []
        # build the rows
        for bot_id, bot_bm_data in self.benchmark_data.rank_data['bot_ov'].items():
            success_rate = 0.0
            if (int(bot_bm_data['success'])+int(bot_bm_data['fail'])) > 0:
                success_rate = (float(int(bot_bm_data['success']))/(int(bot_bm_data['success'])+int(bot_bm_data['fail']))) * 100
            
            
            if int(bot_bm_data['success']) >  int(bot_bm_data['fail']):
                row = html.Tr([html.Td(html.P(bot_id),style={'color':'green'}),html.Td(html.P(bot_bm_data['targets'],style={'color':'green'})),html.Td(dbc.Progress(value=success_rate,color="success")) , html.Td(dbc.Progress(value=bot_bm_data['pc_labels_hit'],color="success")), html.Td(html.P(bot_bm_data['number_files_run'],style={'color':'green'})),html.Td(html.P(bot_bm_data['success'],style={'color':'green'})) , html.Td(html.P(bot_bm_data['fail'],style={'color':'green'})),html.Td(html.P(bot_bm_data['number_frames'],style={'color':'green'})),html.Td(html.A("View Bot", href=viewBotURL(bot_id), target="_blank",style={'color':'white'}),style={'color':'white'}),html.Td(dcc.Link(dbc.Button("Details", color="success"), href=f"/view_bot_bm?op_id={bot_id}")),html.Td(dcc.Link(dbc.Button("Run", color="success"), href=f"/view_bot_id?op_id={bot_id}")) ],style={"background-color":"black"})
            else:
                 row = html.Tr([html.Td(html.P(bot_id),style={'color':'red'}),html.Td(html.P(bot_bm_data['targets'],style={'color':'red'})) ,html.Td(dbc.Progress(value=success_rate,color="error")),html.Td(dbc.Progress(value=bot_bm_data['pc_labels_hit'],color="error")),html.Td(html.P(bot_bm_data['number_files_run'],style={'color':'red'})),html.Td(html.P(bot_bm_data['success'],style={'color':'red'})),html.Td(html.P(bot_bm_data['fail'],style={'color':'red'})) , html.Td(html.P(bot_bm_data['number_frames'],style={'color':'red'})),html.Td(dcc.Link(dbc.Button("Details", color="success"), href=f"/game?op_id={bot_id}")),html.Td(dcc.Link(dbc.Button("View Bot", color="success"), href=f"/view_bot_bm?bot_id={bot_id}")),html.Td(dcc.Link(dbc.Button("Run", color="success"), href=f"/game?op_id={bot_id}")) ])
            my_rows.append(row)

            number_rows+=1
            if number_rows > 300:
                break


        table_header = [html.Thead(html.Tr([html.Th("Bot ID"), html.Th("Target"),  html.Th("Hit Rate"), html.Th("Recall"), html.Th("Number Files"), html.Th("Success"), html.Th("Fail"), html.Th("Avg Frames"),html.Th("Details"),html.Th("View"),html.Th("Run") ]))]
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

    def build_benchmarking_page(self, filter = {}):
        
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
            html.H3("Overview"),
            html.Div("live-time-text"),
            html.Br(),
            dbc.Row([
                dbc.Col(self.build_card("Number Bots", self.benchmark_data.rank_data['bm_ov']["number_bots_total"])),
                dbc.Col(self.build_card("Number Files", self.benchmark_data.rank_data['bm_ov']["number_files_total"])),
                dbc.Col(self.build_card("Number Frames", self.benchmark_data.rank_data['bm_ov']["number_frames_total"])),
                dbc.Col(self.build_card("Number Labels", self.benchmark_data.rank_data['bm_ov']["number_labels_total"]))
            ]),
            dbc.Row([
                dbc.Col(self.build_card("Number Decisions", self.benchmark_data.rank_data['bm_ov']["number_decisions_total"])),
                dbc.Col(self.build_card("Accuracy (%)", self.benchmark_data.rank_data['bm_ov']["accuracy"])),
                dbc.Col(self.build_card("Precision (%)", self.benchmark_data.rank_data['bm_ov']["precision"])),
                dbc.Col(self.build_card("Recall (%)", self.benchmark_data.rank_data['bm_ov']["recall"])) 
            ]),
            html.Br(),
            # table
            html.H3("IDent Bots"),
            html.Br(),
            dbc.Row([html.Div(self.build_benchmark_ov_table())]),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
            ]
        )
        
        return layout


@callback(Output('live-time-text', 'children'), Input('interval-component', 'n_intervals'))
def update_metrics(n):
    
    now_utc = datetime.now(timezone.utc)
    now_utc_str = datatime.strftime(now_utc,"%y%m%d $h%m%s UTC")
    return html.Span(now_utc_str)
    
