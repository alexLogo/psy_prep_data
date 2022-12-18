import math
import pandas as pd
import numpy as np
from Raw_Data.tracker_data.read_trackers import read_tracker


def create_mult_matrix(euler_x, euler_y, euler_z):      
    teta_x = math.radians(euler_x)
    teta_y = math.radians(euler_y)
    teta_z = math.radians(euler_z)
    
    rotation_mat_x = np.array([[1,0,0],[0,math.cos(teta_x),-(math.sin(teta_x))],[0,math.sin(teta_x),math.cos(teta_x)]])
    rotation_mat_y = np.array([[math.cos(teta_y),0,math.sin(teta_y)],[0,1,0],[-(math.sin(teta_y)),0,math.cos(teta_y)]])
    rotation_mat_z = np.array([[math.cos(teta_z),-(math.sin(teta_z)),0],[math.sin(teta_z),math.cos(teta_z),0],[0,0,1]])

    
    rotation_mat = np.matmul(np.matmul(rotation_mat_z,rotation_mat_x), rotation_mat_y)
    return rotation_mat

def frame_to_numpy(frame):
    frame = np.array(frame)
    frame[0] *= -1
    
    return frame


def unity_transformation(frame):
    mult_matrix = create_mult_matrix(frame['Headset_euler_x'], frame['Headset_euler_y'], frame['Headset_euler_z'])
    unity_right = np.matmul(mult_matrix, frame_to_numpy(frame[['right_gaze_x', 'right_gaze_y', 'right_gaze_z']]))
    unity_left = np.matmul(mult_matrix, frame_to_numpy(frame[['left_gaze_x', 'left_gaze_y', 'left_gaze_z']]))
    
    unity_frame = pd.Series(np.concatenate([unity_right,unity_left]), 
                            index = ['u_right_gaze_x', 'u_right_gaze_y', 'u_right_gaze_z',
                                     'u_left_gaze_x', 'u_left_gaze_y', 'u_left_gaze_z'])
    
    return unity_frame 


def global_gaze(unity_gaze, global_headset, relevant_depth=-1):
    # calculating the distance from the eye to the depth of the chosen plain (auto=-1)
    distance_to_relevant_depth = abs(global_headset[2] - relevant_depth)
    if unity_gaze[2] == 0:
        print("0")
    # calculate vector coefficient to the chosen plain 
    t = np.array(distance_to_relevant_depth/unity_gaze[2])
    
    # calculate the point on this plain
    new_x = global_headset[0] + t * unity_gaze[0]
    new_y = global_headset[1] + t * unity_gaze[1]
    # new_z = global_headset[2] + t * unity_gaze[2] # suppose to be {relevant_depth} 
    
    point_on_plain = np.array([new_x, new_y])
    return point_on_plain



def gaze_transformation(frame):
    unity_right = frame[['u_right_gaze_x', 'u_right_gaze_y', 'u_right_gaze_z']]
    unity_left = frame[['u_left_gaze_x', 'u_left_gaze_y', 'u_left_gaze_z']]
    global_headset = frame[['Headset_global_x', 'Headset_global_y', 'Headset_global_z']]
    
    global_right_gaze = global_gaze(unity_right, global_headset)
    global_left_gaze = global_gaze(unity_left, global_headset)
    
    global_gaze_frame = pd.Series(np.concatenate([global_right_gaze,global_left_gaze]), 
                            index = ['right_gaze_x', 'right_gaze_y',
                                     'left_gaze_x', 'left_gaze_y'])
    
    return global_gaze_frame
    

def extract_gaze(df):
    unity_direction = df.apply(unity_transformation, axis=1)
    new_unity_df = pd.concat((df.loc[:, ['Headset_global_x', 'Headset_global_y', 'Headset_global_z']], unity_direction), axis=1)
    real_normalized_gaze = new_unity_df.apply(gaze_transformation, axis=1)
    
    new_df = pd.concat((df.loc[:, ['timestamp']], real_normalized_gaze), axis=1)
    
    return new_df

def gaze_calculation(data):
    for i,(_, df) in enumerate(data): 
        data[i] = (data[i][0], extract_gaze(df))
        
    return data


def no_zero_frame_filter(data):
    for i in range(len(data)):
        data[i] = (data[i][0], data[i][1][data[i][1].isnull().sum(axis=1) == 0])

    return data

