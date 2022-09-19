import numpy as np
from feature_calculations.read_features import read_features
from statsmodels.stats.outliers_influence import variance_inflation_factor



def top_feature_indices(array, num):
    indices = np.argpartition(array, kth=-num)[-num:]
    array = array[indices]
    
    idx_max = np.argmax(array)
    
    return indices, idx_max

def correlation(array, idx):
    array = array.to_numpy()
    
    # normalize the data
    norm_array = array - np.mean(array, axis=0)
    
    # extract the chosen feature
    feature = norm_array[:,idx]
    
    # multiple the feature by the data matrix
    cov = np.matmul(norm_array.T, feature)
    
    # normalize covariance
    to_norm = np.sqrt(np.sum(norm_array ** 2, axis=0)) * np.sqrt(np.sum(feature ** 2))
    corr = cov / to_norm
    
    return corr


def create_corr_filter(threshold):
    def high_corr(data, idx):
        # calculate correlation
        corr = correlation(data, idx)
        # calculate high correlation
        high_corr = np.abs(corr) > threshold
        return np.sum(high_corr)
    
    return high_corr


def create_vif_filter(num_of_correlates):
    def all_vif(data, idx):
        vif = variance_inflation_factor(data.to_numpy(), idx)
        return vif
    
    def high_vif(data, idx):
        # calculate correlation
        corr = correlation(data, idx)
        #absolute value
        corr = np.abs(corr)
        #filter nans away
        corr = corr[~np.isnan(corr)]
    
    def top_vif(data, idx):
        # calculate correlation
        corr = correlation(data, idx)
        #absolute value
        corr = np.abs(corr)
        #filter nans away
        corr = corr[~np.isnan(corr)]
        # if almost empty, retrun nan
        if len(corr) < num_of_correlates:
            return np.nan
        # get idx of top correlate features. +1 is because the feature itself is among them (the function return the new index of desired feature)
        indices, feature_idx = top_feature_indices(corr, num_of_correlates+1)
        # take only relevant features to calculate VIF
        data_for_vif = data.iloc[:,indices]
        # calculate vif
        vif = variance_inflation_factor(data_for_vif.to_numpy(), feature_idx)
        
        return vif
    
    if num_of_correlates == -1:
        return all_vif
    else:
        return top_vif

