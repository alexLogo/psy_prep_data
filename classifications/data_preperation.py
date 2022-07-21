import numpy as np
from copy import deepcopy
from feature_calculations.read_features import read_features
from classifications.utils.filter_creator import create_filter
from classifications.utils.labeler_creator import create_labeler
from classifications.utils.normalize_featrues import feature_normalization

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
    
    # Z is array that contain the other label we keep it in order be able to
    # apply more sophisticated calculations later on
    Z = data[:, 3-idx]
    Y = np.array(labels)
    X = data[:, cfg.header_size:]
    
    return X, Y, Z

def prepre_data(participant, filtering_cfg, labeling_cfg, reading_mode = "clean", data_read=False, feature_normalization_flag=-1):
    # read subject data
    if data_read:
        data = read_features(participant, reading_mode)
    else:
        data = participant
        
    # check whether to normalize the features according to one of the labels
    if feature_normalization_flag > 0:
        data = feature_normalization(data, feature_normalization_flag)
        
    data = np.array(data)
    
    
    # choose relevant trials
    data = filter_trials(data, *filtering_cfg)
    
    X, Y, Z = labeling(data, *labeling_cfg)
    
    return X, Y, Z


def prepre_data_all(data, filtering_cfg, labeling_cfg, feature_normalization_flag=-1):
    data = deepcopy(data)
    for i in cfg.participants_range:
        subject = data[i-1]
        if feature_normalization_flag > 0:
            subject = feature_normalization(subject, feature_normalization_flag)
        
        subject = np.array(subject)
        
        # choose relevant trials
        subject = filter_trials(subject, *filtering_cfg)
        
        X, Y, Z = labeling(subject, *labeling_cfg)
        
        data[i-1] = (X, Y, Z)
    return data
 


