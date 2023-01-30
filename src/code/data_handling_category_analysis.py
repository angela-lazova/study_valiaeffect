# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:47:32 2022

@author: Angela Lazova
"""
import pandas as pd

data_file = pd.read_csv("data/nooutliers/full_mean_std_var.csv")
data_file.rename(columns={'Unnamed: 0':'video'}, inplace=True)

data_file['category'] = 'fill'

my_list = data_file['video'].to_list()

for idx, item in enumerate(my_list):
    if 'P_' in item:
        data_file['category'][idx] = 'P'
    if 'N_' in item:
        data_file['category'][idx] = 'N'
    if 'NU_' in item:
        data_file['category'][idx] = 'NU'
    if 'H_' in item:
        data_file['category'][idx] = 'H'
    if 'D_' in item:
        data_file['category'][idx] = 'D'


#%%
means = data_file.groupby('category')[['positive_mean', 
                                       'negative_mean',
                                       'hunger_mean',
                                       'disgust_mean',
                                       'awake_mean',
                                       'bored_mean',
                                       'like_mean']].mean()

std = data_file.groupby('category')[['positive_std', 
                                        'negative_std',
                                        'hunger_std',
                                        'disgust_std',
                                        'awake_std',
                                        'bored_std',
                                        'like_std']].std()

category_analysis = pd.merge(means, std, on='category')
category_analysis = category_analysis.round(2)

category_analysis.to_csv('category_analysis2.csv')




