import Raw_Data.configurations as cfg
# this function gets groupby object
# and return a list of tuples (trial_num, trial_dataframe)
def convert_groupby_to_list(df_group):
    df_list = []
    for name, df in df_group:
        df.drop(cfg.tracker_idx_col, axis=1,inplace=True)
        df_list.append((name,df))
    return df_list
