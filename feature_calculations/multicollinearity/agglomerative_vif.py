import time
import numpy as np
from progressbar import progressbar
from statsmodels.stats.outliers_influence import variance_inflation_factor


import pathes
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_k_subjects, read_features
from feature_calculations.multicollinearity.util import drop, top_k_indices, update_subjects
from feature_calculations.multicollinearity.Agglomerative import Agglomerative_clustring

MAX_SIZE = 1000
NUM_OF_CLUSTERS = 1
THRESHOLD = 5
NUM_OF_SUBJECTS = 10
EPOCH = 0


def get_features_names(cluster, original_features_names):
    # get names of those features
    names = list(original_features_names.to_series().iloc[cluster])
    
    return names


if __name__ == '__main__':
    # read data
    print("Read data")
    data_raw = read_k_subjects(range(1,NUM_OF_SUBJECTS+1), mode=cfg.filtering_base[EPOCH], z=True)
    data = data_raw.iloc[:,3:]
    
    # original feature name list
    original_features_names = data.columns

    # eliminated features list
    eliminated_features = set()
    
    # Clustering
    print("Starting clustering process:")
    clustering = Agglomerative_clustring(max_size=MAX_SIZE, n_clusters=NUM_OF_CLUSTERS)
    corr = np.corrcoef(data.to_numpy().T)
    distance = 1 - abs(corr)
    clustering.fit(distance)
    
    # iterate over the components (most significant):
    for i, cluster in enumerate(clustering.cluster_sets):
        print(f"Analyzing the {i+1}th cluster from {len(clustering.cluster_sets)}")
        print(f"Cluster size: {len(cluster)}")
        if len(cluster) < 2:
            print("Cluster is too small")
            continue
        cluster = list(cluster)
        # get list of m features
        m_features = get_features_names(cluster, original_features_names)
        
        # create subtable of only this features
        sub_data = data.loc[:, m_features]
        # loop until no VIF passes the threshold:
        out_flag = True
        # create vif deictionary
        vifs = {item:100 for item in m_features}
        while out_flag:
            # initialize flag
            out_flag = False
            # iterate over the remaining features and calculate the VIF
            for name, value in vifs.items():
                # if the vif score is lower than threshold, continue
                if value < THRESHOLD:
                    continue
                idx = list(sub_data.columns).index(name)
                vif = variance_inflation_factor(sub_data.to_numpy(), idx)
                vifs[name] = vif
            
            # find the maximal VIF name
            max_name = max(vifs, key=vifs.get)
            max_vif = vifs[max_name]
            # if higher than threshold:
            if max_vif > THRESHOLD:
                # add to eliminated list
                eliminated_features.add(max_name)
                # throw away from the subtable
                drop(sub_data, max_name)
                # throw away this featrue from the dictionary
                del vifs[max_name]
                # continue the loop
                out_flag = True
            
        print(f"Component {i+1}: {len(m_features)-len(sub_data.columns)} features have been deleted")
        print(f"Total: {len(eliminated_features)}")
    
    # delete correlated columns from all data
    update_subjects(eliminated_features, EPOCH)
                
                