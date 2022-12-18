import numpy as np
import configurations as cfg

def threshold_filter(header, idx=1, threshold=cfg.threshold):
    types = header.iloc[:,idx]
    types = np.array(types)
    _, counts = np.unique(types,return_counts=True)
    
    # check if there is at list one type that smaller than threshold
    is_legal = np.sum(counts[counts < threshold]) > 0
    
    return is_legal