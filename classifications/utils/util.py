import numpy as np
import pandas as pd
import pickle

import pathes

def weights_calculation(labels):
    unique, counts = np.unique(labels, return_counts=True)
    
    weights = [1, counts[0]/counts[1]]
    
    return weights 


def save_results(results, name):
    results = pd.DataFrame(results)
    results.to_csv(pathes.result_path + name + ".csv", header=None, index=None)


def save_models(models, name):
    with open(f'{pathes.models_path}{name}.pickle', 'wb') as handle:
        pickle.dump(models, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def save_matrices(matrices, name):
    with open(f'{pathes.matrices_path}{name}.pickle', 'wb') as handle:
        pickle.dump(matrices, handle, protocol=pickle.HIGHEST_PROTOCOL)


def results_mean(results):
    res = np.array(results)
    res = res[:, 1:]
    mean = np.mean(res, axis=0)
    return mean


def sum_matrices(matrices):
    # initialize the total matrices as the first matrices list on the list 
    sum_matrices = matrices[0]
    
    # add to the sum list the missed subject, the first element of the second matrices list
    sum_matrices = [matrices[1].pop(0)] + sum_matrices 
    
    # deletes the first column from the sum list and cast the rest into ndarray
    sum_matrices = [np.array(x[1:]) for x in sum_matrices]
    
    #iterate over the rest of the matrices lists
    for subject_model_matrices in matrices[1:]:
        # iterate over the subject performance matrices
        for subject_matrices in subject_model_matrices:
            idx = subject_matrices[0] - 1
            matrices = np.array(subject_matrices[1:])
            sum_matrices[idx] += matrices
            
    return sum_matrices

def sum_results(results):
    # initialize the total matrices as the first matrices list on the list 
    sum_results = results[0]
    # add to the sum list the missed subject, the first element of the second matrices list
    sum_results = [results[1].pop(0)] + sum_results 
    
    # deletes the first column from the sum list and cast the rest into ndarray
    sum_results = [np.array(x[1:]) for x in sum_results]
    
    #iterate over the rest of the matrices lists
    for subject_model_results in results[1:]:
        # iterate over the subject performance matrices
        for subject_results in subject_model_results:
            idx = subject_results[0] - 1
            results_temp = np.array(subject_results[1:])
            sum_results[idx] += results_temp
    
    sum_results = [x/(len(results)-1) for x in sum_results]
            
    return sum_results
            


def inner_shuffle(Y, Z):
    Y = pd.Series(Y)
    Z = pd.Series(Z)
    
    uniques = list(Z.unique())
    
    new_y = []
    for value in uniques:
        partial_Y = Y[Z==value]
        new_partial = list(partial_Y)
        np.random.shuffle(new_partial)
        partial_Y = pd.Series(new_partial, index=partial_Y.index)
        new_y.append(partial_Y)
     
    new_y = pd.concat(new_y)
    new_y = new_y.sort_index()
    Y = np.array(new_y)
    
    return Y
    