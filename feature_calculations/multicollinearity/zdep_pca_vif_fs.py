import time
import numpy as np
from sklearn.decomposition import PCA
from progressbar import progressbar
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.cluster import AgglomerativeClustering
import pathes
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_k_subjects, read_features
from feature_calculations.multicollinearity.util import drop, top_k_indices, update_subjects

NUM_OF_COMPONENTS = 100
NUM_OF_FEATURES = 100
THRESHOLD = 5
EPOCH = 1


def get_m_features(component, original_features_names):
    # get indices of top 50
    indices = top_k_indices(component, NUM_OF_FEATURES)
    # get names of those features
    names = list(original_features_names.to_series().iloc[indices])
    
    return names


if __name__ == '__main__':
    # read data
    data_raw = read_k_subjects(range(1,11), mode=cfg.filtering_base[EPOCH], z=True)
    data = data_raw.iloc[:,3:]
    
    # original feature name list
    original_features_names = data.columns

    # eliminated features list
    eliminated_features = set()
    
    # PCA
    pca = PCA(NUM_OF_COMPONENTS)
    pca.fit(data)
    
    
    # iterate over the components (most significant):
    for i, component in enumerate(pca.components_[::-1]):
        print(f"Analyzing the {i+1}th component")
        # get list of m features
        m_features = get_m_features(component, original_features_names)
        
        # filter away any feature that had been eliminated already
        m_features = [x for x in m_features if x not in eliminated_features]
        # create subtable of only this features
        sub_data = data.loc[:, m_features]
        # loop until no VIF passes the threshold:
        out_flag = True
        while out_flag:
            # initialize flag
            out_flag = False
            # define vifs container
            vifs = []
            # iterate over the remaining features and calculate the VIF
            for j in range(len(sub_data.columns)):    
                vif = variance_inflation_factor(sub_data.to_numpy(), j)
                vifs.append(vif)
            
            # find the maximal VIF name
            vifs = np.array(vifs)
            max_idx = vifs.argmax()
            max_vif = vifs[max_idx]
            # if higher than threshold:
            if max_vif > THRESHOLD:
                # find relevant feature
                feature = sub_data.columns[max_idx]
                # add to eliminated list
                eliminated_features.add(feature)
                # throw away from the subtable
                drop(sub_data, feature)
                # continue the loop
                out_flag = True
            
        print(f"Component {i}: {len(m_features)-len(sub_data.columns)} features have been deleted")
        print(f"Total: {len(eliminated_features)}")
    
    # delete correlated columns from all data
    update_subjects(eliminated_features, EPOCH)
                
                