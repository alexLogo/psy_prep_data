import numpy as np
import pandas as pd

import classifications.configurations as cfg
from classifications.data_preperation import prepre_data
from classifications.utils.unconfound import soa_unconfound
from feature_calculations.read_features import read_features
from classifications.evaluate_model import evaluate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pathes
from warnings import simplefilter
simplefilter(action='ignore')


def save_results(results, name):
    results = pd.DataFrame(results)
    results.to_csv(pathes.result_base_clean_feature_path + name + ".csv", header=None, index=None)

# this function return true if the data set isn't passing the threshold
def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def analysis(model, test_set=cfg.tests_configurations, thresholds=cfg.class_threshold, weight_flag=False, 
             feature_mode="clean", smote=False,k=0):
    results = []
    
    for i in cfg.participants_range:
        print(f"analysing subject {i}")
        data = read_features(i, mode=feature_mode)
        subject_results = [i]
        for test in test_set:
            print(f"test: {test['name']}")
            # filter & label the data accordind to the test 
            X, Y, Z = prepre_data(data, test['filter'], test['labeler'])
            
            # unconfound the data, if necessesry
            if test['unconfound']:
                X, Y, Z = soa_unconfound(X, Y, Z)

            # check whether the test is passing the threshold
            if threshold(Y, thresholds[test['validation']]):
                subject_results.append(-1)
                continue
            
            auc, mat = evaluate(X, Y, model=model, validation_method=test['validation'], 
                                weight_flag=weight_flag, smote=smote, k=k)
            
            subject_results.append(auc)
            
        results.append(subject_results)
        
    return results



if __name__ == "__main__":
    model =  LogisticRegression()
    res = analysis(model, weight_flag=False, smote=True, k=5,test_set=cfg.tests_configurations, feature_mode='handcraft')
    save_results(res, "handcraft")