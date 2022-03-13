import numpy as np
import pandas as pd
import timeseries_data.configurations as cfg
import pathes 

def create_meta_string(header_size, num_of_ts, names):
    metastring = str(header_size)+','+str(num_of_ts)+','
    for name in names:
        metastring += name + ','
        
    return metastring[:-1]

def extract_meta_string(metastring):
    splited = metastring.split(',')
    
    header_size = int(splited[0])
    num_of_ts = int(splited[1])
    names = splited[2:]
    
    return header_size, num_of_ts, names


def zero_strip(array):
    for i in range(len(array)-1,0,-1):
        if array[i] != cfg.padding_value:
            return array[:i+1]
    
def deravative(ts):
    ts = ts[0]
    der = np.diff(ts)
    der = np.pad(der, (0,1), mode='edge')
    return der


def euclidian_combination(ts_lst):
    # to array
    ts_array = np.array(ts_lst)
    # square power
    ts_array = ts_array ** 2
    # sum
    sum_ts = np.sum(ts_array, axis=0)
    # sqrt
    result = np.sqrt(sum_ts)
    
    return result


def path_resolver(mode, num):
    if mode == "base":
        path = pathes.ts_data_path
    elif mode == 'full kinematic':
        path = pathes.full_kinematic_ts_data_path
    elif mode == 'handcraft':
        path = pathes.handcraft_features
        
    return path + 'participant' + str(num) + '.csv'


