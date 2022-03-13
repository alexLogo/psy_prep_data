import pandas as pd
import numpy as np
import Raw_Data.configurations as cfg
from Raw_Data.utils.utils import convolve

K = 10
MOVEMENT_THRESHOLD = 0.002

def idx_of_back(ts):
    # calculate velocity
    ts_diff = ts.diff()
    # smooth timeseries
    ts_diff_for_min = convolve(ts_diff)
    # calculate the velocity peak in the return phase
    idx_of_fast_return = ts_diff_for_min.idxmin()
    
    for i in range(idx_of_fast_return, len(ts_diff)):
        if ts_diff.iat[i] > 0:
            return i
    
    return len(ts) - 1
    


def idx_of_return(ts):
    return ts.idxmax()


def idx_of_start(ts):
    # calculate velocity
    ts_diff = ts.diff()
    ts_diff[0] = 0
    
    # smooth timeseries
    ts_diff = convolve(ts_diff)
    
    # calculate velocity peak index    
    velocity_peak_idx = idx_of_return(ts_diff)
    
    
    for i in range(1, velocity_peak_idx):
        if (ts_diff.iloc[i:velocity_peak_idx] > MOVEMENT_THRESHOLD).all():
            return i
        # check if the K next differences are positive, if so, that would be thee begning of the movement
        '''if (sum(ts_diff.iloc[i:return_idx] > 0) > (return_idx-i)*.9) and (ts_diff.iloc[i:i+K] > 0).all():
            return i'''
        
    return -1
    



def calculate_points_of_interest(header, data):
    # calculate points of interest foreaech trial
    point_of_interest = np.zeros((len(data), 3))
    
    for i,(_, df) in enumerate(data): 
        ts = df[cfg.filter_column_of_interest]
        start = idx_of_start(ts)
        ret = idx_of_return(ts)
        back = idx_of_back(ts)
        point_of_interest[i] = [start, ret, back]
    
    # add results to header
    point_of_interest = pd.DataFrame(point_of_interest)
    header = pd.concat((header, point_of_interest), axis=1)
 
    return header, header.shape[1]
