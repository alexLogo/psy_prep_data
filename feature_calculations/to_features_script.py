import pandas as pd
import feature_calculations.configurations as cfg
from feature_calculations.ts_to_features import participant_to_features
import pathes

if __name__ == "__main__":
    for i in cfg.participants_range:
        print(f'participant {i} to features')
        
        data = participant_to_features(i, setting=pathes.features_type)
        
        # sort columns
        header = data.iloc[:, :3]
        x = data.iloc[:, 3:]
        x = x.reindex(sorted(x.columns), axis=1)
        data = pd.concat((header, x), axis=1)
        
        
        data.to_csv(pathes.base_kin_feature_path+"participant"+str(i)+".csv", index=False)
        
