import time
from progressbar import progressbar
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_k_subjects, read_features
from feature_calculations.multicollinearity.threshold import create_threshold_function_v2
from feature_calculations.multicollinearity.filter_functions import *
from feature_calculations.multicollinearity.util import drop, update_subjects

import pathes

THRESHOLD_FUN = [create_threshold_function_v2(create_corr_filter(.9), 1),
                 create_threshold_function_v2(create_vif_filter(-1), 10),
                 create_threshold_function_v2(create_vif_filter(-1), 5),
                 create_threshold_function_v2(create_vif_filter(200), 10),
                 create_threshold_function_v2(create_vif_filter(-1), 10),
                 create_threshold_function_v2(create_vif_filter(100), 10),
                 create_threshold_function_v2(create_vif_filter(400), 5),
                 create_threshold_function_v2(create_vif_filter(-1), 10),
                 create_threshold_function_v2(create_vif_filter(-1), 5)]


        


if __name__ == "__main__":
    for epoch in range(2,3):
        start = time.time()
    
        data = read_k_subjects(range(1,11), mode=cfg.filtering_base[epoch])
        data = data.iloc[:,3:]
        
        drop_columns = []
        
        threshold_fun = THRESHOLD_FUN[epoch]
            
        for feature in progressbar(data.columns, redirect_stdout=False):
        #for feature in data.columns:
            idx = data.columns.to_list().index(feature)
            
            if threshold_fun(data, idx):
                drop(data, feature)
                drop_columns.append(feature)
                
                if len(drop_columns) % 100 == 0:
                    print(f"{len(drop_columns)} had been deleted")
                    print(f"{len(data.columns)} features had been left")
                    end = time.time()
                    print(f"{end - start} had pass")
        
        # delete correlated columns from all data
        update_subjects(drop_columns, epoch)

        end = time.time()
        print(f"Epoch{epoch} total time: {end - start}" )