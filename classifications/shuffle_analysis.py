import numpy as np
from sklearn.linear_model import LogisticRegression

import classifications.configurations as cfg
from classifications.data_preperation import prepre_data
from feature_calculations.read_features import read_features, random_read
from classifications.utils.unconfound import soa_unconfound
from classifications.utils.export_models import save_model
from classifications.evaluate_model import evaluate
from classifications.utils.import_models import import_model
from warnings import simplefilter
simplefilter(action='ignore')



# this function return true if the data set isn't passing the threshold
def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def run_test(data, test, model, feature_normalization_flag=-1, weight_flag=False, 
             smote=False, k=5, covariat=False, trained_model=False, thresholds=cfg.class_threshold):
        print(f"test: {test['name']}")
        # filter & label the data accordind to the test 
        X, Y, Z = prepre_data(data, test['filter'], test['labeler'], feature_normalization_flag=feature_normalization_flag)
        
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



def shuffle_results(model, test_set=cfg.tests_configurations, thresholds=cfg.class_threshold, 
             feature_mode="clean", smote=False,k=0, fitted_model = False, filename="", iterations=100):
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
            for i in range(iterations)
                auc, model_weights, matrix = run_test(data, test, model, feature_normalization_flag=feature_normalization_flag, 
                                                      weight_flag=weight_flag, smote=smote, k=k, 
                                                      covariat=covariat, trained_model=fitted_model, 
                                                      thresholds=thresholds)
                
                # add AUC to results list
                subject_results.append(auc)
                subject_models.append(model_weights)
                subject_matrices.append(matrix)
            
            
        results.append(subject_results)
        models.append(subject_models)
        matrices.append(subject_matrices)
        
    return results, models, matrices



if __name__ == "__main__":
    name = "results1_sub_model"
    model =  LogisticRegression()
    res, models, matrices = analysis(model, weight_flag=False, smote=False, k=50,test_set=cfg.subjective_tests, 
                   feature_mode='mult1', feature_normalization_flag=-1, fitted_model=True, filename="results1",
                   covariat=False)
    #util.save_results(res, name)
    #util.save_matrices(matrices, name)
    #util.save_models(models, name)