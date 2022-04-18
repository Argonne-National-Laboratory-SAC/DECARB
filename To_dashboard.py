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

# Read output data files

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository

interim_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\2_intermediate_files'
output_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'

f_activity = 'activity_ref_mtg_cases.xlsx'
f_env = 'env_ref_mtg_cases.xlsx'
f_eps_capacity
f_eps_net_gen
f_eps_env
f_eps_CI

activity
env
eps_capacity
eps_net_gen
eps_env
eps_CI

# Write results to excel file

app = xw.App()

wb = xw.Book(path + "\\" + f_age)

sheet_1 = wb.sheets['env matrix']
sheet_1['A5'].options(chunksize=5000).value = env_matrix

sheet_2 = wb.sheets['metadata']
sheet_2['A5'].options(chunksize=5000).value = df_metadata

sheet_3 = wb.sheets['energy cons']
sheet_3['A5'].options(chunksize=5000).value = df_energy_cons

wb.save()
wb.close()
app.quit()