import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score

import classifications.configurations as cfg
from classifications.utils.smote import create_synthetic_data, upsample_data
import classifications.utils.util as util

def validation_method_decision(validation_cfg, data_len):
    if validation_cfg == "cv":
        kf = StratifiedKFold(n_splits=cfg.k_validation, shuffle=True, random_state=cfg.random_seed)
    elif validation_cfg == "lto": # leave two out without repetitions
        kf = StratifiedKFold(n_splits=data_len//2, shuffle=True, random_state=cfg.random_seed)
    
    return kf



def evaluate(X, Y, model, validation_method='cv', weight_flag=False, test_mode=False, smote=False, k=0):
    # define validation method 
    kf = validation_method_decision(validation_method, len(X))

    # initialize performance lists:
    # results: confusion matrices
    # total_true: list of "real label" order in the same way as "total_score"
    # total_score: model probability score, used to calculate AUC
    results = []
    total_true = []
    total_score = []
    
    # initialize model_weights list
    model_weights = []
    
    # iterate over the folds
    for train_index, test_index in kf.split(X, Y):
        x_train, x_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]
        
        #create weight map
        weights_map = util.weights_calculation(y_train)
        
        
        if smote:
            x_train, y_train = create_synthetic_data(x_train, y_train, k=k)
        else:
            x_train, y_train = upsample_data(x_train, y_train)
        
        # if weight_flag is on, create weight array
        if weight_flag:
            weights = [weights_map[i] for i in y_train]
        else:
            weights = None
            
        
        # standardize data
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)
        
        # fit model        
        model.fit(x_train, y_train, sample_weight=weights)
        
        # save model weights
        model_weights.append(np.concatenate((model.intercept_, model.coef_.squeeze())))
        
        # calculate confusion matrix
        y_hat = model.predict(x_test)
        results.append(confusion_matrix(y_test, y_hat))
        
        # calculate probablity
        y_hat = model.predict_proba(x_test)
        y_prob = list(y_hat[:,1])
        
        
        
        # add y and y_hat to results lists
        total_true += list(y_test)
        total_score += y_prob
        
        
    # sum up confusion matrices
    #conf = sum(results)
    # calculate auc
    auc = roc_auc_score(total_true, total_score)   
    
    # calculate confusion matrix
    confusion = sum(results)
    
    
    # in testing mode we will want to check whether the randomality is static (reproductability&static folds)
    if test_mode:
        return auc, kf.split(X)
    
    return auc, model_weights



