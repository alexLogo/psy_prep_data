import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import classifications.configurations as cfg
from classifications.data_preperation import prepre_data
from feature_calculations.read_features import read_features
from classifications.utils.smote import create_synthetic_data, upsample_data
from classifications.utils import util


def build_model(model, subject, feature_mode, smote=False, k=0):
    data = read_features(subject, mode=feature_mode)
    X, Y, Z = prepre_data(data, cfg.tests_configurations[0]['filter'], cfg.tests_configurations[0]['labeler'])
    if smote:
        X, Y = create_synthetic_data(X, Y , k=k)
    else:
        X, Y  = upsample_data(X, Y)
    
    # standardize data
    sc = StandardScaler()
    X = sc.fit_transform(X)
    
    # fit model        
    model.fit(X, Y)
    
    return model, sc


def evaluate_model(X, Y, model, sc, smote=False, k=0):
    X = sc.transform(X)
    
    # calculate probablity
    y_hat = model.predict_proba(X)
    y_prob = list(y_hat[:,1])
    
    y_hat = model.predict(X)
    
    auc = roc_auc_score(Y, y_prob)
    matrix = confusion_matrix(Y, y_hat, labels=[1,0])
    
    return auc, matrix


def one_subject_model_base_analysis(model, subject=1, test_set=cfg.objective_tests,
             feature_mode="mult1", smote=False, k=0, feature_normalization_flag=-1, save_models=""):
    
    results = []
    matrices = []
    
    model, sc = build_model(model, subject, feature_mode, smote=smote, k=k)
    
    for i in cfg.participants_range:
        if i == subject:
            continue
        
        
        # read subject data
        data = read_features(i, mode=feature_mode)
        # build current subject results list
        subject_results = [i]
        matrices_results = [i]
        # iterate over the tests
        for test in test_set:
            # filter & label the data accordind to the test 
            X, Y, Z = prepre_data(data, test['filter'], test['labeler'], feature_normalization_flag=feature_normalization_flag)
            

            
            # apply the model, evalute model performance, and return foldsw models betas
            auc, matrix = evaluate_model(X, Y, model=model, sc=sc, smote=smote, k=k)
            
            # add AUC to results list
            subject_results.append(auc)
            matrices_results.append(matrix)
            
        results.append(subject_results)
        matrices.append(matrices_results)
        
    return results, matrices

def subjects_iterations(mode='mult1'):
    model =  LogisticRegression()
    results = []
    matrices = []
    for i in cfg.participants_range:
        print(f"analysing subject {i}")
        res, mat = one_subject_model_base_analysis(model, subject=i, feature_normalization_flag=-1, 
                                                   test_set=cfg.objective_tests, feature_mode=mode)
        
        #results.append([i] + list(util.results_mean(res)))
        results.append(res)
        matrices.append(mat)
    
    results = util.sum_results(results)
    matrices = util.sum_matrices(matrices)
    return results, matrices

    
if __name__ == "__main__":
    name = "results_pupil_one"
    model =  LogisticRegression()
    res, matrices = subjects_iterations()
    util.save_results(res, name)
    util.save_matrices(matrices, name)
    