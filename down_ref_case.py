# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:18:50 2022

@author: skar
"""

#%%

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository

input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
interim_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\2_intermediate_files'
output_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'

# Declaring paths for data loading
input_path_EIA = input_path_prefix + '\\EIA'
input_path_EPA = input_path_prefix + '\\EPA_GHGI'
input_path_corr = input_path_prefix + '\\correspondence_files'
input_path_aggriculture = input_path_prefix + '\\Agriculture'
input_path_industrial = input_path_prefix + '\\Industrial'
input_path_electricity = input_path_prefix + '\\Electricity'
input_path_GREET = input_path_prefix + '\\GREET'
input_path_units = input_path_prefix + '\\Units'
input_path_transport = input_path_prefix + '\\Transportation'
input_path_neu = input_path_prefix + '\\Non-Energy Use EFs'


#%%

# import packages
import pandas as pd
"""
import numpy as np
import os
from datetime import datetime

# Import user defined modules
os.chdir(code_path_prefix)

from EIA_AEO_import import EIA_AEO
from Industrial_import import Industrial
from Agriculture_import import Agriculture
from Transportation_VISION_import import Transport_Vision
from EPA_GHGI_import import EPA_GHGI_import
from NREL_electricity_import import NREL_elec
from GREET_EF_import import GREET_EF
from unit_conversions import model_units   """

#%%

activity_BAU = pd.read_csv(interim_path_prefix + '\\' + 'interim_activity_reference_case.csv')

activity_BAU = activity_BAU.loc[(activity_BAU['Year'] == 2020) &
                                        (activity_BAU['Scope'].isin(['Direct, Combustion', 'Direct, Non-Combustion']) ), :]

activity_BAU_elec = activity_BAU.loc[activity_BAU['Energy carrier type'].isin(['U.S. Average Mix', 'U.S. Average Grid Mix']), : ]

activity_BAU_non_elec = activity_BAU.loc[~activity_BAU['Energy carrier type'].isin(['U.S. Average Mix', 'U.S. Average Grid Mix']), : ]

activity_BAU_elec_agg = activity_BAU_elec.groupby(['Sector', 'Formula', 'Year', 'Unit']).\
                                          agg({'LCIA_estimate' : 'sum'}).reset_index()
activity_BAU_elec_agg['Type'] = 'Electric use activities'
                                          
activity_BAU_non_elec_agg = activity_BAU_non_elec.groupby(['Sector', 'Formula', 'Year', 'Unit']).\
                                          agg({'LCIA_estimate' : 'sum'}).reset_index()
activity_BAU_non_elec_agg['Type'] = 'Non-electric use activities'

activity_BAU_agg = pd.concat([activity_BAU_elec_agg, activity_BAU_non_elec_agg], axis=0).reset_index()

activity_BAU_agg.to_excel(interim_path_prefix + '\\' + 'interim_activity_reference_case_agg_2020.xlsx')

