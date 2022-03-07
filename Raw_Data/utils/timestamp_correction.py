import pandas as pd
import numpy as np

TIME_SIZE = 100000
SECOND = 60000
def timestamp_correction(ts):    
    ts = ts % TIME_SIZE
    
    ts_diff = ts.diff()
    add_second = ts_diff < 0
    
    seconds = 0
    for i in range(1, len(ts)):
        if add_second.iat[i]:
            seconds += 1
        ts.iat[i] = SECOND * seconds + ts.iat[i]
    
    return ts