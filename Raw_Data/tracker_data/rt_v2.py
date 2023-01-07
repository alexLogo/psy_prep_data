import logging
import os

import numpy as np
import pandas as pd

import Raw_Data.configurations as cfg
from Raw_Data.utils.convert_groupby import convert_groupby_to_list
from Raw_Data.utils.utils import number_to_string
import pathes

def new_path_resolver(subject_num):
    path = pathes.raw_data_path + cfg.participant_dir_name + number_to_string(subject_num) + '/Butterfly Predictions/'
    try:
        inner_dir = [f for f in os.listdir(path) if f.startswith('Sub')][0]
    except OSError as e:
        logging.error(f"Error while accessing the directory at {path}: {e}")
        raise
    path += inner_dir + '/'
    try:
        filename = [x for x in os.listdir(path) if x.startswith(cfg.tracker_file_name_prefix)][0]
    except OSError as e:
        logging.error(f"Error while accessing the directory at {path}: {e}")
        raise
    path += filename
    return path


def path_resolver(subject_num, new=False):
    if new:
        return new_path_resolver(subject_num)
    path = pathes.raw_data_path + cfg.participant_dir_name + number_to_string(subject_num) + '/' + cfg.tracker_file_name
    return path


def room_rows_filter(df):
    for idx, value in cfg.relevant_rows_filter:
        df = df[df.iloc[:, idx] == value]
        
    return df


def unrelevant_trials_filter(df):
    df = df[~df.loc[:, cfg.tracker_idx_col].isin(cfg.unrelevant_trials)]
    return df


def relevant_column_filter(df):
    df = df.iloc[:, cfg.tracker_relevant_data_cols]
    df.columns = cfg.tracker_relevant_data_names
    return df

    

def split_to_trials(df):
    # groupby trial number (2)
    df_group = df.groupby(cfg.tracker_idx_col)
    
    #convert groupby object to list of (trial_num, trial_dataframe)
    df_list = convert_groupby_to_list(df_group)

    return df_list
    

def read_tracker(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num, new=True)
    
    # read trials data
    try:
        data = pd.read_csv(path)
    except OSError as e:
        logging.error(f"Error while reading file at {path}: {e}")
        raise
    
    # take only relevant room rows
    data = room_rows_filter(data)
 # take only relevant columns
data = relevant_column_filter(data)

# take only relevant trials
data = unrelevant_trials_filter(data)


# split to trials (list of tuples: (idx, df))
try:
    splited_data = split_to_trials(data)
except Exception as e:
    logging.error(f"Error while splitting data into trials: {e}")
    raise
    
return splited_data




