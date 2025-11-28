#!/usr/bin/python3


#----------------------------------------------------------------------------
#                               IDent Learn                                 #
#                               c. Rahul Tandon, 2025                       #
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
#                               IMPORTS                                     #
#----------------------------------------------------------------------------


import os, sys, json
from dotenv import load_dotenv, dotenv_values
load_dotenv()


from loguru import logger as logger_
logger_.add('log/ident_learn.log', format="{level} : {time} : {message}: {process}", level="INFO")
logger_.remove(0)
logger_.add(sys.stdout, level="INFO")  


#----------------------------------------------------------------------------
#                               CUSTOM FOLDERS                              #
#----------------------------------------------------------------------------


# Brahma library
BRAHMA_FOLDER_USR = os.path.join('/','home','vixen','dev','marlin_brahma', '')
os.environ['BRAHMA_ROOT_USR'] = BRAHMA_FOLDER_USR
sys.path.insert(0, os.environ['BRAHMA_ROOT_USR'])

# MARLIN data
MARLIN_DATA_FOLDER_USR = os.path.join('/','home','vixen','rs','dev','marlin_data', 'marlin_data','')
os.environ['MARLIN_DATA_USR'] = MARLIN_DATA_FOLDER_USR
sys.path.insert(0, os.environ['MARLIN_DATA_USR'])


# Define location of bespoke genes
GENETIC_DATA_FOLDER_USR = os.path.join('/','home','vixen','rs','dev','dmdb','custom_genes')
os.environ['GENETIC_DATA_FOLDER_USR'] = GENETIC_DATA_FOLDER_USR
sys.path.insert(0, os.environ['GENETIC_DATA_FOLDER_USR'])

# Define location of bespoke bots
BOT_DATA_FOLDER_USR =  os.path.join('/','home','vixen','rs','dev','dmdb','custom_bots')
os.environ['CUSTOM_BOT_FOLDER_USR'] = BOT_DATA_FOLDER_USR
sys.path.insert(0, os.environ['CUSTOM_BOT_FOLDER_USR'])

# Define bespoke decision logic
DECISION_FOLDER_USR =  os.path.join('/','home','vixen','rs','dev','dmdb','custom_decisions')
os.environ['DECISION_FOLDER_USR'] = DECISION_FOLDER_USR
sys.path.insert(0, os.environ['DECISION_FOLDER_USR'])

# Define bespoke transcription logic
TRANSCRIPTION_FOLDER_USR =  os.path.join('/','home','vixen','rs','dev','dmdb','custom_transcription')
os.environ['TRANSCRIPTION_FOLDER_USR'] = TRANSCRIPTION_FOLDER_USR
sys.path.insert(0, os.environ['TRANSCRIPTION_FOLDER_USR'])


from marlin_data import MarlinDerivedData
from marlin_data import MarlinDataStreamer
from marlin_data import MarlinData


import marlin_brahma.bots.bot_root as bots
import marlin_brahma.world.population as pop
from marlin_brahma.fitness.performance import RootDecision
import marlin_brahma.fitness.performance as performance
import marlin_brahma.game.game_play as mygame


from custom_bots import *
from custom_genes import *
from custom_decisions import *

#----------------------------------------------------------------------------
#                           LOAD GAME CONFIG & ENV                          #
#----------------------------------------------------------------------------

# Load the game env file
game_env = dotenv_values(f'game_env.env')

# Load the config file
with open('config.json', 'r') as config_f:
    game_args = json.load(config_f)

# Load the gene limits files
with open(f'gene_limits.json', 'r') as config_f:
    gene_limits = json.load(config_f)


#----------------------------------------------------------------------------
#                           CREATE WORLD                                    #
#----------------------------------------------------------------------------
    
# *** Build the initial population structure for the game. ***
population = pop.Population(parms=game_args, name=game_args['name'], gene_args = gene_limits, version=game_args['feature_version'],dmdb_load=True)

# *** Populate the world ***
population.Populate(species="AcousticBot", args = None, dmdb = True)
population.ShowDMDB()
# population.save_dmdb()
# population.DMDB_saveBots(population.bots,{})
# exit()
#----------------------------------------------------------------------------
#                           BUILD DATASETS                                  #
#----------------------------------------------------------------------------
data_adapter = MarlinData(load_args={'limit' : 1000})
data_feed = MarlinDataStreamer()

# *** Download dataset ***
data_adapter.download_simulation_snapshots(load_args={'simulation_path':game_env['simulation_data_path'], 'location':game_args['data_location'], 'ss_ids' : game_env['sim_ids']})
data_feed.init_data(data_adapter.simulation_data, data_adapter.simulation_index)

# *** Build derived data for signal processing ***
data_adapter.build_game_data(data_feed, game_args, gene_limits)
data_adapter.show_game_data()



# *** Download labels *
data_adapter.derived_data.build_xr_data(user_uid = game_args['uid'], target=game_args['target'])
#----------------------------------------------------------------------------
#                           RUN GAME                                        #
#----------------------------------------------------------------------------
# *** Run DMDB game ***

# {self.dump_path}/learn_out/
bot_path = "bots_new"
dump_path = "/home/vixen/html/dump"
identGame = mygame.IdentGame(population = population, data_feed = data_feed, derived_data = data_adapter.derived_data, multiple_derived_data = data_adapter.multiple_derived_data, game_id = "rev1", game_parms=game_args, dmdb_flag = True, init_expression_load=True, dump_path=dump_path, bot_path = bot_path)
identGame.play()


#----------------------------------------------------------------------------
#                             END                                           #
#----------------------------------------------------------------------------


