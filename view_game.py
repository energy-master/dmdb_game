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


from common_components import *
from dash_data import *



def build_game(application_data, app=app):
    nav = create_navbar(app)
    layout = html.Div([
        
        nav
        
    ])
    return layout
    