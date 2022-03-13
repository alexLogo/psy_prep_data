import numpy as np

import classifications.configurations as cfg
from classifications.data_preperation import prepre_data
from classifications.utils.unconfound import soa_unconfound
from feature_engineering.read_features import read_features
from classifications.evaluate_model import evaluate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from warnings import simplefilter
simplefilter(action='ignore')


# this function return true if the data set isn't passing the threshold
def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def calculate_size(thresholds=cfg.class_threshold):    
    size = []
    for i in cfg.participants_range:
        test = cfg.tests_configurations[2]
        print(f"analysing subject {i}")
        data = read_features(i)
        # filter & label the data accordind to the test 
        X, Y, Z = prepre_data(data, test['filter'], test['labeler'])
        
        # unconfound the data
        idx = soa_unconfound(Y, Z)
        X = X[idx]
        Y = Y[idx]
        Z = Z[idx]

        # check whether the test is passing the threshold
        if threshold(Y, thresholds[test['validation']]):
            size.append(-1)
            continue
        
        size.append(len(idx))
        
        
    return size



if __name__ == "__main__":
    size = calculate_size()