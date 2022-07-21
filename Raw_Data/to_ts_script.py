import os
import Raw_Data.configurations as cfg
from Raw_Data.integration import raw_data_integration
from timeseries_data.Timeseries_Data import TimeseriesData
from Raw_Data.utils.utils import extract_subject_number
import pathes

if __name__ == "__main__":
    if not os.path.isdir(pathes.ts_data_path):
        os.mkdir(pathes.ts_data_path)
    idx_counter = 1
    log = ""
    for dir_name in os.listdir(pathes.raw_data_path):
        # checking if we are in a directory 
        path = os.path.join(pathes.raw_data_path, dir_name)
        if not os.path.isdir(path):
            continue
        
        # extract subject number
        subject_num = extract_subject_number(dir_name)
        print(subject_num)
        # get subject data
        ts_data = raw_data_integration(subject_num)
        
        # if there is no sufficient amount of data in specific subject the function above will return -1 
        if ts_data is -1:
            log += f"subject {subject_num} don't have enough trials\n"
            continue
        log += f"subject {subject_num} -> participant{idx_counter}\n"
        
        
        
        path = pathes.ts_data_path+"participant"+str(idx_counter)+".csv"
        ts_data.to_csv(path)
        idx_counter += 1
    
    # write log into file
    log_path = os.path.join(pathes.ts_data_path, "log.txt")
    f = open(log_path, "w")
    f.write(log)
    f.close()

