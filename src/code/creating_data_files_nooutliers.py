# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:01 2022

@author: Angela Lazova
"""
import pandas as pd
import numpy as np
from scipy import stats

#%%
#Improting the data file
video_data = pd.read_csv('data/PARTICIPANTS_DATA2.csv')
video_data = video_data.sort_values('video')


#Counting how many times each video is seen
#for the rows, delete all exept those where the value in column "qtype" is positive (randomly taking one question to prevent counting one video view twice)
views = video_data[video_data['qtype'].isin(['positive'])] #since each video view is written times 7 - onvce for each question, and we want to count it only as one view, we delete the other 6 times it is written
        

P = views[views['blocktype'].isin(['P'])]
P_views = P['video'].value_counts().rename_axis('videos').reset_index(name='counts')

N = views[views['blocktype'].isin(['N'])]
N_views = N['video'].value_counts().rename_axis('videos').reset_index(name='counts')

NU = views[views['blocktype'].isin(['NU'])]
NU_views = NU['video'].value_counts().rename_axis('videos').reset_index(name='counts')

H = views[views['blocktype'].isin(['H'])]
H_views = H['video'].value_counts().rename_axis('videos').reset_index(name='counts')

D = views[views['blocktype'].isin(['D'])]
D_views = D['video'].value_counts().rename_axis('videos').reset_index(name='counts')

list_of_views = [P_views, N_views, NU_views, H_views, D_views]
all_views = pd.concat(list_of_views)
all_views = all_views.sort_values('videos')
all_views.rename(columns={"videos": "video"}, inplace=True)
all_views.to_csv('all_views.csv')


# Specifying columns of interest
columns = [
    'video',
    'Response',
    'blocktype',
    'qtype'
    ]

complete_views_data = video_data[columns]
trying1 = complete_views_data.to_csv('plotting_videos.csv')

#%%
# Computing the mean and standard deviation for each video for all questions

video_means = complete_views_data.groupby(['video', 'qtype'])['Response'].mean().unstack()


video_means = video_means.rename(columns={"awake": "mean_awake", 
                                            "bored": "mean_bored",
                                            "disgust": "mean_disgust",
                                            "hunger": "mean_hunger",
                                            "like": "mean_like",
                                            "negative": "mean_negative",
                                            "positive": "mean_positive"})

# also calculating standard deviation
video_std = complete_views_data.groupby(['video', 'qtype'])['Response'].std().unstack()
video_std = video_std.rename(columns={"awake": "std_awake", 
                                        "bored": "std_bored",
                                        "disgust": "std_disgust",
                                        "hunger": "std_hunger",
                                        "like": "std_like",
                                        "negative": "std_negative",
                                        "positive": "std_positive"})

# concating the means and std into one data frame and saving it to a csv file
means_std_of_videos = pd.concat([video_means, video_std], axis=1)
means_std_of_videos = means_std_of_videos.round(2)


means_std_of_videos.to_csv('data/VIDEO_STD_MEANS.csv')

trying = video_means.to_csv('data/VIDEO_MEANS.csv')



#%%
## Computing mean and standard deviation separately for each question 
#so we can idendity outliers

## create a dictionary for each question
questions = ['positive','negative','hunger','disgust','awake','bored','like']

#specifying columns of interest
two_columns = ['video', 'Response']

# get unique video names, and preapre a dict so we can use them as keys.
video_names = video_data['video'].unique()

#preapre dictionaries for each question
questions_dict = {}

# create dataframe for only the awake question resposes
for question in questions:
    response_question = video_data[video_data['qtype'].isin([question])]
    response_question = response_question[two_columns]
    
    video_dict = {}
    
    for item in video_names:
        current_responses = response_question[response_question['video'].isin([item])]
        video_dict[item] = current_responses['Response'].values
        
    questions_dict[question] = video_dict

#awake_mean = video_data[video_data['qtype'].isin(['awake'])]

#remove unnecessary columns
#awake_mean = awake_mean[two_columns]

# go through all the responses and for each video, add reponses to a dict list with
# the video name as key.
#for item in video_names:
#    current_responses = awake_mean[awake_mean['video'].isin([item])]
#    video_dict[item] = current_responses['Response'].values

#%%
questions_dict_nooutliers = {}
questions_dict_mean_std_var = {}


#remove outliers
for question_key, video_dictionary in questions_dict.items():
    video_dict_nooutliers = {}
    video_dict_mean_std_var = {}
    for video_key, response_list in video_dictionary.items():
        new_response_list = response_list[(np.abs(stats.zscore(response_list)) < 3)]
        video_dict_nooutliers[video_key] = new_response_list
        
        #calulate mean, std, and var and save it to dict- for each video
        video_mean = np.mean(new_response_list)
        video_std = np.std(new_response_list)
        video_var = np.var(new_response_list)
        mean_std_var_list = [video_mean, video_std, video_var]
        
        video_dict_mean_std_var[video_key] = mean_std_var_list
        
    questions_dict_nooutliers[question_key] = video_dict_nooutliers
    questions_dict_mean_std_var[question_key] = video_dict_mean_std_var

#%%
#Create 7 dataframes and csvs for mean, std, and var of each video for each question
df_list = []

for question, videos_dictionary in questions_dict_mean_std_var.items():
    current_file = pd.DataFrame.from_dict(videos_dictionary, orient='index',
                                          columns=['{}_mean'.format(question), 
                                                   '{}_std'.format(question), 
                                                   '{}_var'.format(question)])
    
    
    current_file = current_file.round(2)
    df_list.append(current_file)
    current_file.to_csv("data/nooutliers/{}_mean_std_var.csv".format(question))

merged_file = pd.concat(df_list, axis=1)
merged_file.to_csv("data/nooutliers/full_mean_std_var.csv")

#%%

# Preparing csv files for plotting

# Creating dictionairies to loop through

categories = ['P','N','NU','H','D']
category_dict = {key:value for (key, value) in zip(range(len(categories)), categories)}

questions = ['positive','negative','hunger','disgust','awake','bored','like']
question_dict = {key:value for (key, value) in zip(range(len(questions)), questions)}

#Looping through dictionaires and creating files
for category_value in category_dict.values():
    temp_file = video_data[video_data['blocktype'].isin([category_value])]
    for question_value in question_dict.values():
        plotting_file = temp_file[temp_file['qtype'].isin([question_value])]
        plotting_file = pd.merge(plotting_file, all_views, on="video")
        plotting_file.to_csv('plotting_files/{}_{}_videos.csv'.format(category_value, question_value))
