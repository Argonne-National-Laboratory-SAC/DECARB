# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:42:37 2022

@author: skar
"""

#%%
# path, data files, and packages

import pandas as pd
import os

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository
path_env_mx = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\2_intermediate_files'
input_path_EIA = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files\\EIA'
input_path_GREET = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files\\GREET'
input_path_units = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files\\Units'
input_path_corr = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files\\correspondence_files'
output_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'

EIA_AEO_fetch_data = False
EIA_AEO_save_to_file = False
verbose = True

f_env_mx = 'interim_env_ref_mtg_cases.csv'
f_EIA = 'EIA Dataset.csv'
f_out_CI = 'CI_sectoral_ref_mtg.csv'

os.chdir(code_path_prefix)

from EIA_AEO_import import EIA_AEO
from unit_conversions import model_units 

# Unit conversion class object
ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)

# EIA data import and processing
ob_eia = EIA_AEO(input_path_EIA, input_path_corr)
ob_eia.EERE_data_flow_EIA_AEO(ob_units, EIA_AEO_fetch_data, EIA_AEO_save_to_file, verbose)

d_EIA = ob_eia.EIA_data['energy_demand']

del ob_eia

d_EIA = d_EIA[[#'Data Source', 
               #'AEO Case', 
               'Sector', 
               'Subsector', 
               'End Use Application',
               'Energy carrier', 
               'Energy carrier type', 
               'Basis', 
               'Year', 
               'Unit',
               'Value', 
               'Case', 
               'Generation Type', 
               #'Fuel Pool'
               ]]


d_env_mx = pd.read_csv(path_env_mx + '//' + f_env_mx)

d_env_mx = d_env_mx[[#'Unnamed: 0', 
                     #'Data Source', 
                     #'AEO Case',
                     'Case',
                     'Sector',
                     'Subsector',
                     'End Use Application',
                     'Scope',
                     'Energy carrier',
                     'Energy carrier type',
                     'Basis',
                     #'Fuel Pool',
                     'Year',
                     #'Flow Name',
                     #'Formula',
                     'Emissions Unit',
                     #'Unit',
                     #'Value',
                     #'CI',
                     #'Total Emissions',
                     #'Mitigation Case',
                     #'Emissions Type',
                     #'LCIA Method',
                     #'GWP',
                     #'timeframe_years',
                     'LCIA_estimate',
                     #'Generation Type',
                     #'Energy Unit',
                     #'GREET Version',
                     #'GREET Tab',
                     #'GREET Pathway',
                     #'Unit (Numerator)',
                     #'Unit (Denominator)',
                     #'GREET Default',
                     #'Zero Elec Comb',
                     #'Factor',
                     #'EF',
                     #'Assigned Sector',
                     #'Emissions Category, Detailed',
                     'Emissions Category, Aggregate']]

#%%
# Calculate sector classified emissions for reference case and mitigation case

d_env_mx_1 = d_env_mx.groupby(['Case',
                               'Sector',
                               'Year',
                               'Emissions Unit',]).agg({'LCIA_estimate' : 'sum'}).reset_index()

d_env_mx_1 = d_env_mx_1.pivot(index = ['Sector',
                                       'Year',
                                       'Emissions Unit'],
                              columns='Case',
                              values='LCIA_estimate').reset_index()

d_env_mx_1['Mitigation'] = d_env_mx_1['Reference case'] + d_env_mx_1['Mitigation']

d_env_mx_1.rename(columns={'Mitigation' : 'With Mitigations'}, inplace=True)

#%%
# Calculate sector classified energy demand as per EIA AEO reference case

d_EIA_1 = d_EIA.groupby(['Sector',
                         'Year',
                         'Unit']).agg({'Value' : 'sum'}).reset_index()
d_EIA_1.rename(columns={'Value' : 'Energy Demand',
                        'Unit' : 'Energy Unit'}, inplace=True)

#%%

# Merge and calculate carbon intensities for reference case and mitigation case

d_CI = pd.merge(d_EIA_1, d_env_mx_1, 
                how='left', on=['Sector', 'Year']).reset_index(drop=True)

d_CI['CI_Reference'] = d_CI['Reference case'] / d_CI['Energy Demand'] * 1000000 / 0.0010544 # mmmt to MT to g; mmbtu to btu to MJ
d_CI['CI_Mitigation'] = d_CI['With Mitigations'] / d_CI['Energy Demand'] * 1000000 / 0.0010544
d_CI = d_CI[['Sector', 'Year', 'Energy Unit', 'Emissions Unit', 'CI_Reference', 'CI_Mitigation']]
d_CI['Energy Unit'] = 'MJ'
d_CI['Emissions Unit'] = 'g'

d_CI.to_csv(output_path_prefix + '//' + f_out_CI)