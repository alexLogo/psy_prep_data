import numpy as np
import feature_calculations.configurations as cfg

def create_threshold_function(fun, threshold, generalize_fun):
    def threshold_filter(data_array, idx):
        # calculate measurments for each participant
        measurements = np.array([fun(data, idx) for data in data_array])
        # filter nans out
        measurements = measurements[~np.isnan(measurements)]
        # if the array is almost empty (predefined threshold), return true
        if len(measurements) <= cfg.minimum_unnan:
            return True
        # extract one measure as a representation of the distribution (default=min)
        measure = generalize_fun(measurements)
        
        return measure > threshold
    
    return threshold_filter


def create_threshold_function_v2(fun, threshold):
    def threshold_filter(data, idx):
        measure = fun(data, idx)
        #print(f"{measure:.2f}")
        return measure > threshold
    
    return threshold_filter

        