import pandas as pd
import feature_calculations.configurations as cfg
from feature_calculations.read_features import read_features 
import pathes


def key(x):
    if x.startswith('10') or x.startswith('11'):
        return '@'+x
    return x

if __name__ == "__main__":
    for i in cfg.participants_range:
        print(f"sorting participant {i}")
        data = read_features(i, mode='base')
        header = data.iloc[:, :3]
        x = data.iloc[:, 3:]
        x = x.reindex(sorted(x.columns, key=key), axis=1)
        data  = pd.concat((header, x), axis=1)
        data.to_csv(pathes.base_feature_path+"participant"+str(i)+".csv", index=False)
        
        