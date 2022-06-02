import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import seaborn as sns

from feature_calculations.read_features import read_features

data = read_features(1, mode='clean')
#names = ['len', 'vel_reach', 'acc_reach', 'vel_back', 'acc_back']
x = data.iloc[:, 3:]
#x.set_axis(names, axis=1, inplace=True)
y = data.iloc[:, 1] > 0
corr = np.corrcoef(x.T)


def feature_drop(data):
    vif = create_vif(data)
    idx = vif['vif'].idxmax()
    label = vif['features'].iat[idx]
    data.drop(label, axis=1, inplace=True)

def create_vif(data):
    vif = pd.DataFrame()
    vif['features'] = data.columns
    vif['vif'] = [variance_inflation_factor(data.to_numpy(), i) for i in range(len(data.columns))]
    print(vif)
    return vif


def heat(corr_data):
    corr = np.corrcoef(corr_data.T)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    names = corr_data.columns
    # adjust mask and df
    mask = mask[1:, :-1]
    corr = corr[1:,:-1]
    
    fig, ax = plt.subplots(figsize=(8,7))
    sns.heatmap(corr, mask=mask, cmap="coolwarm", annot=True, fmt=".2f",
                vmin=-1, vmax=1, square=True, linewidth=2, cbar_kws={"shrink": .8})
    ax.set_title("correlations", fontsize=20, pad=20)
    x = [names[i] for i in range(len(names)-1)]
    plt.xticks(np.arange(len(names)-1) + .5, labels=names[:-1], rotation=85)
    plt.yticks(np.arange(len(names)-1) + .5, labels=names[1:], rotation=0)
    #plt.xticks(rotation=70)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.grid(False)
