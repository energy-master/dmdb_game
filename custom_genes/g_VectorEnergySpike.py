

"""
Gene : Energy Spike gene. Return 1 if True. True if f domain is in range of gene.
Peristent version. 


"""

#/usr/bin/python3

import numpy as np
import os
from scipy.io import wavfile
import time as t
from loguru import logger as logger_
# ================================== timers ==================

duration = {}
def startt(name=""):
    duration[name] = t.time()
    
def stopt(desc = "", name="", out=0):
    # print (desc)
   
    if name == "":
        name = desc
    
    d_ = t.time() - duration[name]
    if out == 1:
        print (f'{desc} => {d_} (s)')
    duration[name] = d_


# ================================== band pass ==================

version = 1.0
# print (f"VectorEnergySpike [{version}]")
from marlin_data import *
from marlin_brahma.genes.gene_root import *



import random, json, math
from datetime import timedelta
import statistics

from numba import jit, njit, vectorize
import numpy as np
import time as t
   
# from marlin_utils import *
    
# --- optimisation ----

@njit(nopython=True, cache=False)
def query_stats_freq_index_hyped(frequency_index : int = 0, _time : int = None, data_arr = None ):
    
    #v3.2
    idx_value = np.argmin(np.abs(data_arr[frequency_index] - _time))
    return (idx_value)
    

@njit(nopython=True, cache=False)
def query_closest_idx( value : float = None, data_arr = None ):
    
    #v3.2
    idx_value = np.argmin(np.abs(data_arr - value))
    return (idx_value)
  
  
  
@njit(nopython=True, cache=False)
def get_fast_mean( data_arr  ):
    typed_a = np.array(data_arr)
    #v3.2
    mean_value = np.mean(typed_a)
    return (mean_value)
      
# --- end optimisation ----

DEBUG_OUT = ""
FILE_OUT = False



class VectorEnergySpike(ConditionalRoot):
  
  def __init__(self,env=None,  gene_args = None):
    """[summary]

    :param env: [description], defaults to None
    :type env: [type], optional
    """
    
   
    super().__init__(condition='VectorEnergySpike', env=env)
    
    
    max_memory = gene_args['max_memory']
    min_freq = gene_args['f_min']
    max_freq = gene_args['f_max']
    min_threshold = gene_args['spike_energy_min']
    max_threshold = gene_args['spike_energy_max']
    center_threshold_bound = float(min_threshold + ((max_threshold-min_threshold)/2))
    
    self.memory = random.uniform(5 , max_memory) # ms
    self.memory_ref =  random.uniform(5, max_memory) # ms
    self.frequency = math.floor(random.uniform(min_freq , max_freq))   
     
    self.energy_threshold_lower = random.uniform(min_threshold,center_threshold_bound) 
    self.energy_threshold_upper = random.uniform(center_threshold_bound,max_threshold)
    
    self.energy_tracker = []
    self.energy_tracker_ref = []
    self.ratio_threshold = 1.05
    
    self.query_memory = {}
    self.built = False
    self.birth_generation = 0
    
    
    self.regulatory = 1 #random.random() * random.choice([1,1])
    self.state = 0
  def __str__(self):
    description = {}
    overview = super().__str__()
    
    data = {
        "decision_type" : "VectorEnergySpike",
        "frequency" : self.frequency,
        
        "energy_threshold_lower" : self.energy_threshold_lower,
        "energy_threshold_upper" : self.energy_threshold_upper,
        "memory_ref" : self.memory_ref,
        "memory" : self.memory,
        "regulatory" : self.regulatory,
        "desc" : f'VectorEnergySpike {self.frequency} for {self.memory} ms'
    }
    
    description['overview'] = overview
    description['data'] = data
    
    return ((json.dumps(description)))
    
    
  def GetMemory(self):
    return self.memory
  
  def Reset(self):
    # self.energy_tracker = []
    # self.energy_tracker_ref = []
    self.built = False
    self.birth_generation = 0
    
  def run(self, data = {}, dmdb_flag = False):
    
    
    if dmdb_flag:
      # get state of DM at index_value and return [0,1]
      pass
    
    import math
    
   
    avg_energy = 0
    timings_on = data['timings']
    owner_id = data['bot_id']
    # get f at timestamps
    derived_data = data['derived_model_data']
    
    iter_start_time = data['iter_end_time']
    stats = None
    geneInit = False
    
    sample_rate = data['sample_rate']
    current_data_index = data['data_index'] 
    current_data_delta_time = (current_data_index/sample_rate) * 1000 # ms
    current_data_delta_time_s = current_data_delta_time / 1000
    self.Start()
    self.state = 0
   
   
    
    number_indices_memory = math.floor(self.memory/(data['sim_delta_t']*1000))
    number_indices_ref = math.floor(self.memory_ref/(data['sim_delta_t']*1000))
    
    
    if ((current_data_delta_time) > self.memory):
      geneInit = True
      
    logger_.trace(f'init : {geneInit}')
    if 0 not in self.query_memory:
      self.built = False
      self.birth_generation = data['generation']
    
    
    if not self.built:
      if data['generation'] > self.birth_generation:
        # print ("true")
        # self.built = True
        pass
        

    if not self.built:  
      
      # self.query_memory[data['global_iter_count']] = {}
      # self.query_memory[data['global_iter_count']]['condition'] = 0
      fourier_e_pivot = 0.0
      fourier_f_idx = query_closest_idx(self.frequency, derived_data.librosa_f_bins)
      fourier_t_idx = query_closest_idx(current_data_delta_time_s, derived_data.librosa_time_bins)
      fourier_e_pivot = derived_data.fourier[fourier_f_idx,fourier_t_idx]
      # self.query_memory[data['global_iter_count']] = fourier_e_pivot
      
    
      if not geneInit:
        self.energy_tracker.append(fourier_e_pivot)
        self.energy_tracker_ref.append(fourier_e_pivot)
        return 0
      
      
    # Remove for now. This does not allow simple parameter changes, e.g. energy threshold
    # if (self.built):
    #   if data['global_iter_count'] in self.query_memory:
    #     return (self.query_memory[data['global_iter_count']]['condition'])
    #   else:
    #     k = data['global_iter_count']
    #     print (f'error key : {k}')
    #     print (self.query_memory)
        
    #     return 0
  
    delta_f_pc = 0.0
    file_out = False
    condition = False
    if geneInit:
        self.Safe()
        

        
        if self.frequency > derived_data.librosa_f_bins[-1]:
          logger_.error("Frequency out of range.")
          return 0.0
        
        
        if not self.built:
          
          if timings_on:
            startt(name="mean_attack")
            
          
          
          if (len(self.energy_tracker[(len(self.energy_tracker)-number_indices_memory): ]) > 3):
            if (len(self.energy_tracker_ref[(len(self.energy_tracker_ref)-number_indices_ref) : ]) > 3):
              
              avg_energy = np.mean(self.energy_tracker[(len(self.energy_tracker)-number_indices_memory): ])
              avg_energy_ref = np.mean(self.energy_tracker_ref[(len(self.energy_tracker_ref)-number_indices_ref): ])
            
            else:
              avg_energy = 0
              avg_energy_ref = 0
          else:
            avg_energy = 0
            avg_energy_ref = 0
          if timings_on:
            stopt(desc="mean_attack", out=0)
        
          
          if not self.built:
            self.energy_tracker.append(fourier_e_pivot)
            self.energy_tracker_ref.append(fourier_e_pivot)

            self.energy_tracker.pop(0)
            self.energy_tracker_ref.pop(0)
          
          if avg_energy == 0:
            return 0
          
          # print (avg_energy_ref, avg_energy)
          
          # --- USING MARLIN-DATA Frequency Indexing ----       
          delta_f = 0
          # delta_f = abs(fourier_e_pivot - avg_energy)
          delta_f = abs(avg_energy_ref - avg_energy)
          delta_f_pc = (delta_f / (avg_energy))  * 100
          ratio = avg_energy_ref/avg_energy
          # self.query_memory[data['global_iter_count']]['delta_f_pc'] = delta_f_pc
          #--- debg out --
          
        else:
          
          if data['global_iter_count'] in self.query_memory:
            try:
              delta_f_pc = self.query_memory[data['global_iter_count']]['delta_f_pc']
            except:
              print (self.built, data['global_iter_count'])
              # print (self.query_memory)
              return 0
          
          
        logger_.trace(f'delta f % : {delta_f_pc} [ {self.energy_threshold_lower} - {self.energy_threshold_upper} ]')

        if delta_f_pc > self.energy_threshold_lower and delta_f_pc < self.energy_threshold_upper:
        # if ratio > self.ratio_threshold:
          condition = True
        
        # self.query_memory[data['global_iter_count']]['condition'] = 1 if condition == True else 0
        
        if FILE_OUT:
            outfile_name = f'{owner_id}.csv'
            with open(f'{DEBUG_OUT}/{outfile_name}', 'a+') as f:
              iter_number = data['global_iter_count']
              f.write(f'{iter_start_time},{iter_number},{avg_energy},{fourier_e_pivot},{delta_f_pc}, {self.frequency}, {self.memory}, {self.energy_threshold_lower},{self.energy_threshold_upper}, {self.i_D}, {condition}, {ratio} \n')
        
        #and delta_f_pc < self.energy_threshold_upper:
        if delta_f_pc > self.energy_threshold_lower: 
            logger_.trace(f'Return 1')
            if hasattr(self, 'regulatory'):
              self.state = 1
              return (1 * self.regulatory)

            else:
              self.state = 1
              return (1)

        
        logger_.trace(f'Return 0')
        self.state = 0
        return 0
    self.state = 0
    return 0
  
  
  
  
  
  
  def mutate(self, data = {}):
    
    factor = 1
    creep_rate = data['pc_threshold_creep_rate']
    dice = random.uniform(0,1)
    if dice > 0.5:
      self.energy_threshold_lower = self.energy_threshold_lower + (creep_rate*factor)
    else:
      self.energy_threshold_lower = self.energy_threshold_lower - (creep_rate*factor)
    
    dice = random.uniform(0,1)
    if dice > 0.5:
      self.energy_threshold_upper = self.energy_threshold_upper + (creep_rate*factor)
    else:
      self.energy_threshold_upper = self.energy_threshold_upper - (creep_rate*factor)
    
    dice = random.uniform(0,1)
    
    
      

