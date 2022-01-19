# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 20:08:36 2022

@author: skar
"""

#%%
# import packages

import pandas as pd
import numpy as np
import os

# Import user defined modules
code_path = 'C:\\Users\\skar\\repos\\EERE_decarb'
os.chdir(code_path)

import unit_conversions as ut
from eia_import_ import EIA_AEO

#%%


#%%
# Analysis parameters

fetch_data = True # True for fetching data, False for loading pre-compiled data

path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'

f_eia = 'EIA Dataset.csv'
f_corr_eia = 'corr_EIA_EERE.csv'
f_corr_ef_greet = 'corr_EF_GREET.csv'

save_interim_files = True

#%%
# Call data import functions

if fetch_data == False:
    eia_data = pd.read_csv(path_data + '\\' + f_eia)
else:
    eia_ob = EIA_AEO(save_to_file = False)
    eia_data = eia_ob.eia_multi_sector_import(sectors = ['Residential',
                                                         'Commercial',
                                                         'Electric Power'
                                                         ],
                                                  
                                                  aeo_cases = ['Reference case'
                                                               ]                                                  
                                                  )

corr_EIA_EERE = pd.read_csv(path_data + '\\' + f_corr_eia, header = 3)
corr_EF_GREET = pd.read_csv(path_data + '\\' + f_corr_ef_greet, header = 3)

#%%

#%%
# Merge data frames
activity = pd.merge(eia_data, corr_EIA_EERE, how='right', left_on=['Sector', 'Subsector'], right_on=['EIA: Sector', 'EIA: Subsector']).dropna().reset_index()
activity.rename(columns = {'Sector_y' : 'Sector',
                           'Subsector_y' : 'Subsector', 
                           'End use' : 'End Use Application',
                           'Energy Carrier' : 'Activity', 
                           'Date' : 'Year',                            
                           'Series Id' : 'EIA Series ID'}, inplace = True)
activity = activity [['AEO Case', 'Sector', 'Subsector', 'EIA: End Use Application', 'Activity', 'Activity Type', 'Activity Basis', 
                      'Year', 'Unit', 'Value', 'EIA Series ID']]

# unit conversion
activity['unit_to'] = 'MMBtu'
activity['unit_conv'] = activity['unit_to'] + '_per_' + activity['Unit']
activity['Value'] = np.where(
     [x in ut.unit1_per_unit2 for x in activity['unit_conv'] ],
     activity['Value'] * activity['unit_conv'].map(ut.unit1_per_unit2),
     activity['Value'] )
activity.drop(['unit_conv', 'Unit'], axis = 1, inplace = True)
activity.rename(columns = {'unit_to' : 'Unit'}, inplace = True)

if save_interim_files == True:
    activity.to_csv(path_data + '\\' + 'interim_Activity Matrix.csv')

#%%
