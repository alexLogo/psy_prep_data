import pandas as pd
import numpy as np
from os import listdir

import Raw_Data.configurations as cfg

def path_resolver(subject_num):
    path = cfg.raw_data_path + cfg.participant_dir_name + str(subject_num) + '/' + cfg.trials_file_name[0]
    suffix = [f for f in listdir(path) if f.startswith(cfg.trials_file_name[1])]
    
    path = path + '/' + suffix[0]
    
    return path


def filter_trials_file_question(df):
    # take only real trials rows
    # filter by question
    df = df[df[cfg.trial_question_col_name] == cfg.relevant_question]
    
    
    # take only id and relevant columns
    df = df[[cfg.trial_index] + cfg.trial_relevant_cols]
    
    return df
    
def label_trials_file_one_columns(df, col_id, tranfrom_dic=cfg.trial_labels_dic):
    df.iloc[:,col_id].replace(tranfrom_dic, inplace=True)
    return df


def read_trials(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num)
    
    # read trials data
    data = pd.read_csv(path)
    
    # filter trials data
    data = filter_trials_file_question(data)
    
    # label trials in organize manner (by dictionary)
    data = label_trials_file_one_columns(data, col_id=1)
    
    return data