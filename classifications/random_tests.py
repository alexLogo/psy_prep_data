import numpy as np

import classifications.configurations as cfg
from classifications.data_preperation import prepre_data
from classifications.utils.unconfound import soa_unconfound
from feature_calculations.read_features import read_features
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


def analysis(model, test_set=cfg.tests_random_configurations, thresholds=cfg.class_threshold, weight_flag=False, 
             feature_mode="clean", smote=False,k=0, num_of_iterations=100):
    results = []
    np.random.seed(cfg.np_seed)
    for i in cfg.participants_range:
        print(f"analysing subject {i}")
        data = read_features(i, mode=feature_mode)
        subject_results = []
        for test in test_set:
            print(f"test: {test['name']}")
            # filter & label the data accordind to the test 
            X, Y, Z = prepre_data(data, test['filter'], test['labeler'])
            
            # unconfound the data, if necessesry
            if test['unconfound']:
                idx = soa_unconfound(Y, Z)
                X = X[idx]
                Y = Y[idx]
                Z = Z[idx]

            # check whether the test is passing the threshold
            if threshold(Y, thresholds[test['validation']]):
                subject_results.append([])
                continue
            
            # calculate random permutations of the test
            auc_list = []
            for i in range(num_of_iterations):
                np.random.shuffle(Y)
                auc, _ = evaluate(X, Y, model=model, validation_method=test['validation'], 
                                    weight_flag=weight_flag, smote=smote, k=k)
                auc_list.append(auc)
            
            # add results to subject results list
            subject_results.append(auc_list)
        
        # add subject results to results list
        results.append(subject_results)
    
    # concatenate different random permutations
    
    return results
    random_permutations_results = []
    for i in range(len(test_set)):
        res = []
        for subject in cfg.participants_range:
            res += results[subject-1][i]
        random_permutations_results.append(res)
    return random_permutations_results



if __name__ == "__main__":
    model =  LogisticRegression()
    res1 = analysis(model, weight_flag=False, num_of_iterations=100)