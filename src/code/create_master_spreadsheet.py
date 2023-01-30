# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 09:56:02 2022

@author: Angela Lazova
"""
# Importing packages
import pandas as pd


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


# Now, to create the section_two (300 video columns) we loop through the 300s.

section_two = pd.DataFrame()
my_list = [*range(1,301)]
for num in my_list:
    #to get the spreadsheet number with 00 at front
    if len(str(num)) == 1:
        number = '00' + str(num)
    elif len(str(num)) == 2:
        number = '0' + str(num)
    else:
        number = str(num)
    #read the spreadsheet from 1 to 300
    current_file = pd.read_excel("xlsx_spreadsheets/spreadsheet_{}.xlsx".format(number))
    #add the new column to section_two
    section_two['s_{}'.format(number)] = current_file['video']

# Let's combine the sections to make our master_spreadsheet and save it to excel

master_spreadsheet = pd.concat([section_one, section_two, section_three], axis=1,)
master_spreadsheet.to_excel('master_spreadsheet.xlsx')