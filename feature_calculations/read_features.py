import numpy as np
import pandas as pd
import feature_calculations.configurations as cfg
import pathes
from feature_calculations.utils.z_score import z_score


def path_resolver(mode):
    if mode == "base":
        feature_path = pathes.base_feature_path
    elif mode == "clean":
        feature_path = pathes.clean_feature_path
    elif mode == "handcraft":
        feature_path = pathes.handcraft_features
    elif mode == "minimal" or mode == "mult":
        feature_path = pathes.minimal_feature_path
  
    return feature_path 



def random_read(participant_num):
    feature_path = path_resolver('base')

    path = feature_path + "participant" + str(participant_num) + ".csv"
    
    data = pd.read_csv(path, header='infer')

    h = data.iloc[:, :3]
    f = data.iloc[:, 3:]
    f = f.iloc[:, cfg.random_features]
    
    data = pd.concat((h, f), axis=1)
    
    return data

def read_features(participant_num, mode="base", test=False, to_ndarray=False):
    feature_path = path_resolver(mode)

    path = feature_path + "participant" + str(participant_num) + ".csv"
    
    header = None if test else "infer"
    # read the data
    data = pd.read_csv(path, header=header)
    
    if to_ndarray:
        data = np.array(data)
        
    return data 

def read_k_subjects(subjects, mode='base', z=False):
    subjects_data = []
    for subject_num in subjects:
        data = read_features(subject_num, mode)
        header = data.columns
        if z:
            data = z_score(data.to_numpy())
        subjects_data.append(data)
        
    data = np.concatenate(subjects_data, axis=0)
    data = pd.DataFrame(data, columns=header)
    
    return data
    
    


def read_all_data(mode="base"):
    feature_path = path_resolver(mode)
    
    data = []
    for i in cfg.participants_range:
        path = feature_path + "participant" + str(i) + ".csv"
        subject = pd.read_csv(path)
        
        data.append(subject)
        
    return data