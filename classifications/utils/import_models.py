import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

import pathes

def import_model(subject_idx, test_idx, file_name):
    path = pathes.models_path + file_name + '.pickle'
    with open(path, 'rb') as file:
        models = pickle.load(file)
        
        if isinstance(models[0][0], int):
            models = [x[1:] for x in models]
            
    relevant_models = models[subject_idx][test_idx]
    
    mean_model = np.mean(relevant_models, axis=0)
    
    model = LogisticRegression()
    
    model.intercept_ = mean_model[0:1]
    model.coef_ = mean_model[1:].reshape(1,-1)
    model.classes_ = np.array([0,1],dtype=np.int32)
    
    return model
    
    