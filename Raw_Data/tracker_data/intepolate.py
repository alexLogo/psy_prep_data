import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

import Raw_Data.configurations as cfg
 

def interpolate(data):
    kind='cubic'
    if cfg.pathes.trial_mode.startswith('pupil'):
        kind =  'linear'   
    
    original_time = np.array(data['timestamp'])
    new_time = np.arange(0, original_time[-1], cfg.rate_hz)
    
    new_data = [new_time]
    
    for (name, series_data) in data.iteritems():
        # we don't interpolate timestamp column
        if name == 'timestamp':
            continue
        
        # check the data type
        if series_data.dtype == 'object':
            ... #function to interpolate catetorical data 
        else:
            data_array = np.array(series_data)
            
            # interpolate
            # create interpolation function
            f = interp1d(original_time,data_array, kind=kind)
            
            # use the function to create new data points
            new_array = f(new_time)
            
            # add new data to data list
            new_data.append((new_array))
            
    new_data = np.array(new_data).T
    new_data = pd.DataFrame(new_data, columns=data.columns)
    
    return new_data 
            

def data_interpolation(data):
    
    for i,(_, df) in enumerate(data):
        data[i] = (data[i][0], interpolate(df))

    return data
