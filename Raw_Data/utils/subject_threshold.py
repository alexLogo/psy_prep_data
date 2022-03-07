import numpy as np


def threshold_filter(header, idx=1, threshold=20):
    types = header.iloc[:,idx]
    types = np.array(types)
    _, counts = np.unique(types,return_counts=True)
    
    # check if there is at list one type that smaller than threshold
    is_legal = np.sum(counts[counts < threshold]) > 0
    
    return is_legal