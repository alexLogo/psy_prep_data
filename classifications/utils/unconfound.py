import numpy as np
import random
import classifications.configurations as cfg
def counts_format(unique, counts):
    for i in range(7):
        if i not in unique:
            counts.insert(i,0)
    return counts

# this function gets many trials data and return counts of trial types
def trial_type_counter(meta_labels):
    unique, counts = np.unique(meta_labels, return_counts=True)
    
    counts = list(counts)
    
    counts = counts_format(unique, counts)
    
    return counts

# this function gets labels array, meta labels array, conditions for both (label & meta) and k number of indices to choose
# the function k random indices that are label & meta
def random_k_indices(y, z, label, meta, k):
    random.seed(cfg.random_seed)
    # select all indices where y=label and z=meta
    idx = [i for i in range(len(y)) if (y[i] == label) and (z[i] == meta)]
    
    # sample k indices randomly
    chosen_idx = random.sample(idx, k)
    
    return chosen_idx

def soa_unconfound(x,y,z, restricted=False):
    # extract indices to unconfound the data
    idx = []
    idx0 = [i for i in range(len(y)) if y[i] == 0]
    idx1 = [i for i in range(len(y)) if y[i] == 1]
    
    trial_counts0 = trial_type_counter(z[idx0])
    trial_counts1 = trial_type_counter(z[idx1])
    
    for i in range(len(trial_counts0)):
        min_class = min(trial_counts0[i], trial_counts1[i])
        
        if restricted:
            min_class = min(min_class, cfg.restrictions[i])
        idx.extend(random_k_indices(y,z,0,i,min_class))
        idx.extend(random_k_indices(y,z,1,i,min_class))
    
    # unconfound the data
    x = x[idx]
    y = y[idx]
    z = z[idx]
    
    return x,y,z