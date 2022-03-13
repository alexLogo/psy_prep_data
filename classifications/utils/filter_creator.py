import numpy as np
from random import randint, seed

def create_filter(idx, accepted_trials):   
    # define the classifier function
    def filter_fun(trial_header):
        # if idx is -1, we will create random labeler
        key = trial_header[idx]
        if isinstance(key, np.ndarray):
            key = tuple(key)
        return key in accepted_trials
    
    return filter_fun