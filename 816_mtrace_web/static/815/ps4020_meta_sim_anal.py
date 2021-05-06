# -*- coding: utf-8 -*-
##author : oaiskoo
##date : 2006
##goal : 
##
##input
##
##
##process
##
##
##output
##
## 
##history
##-2009
##--task
##
import os
import shutil
import time
import re
import pandas as pd
import numpy as np

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
start = time.time()

### IO name
## input
input_filepath = 'output/ps4010/simple_meta_str.csv'

## output
prefix = 'ps4020'
output_dir = 'output/' + prefix 
oaislib.fn_output_dir_gen(output_dir)
output_filepath1 = 'output/' + prefix + '/meta_sim.csv'
output_filepath2 = 'output/' + prefix + '/meta_sim.xlsx'

##parameter

### data load
input_df = pd.read_csv(input_filepath)
sen_df = input_df[['mov_id', 'mstr_str'] ].copy()

### process
num_sim_sentences = 10
sim_df = oaislib.fn_sentence_cosine_sim(sen_df, num_sim_sentences)

### save result
sim_df.to_csv(output_filepath1, index=False)
sim_df.to_excel(output_filepath2, index=False)

## finish message
print("time :", time.time() - start)
breakpoint()
