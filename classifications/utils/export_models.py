import os
import numpy as np
import pandas as pd

import pathes


def save_model(name, subject_num, test_name, data):
    # data into dataframe
    data = np.array(data)
    data = pd.Dataframe(data, columns = [f'Fold{x}' for x in range(1,11)])
    
    # create new directory
    path = pathes.models_path + '/' + name
    os.mkdir(path)
    
    # save the data
    path = path + '/' + f'subject_{subject_num}_test_{test_name}.csv'
    data.to_csv(path)
    