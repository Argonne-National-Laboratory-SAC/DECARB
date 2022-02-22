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

from EIA_AEO_import import EIA_AEO
from Industrial_import import Industrial
from Agriculture_import import Agriculture
from Transportation_VISION_import import Transport_Vision
from EPA_GHGI_import import EPA_GHGI_import
from NREL_electricity_import import NREL_elec
from GREET_EF_import import GREET_EF
from unit_conversions import model_units   

#%%


#%%
# Analysis parameters

fetch_data = False # True for fetching data, False for loading pre-compiled data
save_interim_files = True

# Please 
#data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data'
data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model'

f_eia = 'EIA Dataset.csv'
f_NREL_elec_option = 'report - All Options EFS.xlsx'
f_ef = 'GREET_EF_EERE.csv'
f_corr_eia = 'corr_EIA_EERE.csv'
f_corr_ef_greet = 'corr_EF_GREET.csv'
f_corr_fuel_pool = 'corr_fuel_pool.csv'
f_corr_elec_gen = 'corr_elec_gen.csv'

#%%
# Create data class objects

# Unit conversion class object
ob_units = model_units(data_path_prefix)

# EIA data import
if fetch_data == False:
    eia_data = pd.read_csv(data_path_prefix + '\\' + f_eia)
else:
    eia_ob = EIA_AEO(save_interim_files, data_path_prefix)
    eia_data = eia_ob.eia_multi_sector_import(sectors = ['Residential',
                                                         'Commercial',
                                                         'Electric Power'
                                                         ],
                                                  
                                                  aeo_cases = ['Reference case'
                                                               ]                                                  
                                                  )

# Industrial data import
ob_industry = Industrial(ob_units, data_path_prefix)

# Agricultural and LULUCF data import
ob_agriculture = Agriculture(data_path_prefix)

# Transportation (VISION) data import
ob_transport = Transport_Vision(data_path_prefix)

# EPA GHGI data import
ob_EPA_GHGI = EPA_GHGI_import(ob_units, data_path_prefix)

# NREL Electricity generation data import
ob_elec = NREL_elec(f_NREL_elec_option, data_path_prefix)

# GREET emission factor load
ob_ef = GREET_EF(f_ef, data_path_prefix)

# Data tables for correspondence across data sets

corr_EIA_EERE = pd.read_csv(data_path_prefix + '\\' + f_corr_eia, header = 3)
corr_EF_GREET = pd.read_csv(data_path_prefix + '\\' + f_corr_ef_greet, header = 3)
corr_fuel_pool = pd.read_csv(data_path_prefix + '\\' + f_corr_fuel_pool, header = 3)
corr_elec_gen = pd.read_csv(data_path_prefix + '\\' + f_corr_elec_gen, header = 3)

#%%

#%%
# Merge EIA and EPA's correspondence matrix
activity = pd.merge(eia_data, corr_EIA_EERE, how='right', left_on=['Sector', 'Subsector'], right_on=['EIA: Sector', 'EIA: Subsector']).dropna().reset_index()
activity.rename(columns = {'Sector_y' : 'Sector',
                           'Subsector_y' : 'Subsector', 
                           'End use' : 'End Use Application',
                           'Energy Carrier' : 'Activity', 
                           'Date' : 'Year',                            
                           'Series Id' : 'EIA Series ID'}, inplace = True)
activity = activity [['AEO Case', 'Sector', 'Subsector', 'EIA: End Use Application', 'Activity', 'Activity Type', 'Activity Basis', 
                      'Year', 'Unit', 'Value']]

# unit conversion
activity['unit_to'] = [ob_units.select_units(x) for x in activity['Unit'] ]
activity['unit_conv'] = activity['unit_to'] + '_per_' + activity['Unit'] 
activity['Value'] = np.where(
     [x in ob_units.dict_units for x in activity['unit_conv'] ],
     activity['Value'] * activity['unit_conv'].map(ob_units.dict_units),
     activity['Value'] )
activity.drop(['unit_conv', 'Unit'], axis = 1, inplace = True)
activity.rename(columns = {'unit_to' : 'Unit'}, inplace = True)

# Merge fuel pool
activity = pd.merge(activity, corr_fuel_pool, how='left', left_on=['Activity'], right_on=['Energy Carrier']).dropna().reset_index()

# Extract electricity generation data from activity data frame
elec_gen = activity.loc[(activity['Sector'] == 'Electric Power') ].dropna().\
    drop(['level_0', 'index', 'EIA: End Use Application', ], axis = 1).reset_index()

# Merge Elec. CI data with LCI EF data table to calculate electricity dependency based CI

# Merge the EF data table with the activity data table

# Merge with EPA data
# env_mx = pd.merge(ob_EPA_GHGI.df_ghgi, activity, how='right', left_on=['Year', 'Sector', 'Subsector'], right_on=['EIA: Sector', 'EIA: Subsector']).dropna().reset_index()

if save_interim_files == True:
    activity.to_csv(path_data + '\\' + 'interim_Activity Matrix.csv')

#%%
