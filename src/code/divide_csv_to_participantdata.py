# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:57:25 2022

@author: Angela Lazova
"""

import pandas as pd
import glob
import os


folder_path = "final_participants\data_exp_59551-v19_task-6bm9.csv"

big_file = pd.read_csv(folder_path)

key = "Participant Private ID"

key_list = big_file[key].unique()
key_list = key_list.astype(int)
key_list = key_list.tolist()
key_list.pop()

#%%

for participant in key_list:
    current_path = 'creating_participant_folders\data_exp_59551-v19-{}\data_exp_59551-v19_task-6bm9-{}.csv'.format(participant,participant)
    current_folder = 'creating_participant_folders\data_exp_59551-v19-{}'.format(participant)
    
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
        
    current_participant = big_file[big_file[key] == participant]
    current_participant.to_csv(current_path)