import numpy as np

def weights_calculation(labels):
    unique, counts = np.unique(labels, return_counts=True)
    
    weights = [1, counts[0]/counts[1]]
    
    return weights 