import numpy as np
from copy import deepcopy
from feature_calculations.read_features import read_features
from classifications.utils.filter_creator import create_filter
from classifications.utils.labeler_creator import create_labeler
import classifications.configurations as cfg


def filter_trials(data, idx, accepted_trials):
    idx_list = []
    trials_filter = create_filter(idx, accepted_trials)
    for i, row in enumerate(data):
        if trials_filter(row[:cfg.header_size]):
            idx_list.append(i)
            
    return data[idx_list]
    

def labeling(data, idx, class_dict):
    labels = []
    labeler = create_labeler(idx, class_dict)
    for i, row in enumerate(data):
        labels.append(labeler(row[:cfg.header_size]))
    
    # Z is array that contain the manipulation type of each trial, we keep it in order be able to
    # unconfound the data when performing agency classification
    Z = data[:, 1]
    Y = np.array(labels)
    X = data[:, cfg.header_size:]
    
    return X, Y, Z

def prepre_data(participant, filtering_cfg, labeling_cfg, reading_mode = "clean", data_read=False):
    # read subject data
    if data_read:
        data = read_features(participant, reading_mode)
    else:
        data = participant
        
    data = np.array(data)
    
    # choose relevant trials
    data = filter_trials(data, *filtering_cfg)
    
    X, Y, Z = labeling(data, *labeling_cfg)
    
    return X, Y, Z


def prepre_data_all(data, filtering_cfg, labeling_cfg):
    data = deepcopy(data)
    for i in cfg.participants_range:
        subject = np.array(data[i-1])
    
        # choose relevant trials
        subject = filter_trials(subject, *filtering_cfg)
        
        X, Y, Z = labeling(subject, *labeling_cfg)
        
        data[i-1] = (X, Y, Z)
    return data
 


