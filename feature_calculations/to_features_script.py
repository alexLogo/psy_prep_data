import feature_calculations.configurations as cfg
from feature_calculations.ts_to_features import participant_to_features

if __name__ == "__main__":
    for i in cfg.subject_range:
        print(f'participant {i} to features')
        
        data = participant_to_features(i)
        
        data.to_csv(cfg.base_feature_path+"participant"+str(i)+".csv", index=False)
        
