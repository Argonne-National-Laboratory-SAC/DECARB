# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:45:33 2022

@author: Shannon Zhang, Saurajyoti Kar
"""

import pandas as pd
import numpy as np
from datetime import datetime

init_time = datetime.now()

input_path_dashboard = "C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Dashboard"
input_path_corr = "C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Data/Script_data_model/1_input_files/correspondence_files"

f_dashboard = "US Decarbonization Tool - test.xlsx"
f_output = "Env_Matrix_corr.xlsx"

f_dashboard_tab = "Env Matrix"

table_header = 3

env_matrix_df = pd.read_excel(input_path_dashboard + '/' + f_dashboard, sheet_name=f_dashboard_tab, header=table_header)

# merging functions
def simple_merge(file_path, df, matrix_merge_col, corr_filename, corr_merge_col, corr_header):
    corr_df = pd.read_csv(file_path + '/' + corr_filename, header=corr_header)
    df = df.merge(corr_df, how='left', left_on=matrix_merge_col, right_on=corr_merge_col)
    df = df.drop(corr_merge_col, axis=1)
    return df

# Sector merge requires there to be a column in the correspondence file
# where the Assigned Sector is identified, labeled "Assigned Sector". 
# Merge will only occur in the rows where the Assigned Sector and other 
# correspondence file conditions are met. 
# 
#   matrix_merge_col_1: column to merge on in Env Matrix
#   corr_filename: correspondence file name
#   corr_merge_col_1: column to merge on in correspondence file
#   corr_header: row where column headers are in correspondence file
#   other_bool: boolean to determine whether an other is included in the 
# correspondence file. If so, any additional values with the given 
# Assigned Sector that are not assigned a label are given the label 
# "Other + other_marker"
#   other_marker: optional input to add onto end of "Other" label
#   sector: input required if other_bool is True. Refers to Assigned
# Sector.
 
def sector_merge(file_path, df, matrix_merge_col_1, corr_filename, corr_merge_col_1, corr_header, other_bool, other_marker="", sector=""):
    matrix_merge_col_2 = "Assigned Sector"
    corr_merge_col_2 = "Assigned Sector"

    corr_df = pd.read_csv(file_path + '/' + corr_filename, header=corr_header)
    df = df.merge(corr_df, how='left', left_on=[matrix_merge_col_1, matrix_merge_col_2], right_on=[corr_merge_col_1, corr_merge_col_2])
    df = df.drop([corr_merge_col_1], axis=1)

    if other_bool: 
        conditions = [(df['Assigned Sector'] == sector) & (df[df.columns[-1]].isna())]
        choices = ['Other' + other_marker]
        df[df.columns[-1]] = np.select(conditions, choices, default = df[df.columns[-1]])
    return df


# Mitigation case correspondence files
env_matrix_df = simple_merge(input_path_corr, env_matrix_df, "Mitigation Case", "corr_output_mtg_agg_1.csv",\
    "Mitigation Case_Decarb", 3)
env_matrix_df = simple_merge(input_path_corr, env_matrix_df, "Mitigation Case", "corr_output_mtg_agg_2.csv",\
    "Mitigation Case_Decarb", 3)
env_matrix_df = simple_merge(input_path_corr, env_matrix_df, "Mitigation Case", "corr_output_mtg_agg_3.csv",\
    "Mitigation Case_Decarb", 3)

# Agriculture end use application 
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "End Use Application",\
     "corr_output_agr_enduse_agg_1.csv", "Agr End Use Application_Decarb", 3, False)

# Transportation end use application
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "End Use Application",\
     "corr_output_transp_enduse_agg_1.csv", "Transportation End-Use Application_Decarb",\
     3, True, '*', "Transportation")

# Industry / Agriculture subsector (supply chain)
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "Subsector", "corr_output_indagr_subsector_agg_1.csv",\
    "Ind/Agr Subsector_Decarb", 3, False)

conditions = [(env_matrix_df['Scope'] == "Supply Chain") & (env_matrix_df['Ind/Agr Subsector_Front'] != ''), 
    (env_matrix_df['Scope'] != "Supply Chain") & (env_matrix_df['Ind/Agr Subsector_Front'] != '')]
choices = ["Supply Chain", env_matrix_df['Ind/Agr Subsector_Front']]
env_matrix_df['Ind/Agr Subsector_Front_SC'] = np.select(conditions, choices, default = '')
env_matrix_df = env_matrix_df.drop(['Ind/Agr Subsector_Front'], axis=1)

# LULUCF end use application
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "End Use Application",\
     "corr_output_LULUCF_enduse_agg_1.csv", "LULUCF end use application_Decarb", 3, False)

# LULUCF end use application major agg
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "End Use Application",\
     "corr_output_LULUCF_enduse_agg_2.csv", "LULUCF end use application_Decarb", 3, True, "", "LULUCF")

# Industry mitigation case
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "Mitigation Case",\
     "corr_output_ind_mtg_agg_1.csv", "Industry Mitigation Case_Decarb", 3, False)

# Industry/Agriculture mitigation case
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "Mitigation Case",\
     "corr_output_indagr_mtg_agg_1.csv", "Ind/Ag Mitigation Case_Decarb", 3, False)

# Residential End use application
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "End Use Application",\
     "corr_output_res_enduse_agg_1.csv", "Res End Use Application_Decarb", 3, False)

# Residential Subsector
env_matrix_df = sector_merge(input_path_corr, env_matrix_df, "Subsector",\
     "corr_output_res_subsector_agg_1.csv", "Res Subsector_Decarb", 3, False)

# Including energy matrix in spreadsheet
energy_matrix = pd.read_excel(input_path_dashboard + '/' + f_dashboard, sheet_name="Energy Demand", header=table_header)

writer = pd.ExcelWriter(input_path_dashboard + '/' + f_output)
env_matrix_df.to_excel(writer, sheet_name=f_dashboard_tab, index=False)
energy_matrix.to_excel(writer, sheet_name = "Energy Demand", index=False)
writer.save()
writer.close()

print( '    Elapsed time: ' + str(datetime.now() - init_time)) 