#!/usr/bin/python3

import os, glob
import dash 
from dash import callback, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import time as t
import json, math
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash_data import *

import requests

# JSON op data output folder
OP_METRICS_OUTPUT_FOLDER = "/home/vixen/rs/dev/dmdb/learn_out"
OP_STRUCTURES_OUTPUT_FOLDER = "/home/vixen/rs/dev/dmdb/bot_str"

BM_RESULTS_FOLDER = "https://marlin-network.hopto.org/marlin_live_data/benchmark_data/results"

class BenchmarkOverviewData(object):
    """BenchmarkingData _summary_

    :param object: _description_
    :type object: _type_
    """
    
    def __init__(self):
        
    
        self.rank_data = {}
    
    def load_data(self):
        # with open(f'{BM_RESULTS_FOLDER}/ranked.json', 'r') as fp:
        #     self.ranked_data = json.load(fp)
        resp = requests.get(f'{BM_RESULTS_FOLDER}/ranked.json')
        self.rank_data = resp.json()
    
        
        
        


class OpData(object):
    """OpData _summary_

    :param object: _description_
    :type object: _type_
    """
    
    def __init__(self, op_id):
        self.op_id = op_id
        self.best_fitness = []
        self.worst_fitness = []
        self.gen_num = []
        self.saved_bots = []
        self.results = {}
        self.number_positive = 0
        self.number_bots_saved = 0
        self.best_life = 0
        self.number_gen = 0
    
    
    def BuildOpData(self):
    
        self.best_fitness = []
        self.worst_fitness = []
        self.gen_num = []
        
        
        
        fn = f'gen_data_{self.op_id}.json'
        path = f'/home/vixen/rs/dev/dmdb/learn_out/{fn}'

        data = None
        with open(path,'r') as fp:
            data = json.load(fp)

        for gen_data in data:
            
            self.gen_num.append(gen_data['generation_number'])
            self.best_fitness.append(gen_data['best'])
            self.worst_fitness.append(gen_data['worst'])
        
        self.number_gen = len(self.best_fitness)
        last_data_iter = data[self.number_gen-1]
        if 'overview' in last_data_iter:
            if 'saved_bots' in last_data_iter['overview']:
                self.saved_bots = last_data_iter['overview']['saved_bots']
                self.number_bots_saved = len(self.saved_bots)
            if 'results' in last_data_iter['overview']:
                self.results = last_data_iter['overview']['results']
                self.number_positive = 0
                
                for bot_id, fitness in self.results.items():
                    if fitness > 0:
                        
                        self.number_positive += 1
                    if fitness > self.best_life:
                        self.best_life = fitness
                
        

    

class IDentData(object):
    """IDentData 

    :param obj: _description_
    :type obj: _type_
    """
    
    
    def __init__(self, app=None):
        
        self.op_data = {}
        
        self.active_optimisation_id = ""
        self.app = app
        self.optimisation_ids = []
        self.number_bots_total = 0

    def BuildFrameworkOverview(self):
        self.number_bots_total = 0
        for op_id in self.optimisation_ids:
            if op_id not in self.op_data:
                self.op_data[op_id] = OpData(op_id=op_id)

            self.op_data[op_id].BuildOpData()
            self.number_bots_total+=self.op_data[op_id].number_bots_saved
    
    
        
        
    def SetActiveOptimisation(self, optimisation_id=""):
        self.active_optimisation_id = optimisation_id
        self.number_games = len(self.active_optimisation_id)

    def GetOpIds(self):
        file_list = glob.glob(f'{OP_METRICS_OUTPUT_FOLDER}/*.json')
        for file in file_list:
            op_id = file.split('.')[0].split('_')[-1]
            self.optimisation_ids.append(op_id)
            
    

application_data = None

    