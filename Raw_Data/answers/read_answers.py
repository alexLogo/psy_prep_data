import pandas as pd
import numpy as np
from os import listdir

import Raw_Data.configurations as cfg
import pathes
from Raw_Data.utils import utils

def read_answers(subject_num):
    # resolve path of trials file
    path = utils.path_resolver(subject_num, cfg.answers_file_name)
    
    # read trials data
    data = pd.read_csv(path)
    
    # filter trials data
    data = utils.filter_answer_file_question(data)
    
    # reset index
    data.reset_index(inplace=True, drop=True)
    
    # no need for labeling in the moment 
    #data = label_trials_file_one_columns(data, col_id=1)
    
    return data 
