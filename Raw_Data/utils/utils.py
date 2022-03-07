import pandas as pd
import numpy as np
import Raw_Data.configurations as cfg

def total_movement(data_series):
    diff = data_series.diff().iloc[1:]
    diff = abs(diff)   
    return sum(diff)



def convolve(data, window_size=10):
    data = np.array(data)
    window = np.ones(window_size)/window_size
    data = np.convolve(data, window, mode='same')
    data = pd.Series(data)
    return data

def number_to_string(num):
    if cfg.numbers_mode == 0:
        return str(num)
    num = num + 10 ** cfg.numbers_mode
    return str(num)[1:]

def extract_subject_number(dir_name):
    num = int("".join(list(filter(str.isdigit, dir_name))))
    return num
