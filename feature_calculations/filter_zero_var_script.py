import pandas as pd
import numpy as np
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_features 
import pathes

def filter_zero():
    idx_to_filter = np.ones(8660)
    idx_to_filter = np.array(idx_to_filter, dtype=bool)
    
    for i in cfg.participants_range:
        print(f"analyzing participant {i}")
        data = read_features(i)
        zero_var = data.std(axis=0)
        zero_var = (zero_var == 0)
        zero_var = np.array(zero_var)
        
        idx_to_filter = (idx_to_filter & zero_var)
        
    print(f"filtering {np.sum(idx_to_filter)} unrelevant features")
        
    for i in cfg.participants_range:
        print(f"rewriting participant {i}")
        data = read_features(i)
        data = data[data.columns[~idx_to_filter]]
        
        data.to_csv(pathes.base_clean_feature_path+"participant"+str(i)+".csv", index=False)
        
if __name__ == "__main__":
    filter_zero()