import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

import classifications.configurations as cfg

def normalize(data):
    if data.name.isdigit():
        num = int(data.name)
        if num < 3:
            return data
    if data.std() == 0:
        return data - data
    # return (data - 3)
    return ((data - data.mean())/data.std())
     

def feature_normalization(data, idx):
    ...


def feature_normalization(data, idx):
    # get column name in order to perform groupby 
    col_name = data.columns[idx]
    # get the column itself in order to add it back to the data
    col = data[col_name]
    # apply normalization
    data = data.groupby(col_name).transform(normalize)
    # add column back
    data.insert(idx, col_name, col)
    return data
    
    
