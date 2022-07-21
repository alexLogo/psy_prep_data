import numpy as np
import pandas as pd
from copy import deepcopy
import timeseries_data.util as util

# temp
import Raw_Data.configurations as cfg

 
class TimeseriesData():
    
    def __init__(self, data=0, header_size=0, num_of_ts=0, ts_names=0):
        # sometimes we will want to call the constructor without doing anything in order to read data from file
        if data is 0:
            return
        self.data = np.array(data)
        self.header_size = header_size
        self.num_of_ts = num_of_ts
        self.ts_names = ts_names
        self.ts_length = (self.data.shape[1] - self.header_size) // self.num_of_ts
        
        
    def read_from_csv(self, path):
        df = pd.read_csv(path)
        
        metastring = df.columns[0]
        self.data = np.array(df)
        self.header_size, self.num_of_ts, self.ts_names = util.extract_meta_string(metastring)
        self.ts_length = (self.data.shape[1] - self.header_size) // self.num_of_ts
        
        
    def to_csv(self, path):
        # create meta data string
        metastring = util.create_meta_string(self.header_size, self.num_of_ts, self.ts_names)
        
        # cast the data into dataframe
        data = pd.DataFrame(self.data)
        
        # insert metadata into column 0
        col_name = data.columns.to_list()[0]
        data.rename(columns={col_name:metastring}, inplace=True)
        #write to disk
        data.to_csv(path, index=None)
        
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def get_header(self, idx):
        return self.data[idx, :self.header_size]
    
    def get_all_header(self):
        return self.data[:, :self.header_size]

    
    def get_data(self, idx):
        return self.data[idx, self.header_size:]
    
    def get_all_ts(self, idx, include_timestamp=False):
        data_lst = []
        for name in self.ts_names:
            if (not include_timestamp) and name == 'timestamp':
                continue
            data_lst.append(self.get_ts(idx, name))
        ts_data = np.array(data_lst)
        return ts_data
    
    def get_ts_range(self, idx, ts_range):
        data_lst = []
        for ts in ts_range:
            ts += 1
            data_lst.append(self.get_ts(idx, ts ))
        ts_data = np.array(data_lst)
        return ts_data
    
    def get_ts(self, row_idx, ts_idx):
        if isinstance(ts_idx, str):
            ts_idx = self.ts_names.index(ts_idx)
        begining_idx = self.header_size + (ts_idx*self.ts_length)
        ts = self.data[row_idx, begining_idx:begining_idx+self.ts_length]
        ts = util.zero_strip(ts)
        return ts
    
    def create_new_ts(self, old_names_list, new_name, fun):
        # get old name index
        old_idx = [self.ts_names.index(old_name) for old_name in old_names_list]
        
        # define new ts data container
        new_data = np.zeros((len(self.data), self.ts_length))
        
        # iterate over the data
        for i in range(len(self.data)):
            # get original ts
            ts_list = [self.get_ts(i, idx) for idx in old_idx]
            # calculate new ts
            new_ts = fun(ts_list)
            
            if len(new_ts) != len(ts_list[0]):
                print()
            
            # pad new ts
            new_ts = np.pad(new_ts, (0, self.ts_length-len(new_ts)), constant_values=cfg.padding_value)
            # insert to new data
            new_data[i] = new_ts
            
        # add new ts to data array
        self.data = np.concatenate((self.data, new_data), axis=1)
        
        self.ts_names.append(new_name)
        
        self.num_of_ts += 1
        
        
    def split_data(self, idx):
        new_ts_list = []
        uniques = np.unique(self.data[:,idx])
        
        for label in uniques:
            new_ts = deepcopy(self)
            new_ts.data = self.data[self.data[:,idx]==label]
            new_ts_list.append(new_ts)
            
        return new_ts_list
        


