import time

import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_features
from feature_calculations.multicollinearity.threshold import create_threshold_function
from feature_calculations.multicollinearity.filter_functions import *
from feature_calculations.multicollinearity.util import drop_list, update_subjects
import pathes

THRESHOLD_FUN = [0,create_threshold_function(create_vif_filter(-1), 5, np.min),
                 create_threshold_function(create_corr_filter(.9), 1, np.min),
                 create_threshold_function(create_corr_filter(.8), 2, np.min),
                 create_threshold_function(create_vif_filter(30), 10, np.min),
                 create_threshold_function(create_vif_filter(50), 10, np.min),
                 create_threshold_function(create_vif_filter(30), 5, np.min),
                 create_threshold_function(create_vif_filter(100), 5, np.min),
                 create_threshold_function(create_vif_filter(150), 5, np.min)]



        


if __name__ == "__main__":
    for epoch in range(1,2):
        start = time.time()
    
        data = [read_features(i, cfg.filtering_base[epoch]) for i in range(1, cfg.subjects_for_multi_calculation+1)]
        data = [x.iloc[:,3:] for x in data]
        
        total_columns = []
        epoch_columns = [0]
        epoch_num = 0
        
        threshold_fun = THRESHOLD_FUN[epoch]
        
        while len(epoch_columns) > 0 and epoch_num == 0:
            epoch_columns = []
            epoch_num += 1
            print('********')
            print(f"epoch: {epoch_num}")
            print('********')
            
            for feature in data[0].columns:
                idx = data[0].columns.to_list().index(feature)
                
                if threshold_fun(data, idx):
                    print(f"droping {feature}")
                    drop_list(data, feature)
                    epoch_columns.append(feature)
                    
                if len(epoch_columns) % 100 == 0:
                    print(f"{len(epoch_columns)} had been deleted")
                    print(f"{len(data[0].columns)} features had been left")
                    end = time.time()
                    print(f"{end - start} had pass")
            total_columns += epoch_columns
        
        # delete correlated columns from all data
        update_subjects(total_columns, epoch)
        
        end = time.time()
        print(f"Epoch{epoch} total time: {end - start}" )