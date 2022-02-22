import numpy as np
import pandas as pd

import Raw_Data.configurations as cfg

def path_resolver(subject_num):
    path = cfg.raw_data_path + cfg.participant_dir_name + str(subject_num) + '/' + cfg.tracker_file_name
    return path



def read_tracker(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num)
    
    # read trials data
    data = pd.read_csv(path)
    
    
    return data 
