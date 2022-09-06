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
from classifications.utils.import_models import import_model
import pathes
from warnings import simplefilter
simplefilter(action='ignore')



# this function return true if the data set isn't passing the threshold
def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def run_test(data, test, model, feature_normalization_flag=-1, weight_flag=False, iterations=1,
             smote=False, k=5, covariat=False, trained_model=False, thresholds=cfg.class_threshold):
        
        # filter & label the data accordind to the test 
        X, Y, Z = prepre_data(data, test['filter'], test['labeler'], feature_normalization_flag=feature_normalization_flag)
        
        # if iteration != 1, shuffle Y according to Z
        if iterations > 1:
            Y = util.inner_shuffle(Y,Z)
        
        # unconfound the data, if necessesry
        if test['unconfound']:
            X, Y, Z = soa_unconfound(X, Y, Z)
        
        if covariat:
            X = np.concatenate((Z.reshape(-1,1), X), axis=1)
            
        # check whether the test is passing the threshold
        if threshold(Y, thresholds[test['validation']]):
            return -1,-1,-1
        
        # apply the model, evalute model performance, and return foldsw models betas
        auc, model_weights, matrix = evaluate(X, Y, Z, model=model, validation_method=test['validation'], 
                            weight_flag=weight_flag, smote=smote, k=k, covariat=covariat,
                            trained_model=trained_model)
        
        return auc, model_weights, matrix



def analysis(model, test_set=cfg.tests_configurations, thresholds=cfg.class_threshold, weight_flag=False, 
             feature_mode="clean", smote=False,k=0, feature_normalization_flag=-1, save_models="", 
             fitted_model = False, filename="", covariat=False, iterations=1):
    results = []
    models = []
    matrices = []
    # iterate over the subjects
    for i in cfg.participants_range:
        print(f"analysing subject {i}")
        
        # read subject data
        data = read_features(i, mode=feature_mode)
        #data = random_read(i)
        # build current subject results list
        subject_results = [i]
        subject_models = []
        subject_matrices = []
        
        # read model if necessary
        if fitted_model :
            model = import_model(i-1,0, filename)
        
        # iterate over the tests
        for test in test_set:
            print(f"test: {test['name']}")
            for _ in range(iterations):
                auc, model_weights, matrix = run_test(data, test, model, feature_normalization_flag=feature_normalization_flag, 
                                                      weight_flag=weight_flag, smote=smote, k=k, 
                                                      covariat=covariat, trained_model=fitted_model, 
                                                      thresholds=thresholds, iterations=iterations)
                
                # add AUC to results list
                subject_results.append(auc)
                subject_models.append(model_weights)
                subject_matrices.append(matrix)
            
                # save models, if required
                if save_models != "":
                    save_model(save_models, i, test['name'], model_weights)
            
        results.append(subject_results)
        models.append(subject_models)
        matrices.append(subject_matrices)
        
    return results, models, matrices



if __name__ == "__main__":
    np.random.seed(cfg.np_seed)
    name = "rf_importance"
    model =  RandomForestClassifier()
    testset = [{'name': 'all agency', 'filter' :(1, [0,1,2,3,4]), 'labeler': (1, {0:0, 1:1, 2:1, 3:1, 4:1}), 'validation':'cv', 'unconfound' : False}]
    res, models, matrices = analysis(model, weight_flag=False, smote=False, k=5, test_set=testset[:1], 
                   feature_mode='mult', feature_normalization_flag=-1, fitted_model=False, filename="results_pupil",
                   covariat=False, iterations=1)
    util.save_results(res, name)
    #util.save_matrices(matrices, name)
    util.save_models(models, name)