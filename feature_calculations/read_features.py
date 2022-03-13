import numpy as np
import pandas as pd
import feature_calculations.configurations as cfg
import pathes

def read_features(participant_num, mode="base", test=False, to_ndarray=False):
    if mode == "base":
        feature_path = pathes.base_feature_path
    elif mode == "clean":
        feature_path = pathes.base_clean_feature_path
    elif mode == "handcraft":
        feature_path = pathes.handcraft_features

    path = feature_path + "participant" + str(participant_num) + ".csv"
    
    header = None if test else "infer"
    # read the data
    data = pd.read_csv(path, header=header)
    
    if to_ndarray:
        data = np.array(data)
        
    return data 


def read_all_data(mode="base"):
    if mode == "base":
        feature_path = pathes.base_feature_path
    elif mode == "clean":
        feature_path = pathes.base_clean_feature_path
    elif mode == "handcraft":
        feature_path = pathes.handcraft_features
    
    
    
    data = []
    for i in cfg.participants_range:
        path = feature_path + "participant" + str(i) + ".csv"
        subject = pd.read_csv(path)
        
        data.append(subject)
        
    return data