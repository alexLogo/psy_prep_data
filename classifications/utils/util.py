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
    with open(f'{pathes.models_path} + {name}.pickle', 'wb') as handle:
        pickle.dump(models, handle, protocol=pickle.HIGHEST_PROTOCOL)

