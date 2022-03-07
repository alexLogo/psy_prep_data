import pandas as pd
import numpy as np

import Raw_Data.configurations as cfg
from Raw_Data.utils.utils import total_movement

def filter_short_trial(df):
    length = df['timestamp'].iat[-1] - df['timestamp'].iat[0]
    return length < cfg.filter_time_short


def filter_short_movement(df):
    movement = total_movement(df[cfg.filter_column_of_interest])
    return movement < cfg.filter_movement_short


def filter_long_movement(df):
    movement = total_movement(df[cfg.filter_column_of_interest])
    return movement > cfg.filter_movement_long


def filter_starting_point(df):
    starting_point = df[cfg.filter_column_of_interest].iat[0]
    return starting_point < cfg.filter_expected_low or starting_point > cfg.filter_expected_high
 

def filter_no_reach_movement(df):
    min_point = df[cfg.filter_column_of_interest].min()
    max_point = df[cfg.filter_column_of_interest].max()
    gap = abs(max_point-min_point)
    return gap < cfg.min_reaching


def filter_reach_hesitation(df):
    movement = np.array(df[cfg.filter_column_of_interest])
    min_point = df[cfg.filter_column_of_interest].min()
    max_point = df[cfg.filter_column_of_interest].max()
    medium_point = (max_point + min_point) / 2
    line = np.ones(len(movement)) * medium_point 
    reaching_point_indices = movement > line 
    length_of_hesitation = np.sum(reaching_point_indices)
    
    return length_of_hesitation > cfg.hesitation_threshold
    