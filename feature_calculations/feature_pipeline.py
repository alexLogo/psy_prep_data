from feature_calculations.to_features_script import to_features_transformation
from feature_calculations.sort_featrues_script import sort_features
from feature_calculations.filter_zero_var_script import filter_zero
from feature_calculations.multicollinearity.full_multicollinearity_elimination_script import multicollinearaty_elimination

if __name__ == "__main__":
    # transform timeseries representation into feature representation
    to_features_transformation()
    
    # sort features
    sort_features()
    
    # eliminate zero variance features
    filter_zero()
    
    # multicollinearaty elimination
    multicollinearaty_elimination()