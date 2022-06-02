import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

import classifications.configurations as cfg
from classifications.utils import util
from classifications.data_preperation import prepre_data
from classifications.utils.unconfound import soa_unconfound
from classifications.utils.export_models import save_model
from feature_calculations.read_features import read_features, random_read
from classifications.evaluate_model import evaluate

import pathes
from warnings import simplefilter
simplefilter(action='ignore')



# this function return true if the data set isn't passing the threshold
def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def analysis(model, test_set=cfg.tests_configurations, thresholds=cfg.class_threshold, weight_flag=False, 
             feature_mode="clean", smote=False,k=0, feature_normalization_flag=-1, save_models=""):
    results = []
    models = []
    # iterate over the subjects
    for i in cfg.participants_range:
        print(f"analysing subject {i}")
        
        # read subject data
        data = read_features(i, mode=feature_mode)
        #data = random_read(i)
        # build current subject results list
        subject_results = [i]
        subject_models = [i]
        # iterate over the tests
        for test in test_set[:-1]:
            print(f"test: {test['name']}")
            # filter & label the data accordind to the test 
            X, Y, Z = prepre_data(data, test['filter'], test['labeler'], feature_normalization_flag=feature_normalization_flag)
            
            # unconfound the data, if necessesry
            if test['unconfound']:
                X, Y, Z = soa_unconfound(X, Y, Z)

            # check whether the test is passing the threshold
            if threshold(Y, thresholds[test['validation']]):
                subject_results.append(-1)
                continue
            
            # apply the model, evalute model performance, and return foldsw models betas
            auc, model_weights = evaluate(X, Y, model=model, validation_method=test['validation'], 
                                weight_flag=weight_flag, smote=smote, k=k)
            
            # add AUC to results list
            subject_results.append(auc)
            subject_models.append(model_weights)
            
            # save models, if required
            if save_models != "":
                save_model(save_models, i, test['name'], model_weights)
            
        results.append(subject_results)
        models.append(subject_models)
        
    return results, models



if __name__ == "__main__":
    name = "results1"
    model =  LogisticRegression()
    res, models = analysis(model, weight_flag=False, smote=False, k=5,test_set=cfg.objective_tests, 
                   feature_mode='mult1')
    util.save_results(res, name)
    util.save_models(res, name)