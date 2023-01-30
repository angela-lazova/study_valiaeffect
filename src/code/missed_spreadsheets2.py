# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:57:25 2022

@author: Angela Lazova
"""

import pandas as pd
import glob
import os


folder_path = "data_exp_59551-v19\data_exp_59551-v19_task-6bm9.csv"

big_file = pd.read_csv(folder_path)

key = "Participant Private ID"

key_list = big_file[key].unique()
key_list = key_list.astype(int)
key_list = key_list.tolist()
key_list.pop()

#%%
import os

for participant in key_list:
    current_path = 'creating_participant_folders\data_exp_59551-v18-{}\data_exp_59551-v19_task-6bm9-{}.csv'.format(participant,participant)
    current_folder = 'creating_participant_folders\data_exp_59551-v18-{}'.format(participant)
    
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
        
    current_participant = big_file[big_file[key] == participant]
    current_participant.to_csv(current_path)


#%%
column = "counterbalance-bkn3"

# Preparing variables for Lopp - to find all csv files that contain the our data
# and save it in a list - my_list
my_list = []

path = "participant_data\*\**.csv"
    
for fname in glob.glob(path):
   if "6bm9" in fname:
       current_file = pd.read_csv(fname)
       my_list.append(current_file.loc[1, column])

#%%

for index, trial in enumerate(my_list):
    prefix, num = trial.split("_")
    num = int(num)
    my_list[index] = num
    
   
my_list = sorted(my_list)

#%%

missing_elemnts = [item for item in range(my_list[0], my_list[-1]+1) if item not in my_list]
print(missing_elemnts)


#%%

#Reading the first spreadsheet so we can isolate and save the fixed (static)
# columns in a seperate DataFrame (section_one and section_three)

initial_data = pd.read_excel("xlsx_spreadsheets/spreadsheet_001.xlsx")


section_one = initial_data[['randomise_blocks', 
                            'randomise_trials',
                            'display', 
                            'Image']]

section_three = initial_data[['question', 
                              'blocktype', 
                              'tn', 
                              'qtype']]


# Now, to create the section_two - 128 columns: only missing spreadsheets

section_two = pd.DataFrame()

for num in missing_elemnts:
    #to get the spreadsheet number with 00 at front
    if len(str(num)) == 1:
        number = '00' + str(num)
    elif len(str(num)) == 2:
        number = '0' + str(num)
    else:
        number = str(num)
    #read the spreadsheet from 1 to 128 - missing values
    current_file = pd.read_excel("xlsx_spreadsheets/spreadsheet_{}.xlsx".format(number))
    #add the new column to section_two
    section_two['s_{}'.format(number)] = current_file['video']

# Let's combine the sections to make our master_spreadsheet and save it to excel

master_spreadsheet = pd.concat([section_one, section_two, section_three], axis=1,)
master_spreadsheet.to_excel('master_spreadsheet_MISSING_SHEETS.xlsx')
