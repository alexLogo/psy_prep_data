import numpy as np

from statsmodels.stats.outliers_influence import variance_inflation_factor

import pathes
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_k_subjects, read_features
from feature_calculations.multicollinearity.util import drop_list, top_k_indices, update_subjects
from feature_calculations.multicollinearity.Agglomerative import Agglomerative_clustring

THRESHOLD = 5
NUM_OF_SUBJECTS = 10
EPOCH = 0


def calculate_vif(data, idx, fun=np.min):
    vif_list = []
    for subject in data:
        vif = variance_inflation_factor(subject.to_numpy(), idx)
        vif_list.append(vif)
    
    value = fun(vif_list)
    return value


if __name__ == '__main__':
    # read data
    print("Read data")
    data = [read_features(i, mode='clean') for i in range(1, cfg.subjects_for_multi_calculation+1)]
    data = [x.iloc[:,3:] for x in data]
    
    # original feature name list
    original_features_names = data[0].columns

    # eliminated features list
    eliminated_features = set()
    
    
    out_flag = True
    # create vif deictionary
    vifs = {item:100 for item in original_features_names}
    while out_flag:
        # initialize flag
        out_flag = False
        # iterate over the remaining features and calculate the VIF
        for name, value in vifs.items():
            # if the vif score is lower than threshold, continue
            if value < THRESHOLD:
                continue
            idx = list(data[0].columns).index(name)
            vif = calculate_vif(data, idx, fun=np.median)
            vifs[name] = vif
        
        # find the maximal VIF name
        max_name = max(vifs, key=vifs.get)
        max_vif = vifs[max_name]
        # if higher than threshold:
        if max_vif > THRESHOLD:
            # add to eliminated list
            eliminated_features.add(max_name)
            # throw away from the subtable
            drop_list(data, max_name)
            # throw away this featrue from the dictionary
            del vifs[max_name]
            # continue the loop
            out_flag = True
            # print report
            print(f"{max_name} have been deleted, VIF:{max_vif}")
            
    print(f"Total: {len(eliminated_features)}")
    
    # delete correlated columns from all data
    # update_subjects(eliminated_features, EPOCH)
                
                