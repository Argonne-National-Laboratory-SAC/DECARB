# -*- coding: utf-8 -*-

"""
Created on Monday Apr 18 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 04/18/2022

Summary: This python script writes the output data to the Excel Dashboard 

"""

#%%

import pandas as pd
import xlwings as xw

# Set file paths, file names and read output data files

print("Status: Writing data files to Dashboard ..")

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository

interim_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\2_intermediate_files'
output_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'

dashboard_path = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Dashboard'

f_activity = 'activity_ref_mtg_cases.csv'
f_env = 'env_ref_mtg_cases.csv' 
f_elec_net_gen = 'interim_elec_gen.csv'
f_elec_env = 'interim_elec_gen_env.csv'
f_elec_CI = 'interim_elec_gen_CI.csv'

f_dashboard = 'US Decarbonization Tool_04_20 - Copy.xlsx'

activity =  pd.read_csv(output_path_prefix + '\\' + f_activity, index_col=0)    
env = pd.read_csv(output_path_prefix + '\\' + f_env, index_col=0)
elec_net_gen = pd.read_csv(interim_path_prefix + '\\' + f_elec_net_gen, index_col=0)
elec_env = pd.read_csv(interim_path_prefix + '\\' + f_elec_env, index_col=0)
elec_CI = pd.read_csv(interim_path_prefix + '\\' + f_elec_CI, index_col=0)

#%%

# Write results to excel file

app = xw.App()

wb = xw.Book(dashboard_path + "\\" + f_dashboard)

# Write to the Activity Matrix tab
sheet_1 = wb.sheets['Energy Demand']
sheet_1['A4'].options(chunksize=5000).value = activity

# Write to the Environmental Matrix tab
sheet_1 = wb.sheets['Env Matrix']
sheet_1['A4'].options(chunksize=5000).value = env

sheet_1 = wb.sheets['EPS - Net Gen']
sheet_1['A4'].options(chunksize=5000).value = elec_net_gen

sheet_1 = wb.sheets['EPS - Env']
sheet_1['A4'].options(chunksize=5000).value = elec_env

sheet_1 = wb.sheets['EPS - CI']
sheet_1['A4'].options(chunksize=5000).value = elec_CI

"""
sheet_2 = wb.sheets['metadata']
sheet_2['A5'].options(chunksize=5000).value = df_metadata

sheet_3 = wb.sheets['energy cons']
sheet_3['A5'].options(chunksize=5000).value = df_energy_cons
"""

wb.save()
wb.close()
app.quit()

print("Status: Writing to Dashboard completed!")

#%%