import feature_calculations.configurations as cfg
from feature_calculations.ts_to_features import participant_to_features
import pathes

if __name__ == "__main__":
    for i in cfg.participants_range:
        print(f'participant {i} to features')
        
        data = participant_to_features(i)
        
        data.to_csv(pathes.base_feature_path+"participant"+str(i)+".csv", index=False)
        
