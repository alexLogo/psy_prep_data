import os
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_features


def top_k_indices(data, k):
    data_and_index = [(i, data[i]) for i in range(len(data))]
    data_and_index.sort(key=lambda x: x[1])
    indices = [x[0] for x in data_and_index[-k:]]
    return indices 


def drop_list(data, feature):
    for i in range(len(data)):
        data[i].drop(feature, axis=1, inplace=True)


def drop(data, feature):
    data.drop(feature, axis=1, inplace=True)


def update_subjects(eliminited_features_list, epoch=-1):
    
    # delete correlated columns from all data
    for i in cfg.participants_range:
        print(f"rewriting participant {i}")
        data = read_features(i, 'clean')
        data.drop(eliminited_features_list, axis=1, inplace=True)
        
        data.to_csv(cfg.pathes.minimal_feature_path+"participant"+str(i)+".csv", index=False)



'''
deprecated
def update_subjects(eliminited_features_list, epoch=):
    if not os.path.isdir(cfg.filtering_to_path[epoch]):
        os.mkdir(cfg.filtering_to_path[epoch])
    
    # delete correlated columns from all data
    for i in cfg.participants_range:
        print(f"rewriting participant {i}")
        data = read_features(i, cfg.filtering_base[epoch])
        data.drop(eliminited_features_list, axis=1, inplace=True)
        
        data.to_csv(cfg.filtering_to_path[epoch]+"participant"+str(i)+".csv", index=False)

'''