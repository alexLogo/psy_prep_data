import pandas as pd
import numpy as np
from os import listdir

from Raw_Data.utils.utils import number_to_string
import Raw_Data.configurations as cfg

def path_resolver(subject_num):
    path = cfg.raw_data_path + cfg.participant_dir_name + number_to_string(subject_num) + '/' + cfg.answers_file_name
    return path



def filter_answer_file_question(df):
    # take only real trials rows
    # filter by question
    df = df[df[cfg.answer_question_col_name] == cfg.relevant_question]
    
    
    # take only id and relevant columns
    df = df[[cfg.answers_index] + cfg.answer_relevant_cols]
    
    return df
    
def label_answer_file_one_columns(df, col_id, tranfrom_dic=cfg.trial_labels_dic):
    df.iloc[:,col_id].replace(tranfrom_dic, inplace=True)
    return df


def read_answers(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num)
    
    # read trials data
    data = pd.read_csv(path)
    
    # filter trials data
    data = filter_answer_file_question(data)
    
    # reset index
    data.reset_index(inplace=True, drop=True)
    
    # no need for labeling in the moment 
    #data = label_trials_file_one_columns(data, col_id=1)
    
    return data 
