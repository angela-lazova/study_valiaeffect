# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:31:35 2022

@author: Angela Lazova
"""
import pandas as pd



#Improting the data files
video_data = pd.read_csv('data/PARTICIPANTS_DATA2.csv')
questionaire_data = pd.read_csv("Rscripted_files_questionaires/scoresFEE_os.csv")

#Rename Participant Private ID to just Participant because of Pandas protected keywords
video_data.rename(columns = {'Participant Private ID':'Participant'}, inplace = True)
questionaire_data.rename(columns = {'ID':'Participant'}, inplace = True)

#Specifying the columns that are important for analysis
columns = ['Participant',
           'Response',
           'blocktype',
           'qtype']

#Cleaning the table: taking only the rows and columns of interest
d_videos = video_data[video_data['blocktype'].isin(['D'])] #only disgusting videos
d_videos = d_videos[columns] #only the columns of interest

#%%

#create a csv file with all the raw data from the FEE questionaire with mean and summed score 
#with participants responses on the D videos.
dv_dq = d_videos[d_videos['qtype'].isin(['disgust'])] #only for the disgusting question

fee_data = pd.merge(dv_dq, questionaire_data, on='Participant')
fee_data.to_csv('fee_regression_file.csv')


#%%

# find the mean value of each participant for the D videos
participant_mean = d_videos.groupby(['Participant', 'qtype'])['Response'].mean().unstack()
participant_mean.reset_index(inplace=True)
participant_mean = participant_mean.rename(columns = {'index':'Participant'})


participant_mean = participant_mean[['Participant', 'disgust']]
questionaire_data.to_csv('trying.csv')

#Merging the two files: questionnaire score and disgust video mean responses
fee_Dmean = pd.merge(participant_mean, questionaire_data, on='Participant')

fee_Dmean.to_csv('temp.csv')

#%%

import numpy as np
import scipy.stats


x_list = fee_Dmean[['disgust']].values.flatten()
y_list = fee_Dmean[['feeTod']].values.flatten()

result = np.corrcoef(x_list, y_list)
print(result)

r = scipy.stats.pearsonr(x_list, y_list)
print(r)