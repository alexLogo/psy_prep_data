from copy import deepcopy
from imblearn.over_sampling import SMOTE , BorderlineSMOTE, SVMSMOTE
import numpy as np


def upsample_data(X_train, y_train):
    sm = SMOTE(random_state=42)
    
    X_res, y_res = sm.fit_resample(X_train, y_train)
    
    return X_res, y_res 



def enlarge_fake_data(x,y,k):
    new_x = deepcopy(x)
    new_y = 1-y
    
    x_list = [new_x for i in range(k)]
    y_list = [new_y for i in range(k)]
    
    x_list.append(x)
    y_list.append(y)
    
    new_x = np.concatenate(x_list, axis=0)
    new_y = np.concatenate(y_list, axis=0)
    
    return new_x, new_y


def filter_by_label(x,y,label):
    idx = [i for i in range(len(y)) if y[i] == label]
    
    return x[idx], y[idx]

    
def create_synthetic_data(x, y, k=5):
    sm = SMOTE(random_state=42)
    #sm = SVMSMOTE(random_state=4)
    
    
    x_0, y_0 = filter_by_label(x,y,0)
    x_1, y_1 = filter_by_label(x,y,1)
    
    x = [x_0, x_1]
    y = [y_0, y_1]
    
    majority = int(len(x_1) > len(x_0))
    
    x[majority], y[majority] = enlarge_fake_data(x[majority], y[majority], k)
    x[majority], y[majority] = sm.fit_resample(x[majority], y[majority])
    x[majority], y[majority] = filter_by_label(x[majority], y[majority],majority)
    
    x = np.concatenate(x, axis=0)
    y = np.concatenate(y, axis=0)
    
    x, y = sm.fit_resample(x, y)

    
    return x, y 
