"""Transcription genetic material/process is responsible for building the protein.
Here we model the action of decision making as the bot able to transcrible protein.
All the dna material in the bot is the genetic material required to regulate and transcribe
three different protein types:
1. An enzyme whose presence prescribes a 'ACTIVE' state
2. An enzyme whose presence prescribes a 'WAIT' state

This class/module is also considered 'genetic material', but it; sole responsibilty is to transcribe the already
exisiting genetic material. The genetic state of the gene(s) modelled here is/are always on (1/True).

gene state->genome->chromosome->expression vector-> [environmental regulation] -> transcription

[environmental regulation] will simply promote/suppress the expression vector rather than work on the transcrition
state

"""
import random, logging

logger = logging.getLogger("__main__")



from loguru import logger as logger_
#local import
import os, sys


# sys.path.append('../')
# from configCore import *



class Transcription(object):
    """This class models the genetic material required to transcribe the 'bot's' genetic material.
    It reads in chromosomal expression levels and decides whether

    Arguments:
        object {[type]} -- [description]


    """

    def __init__(self):

        self.transcription_state = None
        self.transcription_state_recorder = {}
        #self.transcription_threshold = random.random()
        #self.transcription_threshold = 0.002
       
        #v2. update - Apr 16
        #--update -> remove Nov 2020
        #self.transcription_threshold_exit = random.random()

        self.regulatory_network = {}

        # parameters
        self.mean_bound_min = random.randint(120000,150000)
        self.mean_bound_max = random.randint(self.mean_bound_min,150000)
        self.transcription_threshold = random.random()
        self.bandwidth_min = random.randint(1000,20000)
        self.bandwidth_max = random.randint(self.bandwidth_min,20000)
        


    def __str__(self):
        return ("Activation Level: {0}".format(self.transcription_threshold))


    def run_transcription(self,bot=None, dmdb_structure={}, dmdb_expression_vector={},global_iter_count=0, transcription_data={}, dmdb_flag = False):
        """run_transcription Regulate genetic expression and determine protein synthesis

        :param bot: _description_, defaults to None
        :type bot: _type_, optional
        :param dmdb_structure: _description_, defaults to {}
        :type dmdb_structure: dict, optional
        :param dmdb_expression_vector: _description_, defaults to {}
        :type dmdb_expression_vector: dict, optional
        :param global_iter_count: _description_, defaults to 0
        :type global_iter_count: int, optional
        :param transcription_data: _description_, defaults to {}
        :type transcription_data: dict, optional
        """

        regulated = self.Regulate(bot=bot, dmdb_structure = dmdb_structure, dmdb_expression_vector=dmdb_expression_vector, global_iter_count=global_iter_count, dmdb_flag = dmdb_flag)
        if regulated:
            return True
        else:
            return False
    def get_structure(self):
        transcription_str = {}
        transcription_str['state'] = self.transcription_state
        #transcription_str['threshold'] = self.transcription_threshold_exit



    def Regulate(self,bot, dmdb_structure = {}, dmdb_expression_vector={},  global_iter_count=0, dmdb_flag = False):
        """regulate Regulate genetic expression to get real expression

        :param bot: _description_
        :type bot: _type_
        """
        
        
        max_f = 0
        min_f = 99999999999
        
        active_f = []
        
        
        states =[]
        for dna_tag, dna in bot.dNA.items():
            for genome_tag, genome in dna.genome.items():
                for geneTag, gene in genome.genome.items():
                    g_state = -1
                    if dmdb_flag:
                        try:
                            g_state = dmdb_expression_vector[gene][global_iter_count]
                        except:
                            print ("g_state")
                            d = len(dmdb_expression_vector[gene])
                            print (f'gl: {d}')
                            print (f'tag: {gene}')
                            print (f'gi: {global_iter_count}')
                            
                    else:
                        g_state = gene.state
                    states.append(g_state)
                    if g_state == -1:
                        logger_.error("Critical error : No gene structure found.")
                    # print (g_state)
                    if g_state == 1:
                        if dmdb_flag:
                            gene_str = dmdb_structure[gene]
                        else:
                            gene_str = gene
                            
                        min_f = gene_str.frequency if gene_str.frequency < min_f else min_f
                        max_f = gene_str.frequency if gene_str.frequency > max_f else max_f
                        active_f.append(gene_str.frequency)




        activity = 0
        if len(states) > 0:
            activity = sum(states)/len(states)
        


        m = 0
        if len(active_f) > 0:
            m = sum(active_f)/len(active_f)
        
        bw = max_f - min_f
        
        if (bw > self.bandwidth_min) and (bw < self.bandwidth_max) and (m > self.mean_bound_min) and (m<self.mean_bound_max) and (activity > self.transcription_threshold):
            
            return True
        else:
            return False


    # def build_reg_network(self, bot):
    #     self.regulatory_network = {}

        
    #     for dna_tag, dna in bot.dNA.items():
    #         for genome_tag, genome in dna.genome.items():
    #             for activeTag, active_gene in genome.genome.items():
    #                 for geneTag_inner, gene_inner in genome.genome.items():
    #                     if activeTag != geneTag_inner:
    #                         if activeTag not in self.regulatory_network:
    #                             self.regulatory_network[activeTag] = {}
    #                         if geneTag_inner not in self.regulatory_network[activeTag]:
    #                             self.regulatory_network[activeTag][geneTag_inner] = 0
    #                         self.regulatory_network[activeTag][geneTag_inner] = random.random() * random.choice([-1,1])
                        

        
        
    # def update_reg_network(self, bot):
    #     for dna_tag, dna in bot.dNA.items():
    #         for genome_tag, genome in dna.genome.items():
    #             for activeTag, active_gene in genome.genome.items():
    #                 for geneTag_inner, gene_inner in genome.genome.items():
    #                     if activeTag != geneTag_inner:
    #                         if activeTag not in self.regulatory_network:
    #                             self.regulatory_network[activeTag] = {}
    #                         if geneTag_inner not in self.regulatory_network[activeTag]:
    #                             self.regulatory_network[activeTag][geneTag_inner] = random.random() * random.choice([-1,1])
                            
    
    
    # def mutate_reg_network:
    #     pass

    
    def transcribe(self, expression_data, activation_level = 0.7):
        """Transcribe DNA into protein

        Arguments:
            expression_data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        # print (self.transcription_threshold)
        expression_str = expression_data['expression_data']
        #nt ("*********")
        
        expression_vec = []

        for chromTag, expression in expression_str.items():
            #print (expression)
            expression_vec.append(expression)


        protein_transcribe = self.map_expression_vector(expression_vec, t_level=activation_level)
        
       
        if protein_transcribe == True:
            
            self.transcription_state = True
            return protein_transcribe

        else:
            return False

        

    def map_expression_vector(self, e_data=None, t_level = 0.7):
        t_level = float(t_level)
        """Map expression vector. State function on expression vector to determine
        transcription state.

        Keyword Arguments:
            e_vector {[type]} -- [description] (default: {None})
        """
       
        
        express_sum = 0
        number_express = len(e_data)

        for expression in e_data:
            express_sum = express_sum + expression

        if number_express == 0:
            print (f'Error divide by zero. Transcription.')
            # exit()
        transcription_activity = express_sum/number_express
        #see if trade triggered
        
        #---debug
        #print (transcription_activity)
        # if transcription_activity > self.transcription_threshold:
        
        if transcription_activity > t_level:
            
            return True

        else:
            return False
    



    def Mutate(self):
        
        dir = random.choice([1,-1])
        self.transcription_threshold =  self.transcription_threshold + (dir * 0.5)
        
        dir = random.choice([1,-1])
        self.mean_bound_min = self.mean_bound_min + (dir * 1000)
        self.mean_bound_max = self.mean_bound_max + (dir * 1000)
        
        dir = random.choice([1,-1])
        self.bandwidth_min = self.bandwidth_min + (dir * 1000)
        self.bandwidth_max = self.bandwidth_max + (dir * 1000)
        

if __name__=="__main__":
    trans = Transcription()
    data = { 'expression_data':[0.3,0,0.65,0] }
    trans.transcribe(data)
