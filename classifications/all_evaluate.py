import numpy as np
import pandas as pd
from classifications.data_preperation import prepre_data_all
from classifications.utils.unconfound import soa_unconfound
from feature_calculations.read_features import read_all_data
import classifications.configurations as cfg
from sklearn.model_selection import KFold, LeavePOut
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from classifications.utils.smote import create_synthetic_data, upsample_data
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings("ignore")

def save_all_results(results, name):
    results = np.array(results).T
    results = np.concatenate((np.arange(len(results)).reshape(-1,1), results), axis=1)
    results = pd.DataFrame(results)
    results.to_csv(cfg.pathes.result_base_clean_feature_path + name + ".csv", header=None, index=None)



def concat(data):
    X = [x[0] for x in data]
    Y = [x[1] for x in data]
    
    X = np.concatenate(X, axis=0)
    Y = np.concatenate(Y, axis=0)
    
    return X, Y


def evaluate(data, model, validation_method, weight_flag=False, test_mode=False, smote=False, k=0):
    
    kf = KFold(n_splits=cfg.k_validation, shuffle=True, random_state=cfg.random_seed)
    
    results = []
    total_true = []
    total_score = []
    
    # iterate over the folds
    for train_index, test_index in kf.split(data):
        train = [data[i] for i in range(len(data)) if i in train_index]
        test = [data[i] for i in range(len(data)) if i in test_index]
        x_train, y_train = concat(train)
        #x_test, y_test = concat(test)
        
        
        x_train, y_train = upsample_data(x_train, y_train)
        
            
        # standartize data
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        
        for test_subject in test:
            x_test, y_test, _ = test_subject
            x_test = sc.transform(x_test)
            
            # fit model        
            model.fit(x_train, y_train)
            
            
        
            # calculate probablity
            y_hat = model.predict_proba(x_test)
            y_prob = list(y_hat[:,1])
        
            auc = roc_auc_score(y_test, y_prob)   
            
            results.append(auc)
        
        
    # sum up confusion matrices
    #conf = sum(results)
    # calculate auc
    return results

def evaluate2(data, model, validation_method, weight_flag=False, test_mode=False, smote=False, k=0):
    
    
    results = []
    total_true = []
    total_score = []
    
    # iterate over the folds
    for subject in range(len(data)-16):
        print(subject)
        train = [data[i] for i in range(len(data)) if i != subject]
        test = data[subject]
        x_train, y_train = concat(train)
        #x_test, y_test = concat(test)
        
        
        x_train, y_train = upsample_data(x_train, y_train)
        
            
        # standartize data
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        
        x_test, y_test, _ = test
        
        # not enough test data
        if len(y_test) < 18:
            results.append(-1)
            continue
            
        x_test = sc.transform(x_test)
        
        # fit model        
        model.fit(x_train, y_train)
        
        
    
        # calculate probablity
        y_hat = model.predict_proba(x_test)
        y_prob = list(y_hat[:,1])
    
        auc = roc_auc_score(y_test, y_prob)   
        
        results.append(auc)
        
        
    # sum up confusion matrices
    #conf = sum(results)
    # calculate auc
    return results

        

def threshold(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    if len(counts) < 2:
        return True
    return min(counts) < threshold


def analysis(model, test_set=cfg.subjective_tests, thresholds=cfg.class_threshold, weight_flag=False, 
             feature_mode="clean", smote=False,k=0, feature_normalization_flag=-1):
    
    data = read_all_data(mode=feature_mode)
    results = []
    for test in test_set:
        test_data = prepre_data_all(data, test['filter'], test['labeler'], feature_normalization_flag=feature_normalization_flag)
        print(test['name'])
        # unconfound the data, if necessesry
        if test['unconfound']:
            for i in range(len(test_data)):
                X, Y, Z = test_data[i]
                X, Y, Z = soa_unconfound(X, Y, Z)
                test_data[i] = X, Y, Z
                
        auc = evaluate2(test_data, model=model, validation_method=test['validation'], 
                            weight_flag=weight_flag, smote=smote, k=k)
        
        results.append(auc)
        
    return results
                
        
                
if __name__ == "__main__":
    model =  RandomForestClassifier(max_depth=5, n_estimators=1000)
    model = LogisticRegression()
    res = analysis(model, weight_flag=False, smote=False, feature_mode='clean', feature_normalization_flag=1)
    #save_all_results(res, "handcraft_cross")