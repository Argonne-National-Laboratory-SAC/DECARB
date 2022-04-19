# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 20:08:36 2022

@author: skar
"""

#%%
# Analysis parameters

# Update the _prefix paths based on your local Box folder location

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository

input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
interim_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\2_intermediate_files'
output_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'

# Declaring paths for data loading
input_path_EIA = input_path_prefix + '\\EIA'
input_path_EPA = input_path_prefix + '\\EPA_GHGI'
input_path_SCOUT = input_path_prefix + '\\Buildings\\SCOUT'
input_path_corr = input_path_prefix + '\\correspondence_files'
input_path_aggriculture = input_path_prefix + '\\Agriculture'
input_path_industrial = input_path_prefix + '\\Industrial'
input_path_electricity = input_path_prefix + '\\Electricity'
input_path_GREET = input_path_prefix + '\\GREET'
input_path_units = input_path_prefix + '\\Units'
input_path_VISION = input_path_prefix + '\\Transportation'
input_path_neu = input_path_prefix + '\\Non-Energy Use EFs'

# LCIA factors
f_lcia = 'gwp factors.xlsx'
f_lcia_sheet = 'Tidy'

# Non energy use EFs file name
f_neu = 'neu_efs.xlsx'
sheet_neu = 'Sheet1'

# Declaring correlation filenames
f_eia = 'EIA Dataset.csv'
f_NREL_elec_option = 'report - All Options EFS.xlsx'
f_corr_ef_greet = 'corr_EF_GREET.xlsx'

sheet_corr_ef_greet = 'corr_EF_GREET'

f_corr_EIA_SCOUT = 'corr_EERE_SCOUT.xlsx'
sheet_corr_EIA_SCOUT = 'Mapping EIA_to_Scout'

# defining the intermediate and final data table files and their columns
f_interim_activity = 'interim_activity_ref_mtg_cases.csv'
f_interim_env = 'interim_env_ref_mtg_cases.csv'
f_out_activity = 'activity_ref_mtg_cases.csv'
f_out_env = 'env_ref_mtg_cases.csv'
f_elec_net_gen = 'interim_elec_gen.csv'
f_elec_env = 'interim_elec_gen_env.csv'
f_elec_env_agg = 'interim_elec_gen_env_agg.csv'
f_elec_CI = 'interim_elec_gen_CI.csv'

cols_activity_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Unit', 'Value']

cols_env_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Scope', 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Formula', 'Emissions Unit', 'Total Emissions', 'LCIA_estimate']

cols_elec_net_gen = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                     'Energy carrier', 'Unit', 'Electricity Production']

cols_elec_env = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool', 'Generation Type',
                 'Scope', 'Formula', 'Year', 'EF_Unit (Numerator)', 'Total Emissions']

cols_elec_env_agg = ['Case', 'Mitigation Case', 'Sector',
                     'Energy carrier', 'Formula', 
                     'Year', 'EF_Unit (Numerator)', 'Total Emissions']

cols_elec_CI = ['Case', 'Mitigation Case', 'Sector',
                'Energy carrier', 'Formula', 
                'Year', 'Emissions Unit', 'Energy Unit', 'CI']

model_col_list = ['Data Source', 'AEO Case', 'Case', 'Mitigation Case', 'Sector', 'Subsector', 
                  'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                  'Basis', 'Fuel Pool', 'Year', 'Formula', 'Emissions Unit', 
                  'Unit', 'Value', 'CI', 'Total Emissions']

# Decarbonization years of analysis
decarb_year_min = 2020
decarb_year_max = 2050

# Model data pull and intermediate file saving options
EIA_AEO_fetch_data = False # True for fetching EIA AEO data, False for loading pre-compiled data
EIA_AEO_save_to_file = True # True for saving fetched data and saving it to file
save_interim_files = True

# GWP assumptions
# Note: Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI.
LCIA_Method = 'AR4' # QA can use AR4, but model should be based on AR5
lcia_timeframe = 100

# EIA AEO data cases
EIA_AEO_case_option = ['Reference case']

# T&D assumption, constant or calculated
#T_and_D_loss_constant = True
# T_and_D_loss = 0.06

# parameter to print out additional information when code is running
verbose = True

#%%


#%%

# import packages
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Import user defined modules
os.chdir(code_path_prefix)

from EIA_AEO_import import EIA_AEO
from SCOUT_import import SCOUT
#from Industrial_import import Industrial
#from Agriculture_import import Agriculture
from VISION_import import VISION
from EPA_GHGI_import import EPA_GHGI_import
from NREL_electricity_import import NREL_elec
from GREET_EF_import import GREET_EF
from unit_conversions import model_units   

#%%

init_time = datetime.now()

# Create data class objects

# Unit conversion class object
ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)

# EIA data import and processing
ob_eia = EIA_AEO(input_path_EIA, input_path_corr)
ob_eia.EERE_data_flow_EIA_AEO(ob_units, EIA_AEO_fetch_data, EIA_AEO_save_to_file, verbose)

ob_EPA_GHGI = EPA_GHGI_import(ob_units, input_path_EPA, input_path_corr )

ob_EPA_GHGI.remove_combustion_other_em() # removing 'combustion' and 'other' category emissions

ob_EPA_GHGI.process_EERE(decarb_year_min, decarb_year_max) # perform calculations for the decarbonization tool

if save_interim_files:
    ob_EPA_GHGI.activity_non_combust_exp.to_csv(interim_path_prefix + '//' + 'interim_ob_EPA_GHGI.csv')

# NREL Electricity generation data import
ob_elec = NREL_elec( ob_units, input_path_electricity, input_path_corr )

# VISION Transportation data import
ob_VISION = VISION(input_path_VISION, input_path_corr)

# GREET emission factor load
ob_ef = GREET_EF(input_path_GREET )
                      
# Data tables for correspondence across data sets
corr_EF_GREET = pd.read_excel(input_path_corr + '\\' + f_corr_ef_greet, sheet_name = sheet_corr_ef_greet, header = 3)
corr_EIA_SCOUT = pd.read_excel(input_path_corr + '\\' + f_corr_EIA_SCOUT, sheet_name = sheet_corr_EIA_SCOUT, header = 3, index_col=None)

# Life Cycle Impact Assessment metrics table
lcia_data = pd.read_excel(input_path_EPA + '\\' + f_lcia, sheet_name = f_lcia_sheet)         
lcia_select = lcia_data.loc[ (lcia_data['LCIA Method'] == LCIA_Method) & (lcia_data['timeframe_years'] == lcia_timeframe) ]

# Loading Non-energy use EFs
neu_EF_GREET = pd.read_excel(input_path_neu + '\\' + f_neu, sheet_name = sheet_neu, header = 3)

#%%

#%%

# Hydrogen Economy: Track ng use as a feedstock for hydrogen in a separate df. Steam methane reform ef from thet data frame

print('Status: Constructing Electric generation activity and Emission Factors data frames ..')
 
"""
Steps for constructing electric generation activity and emissions:   
1. Pre-process emissions factor data
2. Aggregrate and calculate net generation and/or emissions in separate dfs/file. Consider T&D loss for electricity generation.
3. Merge two dfs and calculate direct-combustion electric generation CI
"""

# Map with correlation matrix to GREET pathway names
ob_ef.ef_raw = ob_ef.ef.copy()
ob_ef.ef = pd.merge(corr_EF_GREET.loc[:, ~ corr_EF_GREET.columns.isin(['GREET Tab', 'GREET Version'])],
                    ob_ef.ef,
                    how='left',on=['GREET Pathway', 'Scope']).reset_index(drop=True)

# Filter combustion data for electricity generation 
ob_ef.ef_electric = ob_ef.ef.loc[ob_ef.ef['Scope'].isin(['Electricity, Combustion'])].copy()

ob_ef.ef_electric.rename(columns = {'Unit (Numerator)' : 'EF_Unit (Numerator)',
                                    'Unit (Denominator)' : 'EF_Unit (Denominator)'}, inplace = True)                

# Calculate aggregrated electricity generation and merge T&D loss
# Merge T&D loss data
electric_gen = ob_eia.EIA_data['energy_supply'].groupby(['Year', 'Sector', 'End Use', 'Energy carrier', 'Unit']).\
                                                agg({'Value' : 'sum'}).reset_index().\
                                                rename(columns = {'Value' : 'Electricity Production'})

electric_gen = pd.merge(electric_gen, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
electric_gen['Electricity Production'] = electric_gen['Electricity Production'] * (1 - electric_gen['loss_frac'])
electric_gen.rename(columns={'End Use' : 'End Use Application'}, inplace=True)

electric_gen['Case'] = 'Reference Case'
electric_gen[['Mitigation Case', 'Subsector']] = '-'
if save_interim_files == True:
    electric_gen[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)

# Merge emission factors for fuel-feedstock combustion used for electricity generation with net electricity generation
electric_gen_ef = pd.merge(ob_eia.EIA_data['energy_supply'][['AEO Case', 'End Use', 'Sector', 'Subsector', 'Energy carrier', 
                                     'Energy carrier type', 'Basis', 'Year', 'Unit', 'Value',
                                     'Fuel Pool', 'Generation Type', 'Case' ]],
                           ob_ef.ef_electric, 
             how='left',
             on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 'Year', 'Case'])

# Calculate net emission by GHG species, from electricity generation    
electric_gen_ef['Total Emissions'] = electric_gen_ef['Reference case'] * electric_gen_ef['Value'] 

# Rename and re-arrange columns
electric_gen_ef = electric_gen_ef.rename(columns={
                                                  'Reference case' : 'EF_withElec',
                                                  'Elec0' : 'EF_Elec0',
                                                  'Unit' : 'Energy Unit',
                                                  'Value' : 'Electricity Production'
                                        })
electric_gen_ef = electric_gen_ef[['AEO Case', 'Case', 'GREET Pathway', 'Sector', 'Subsector', 'End Use Application', 
                          'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool', 'Generation Type',
                          'Year', 'Energy Unit', 'Electricity Production', 'Scope', 'Flow Name', 'Formula', 
                          'EF_Unit (Numerator)', 'EF_Unit (Denominator)', 
                          'EF_withElec', 'Total Emissions']]

electric_gen_ef['Mitigation Case'] = '-'
if save_interim_files == True:
    electric_gen_ef[cols_elec_env].to_csv(interim_path_prefix + '\\' + f_elec_env)

# Aggregrate emissions
electric_gen_ef_agg = electric_gen_ef.groupby(['Year', 'Sector', 'End Use Application', 'Energy carrier', 'Flow Name', 'Formula', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   
                                                
electric_gen_ef_agg['Case'] = 'Reference Case'
electric_gen_ef_agg['Mitigation Case'] = '-'
if save_interim_files == True:
    electric_gen_ef_agg[cols_elec_env_agg].to_csv(interim_path_prefix + '\\' + f_elec_env_agg)
 
# merging the electricity production data with the total emissions data    
elec_gen_em_agg = pd.merge(electric_gen, electric_gen_ef_agg, how='left', on=['Year', 'Sector', 'End Use Application', 'Energy carrier']).drop(columns=['loss_frac']) 
elec_gen_em_agg.rename(columns={
    'Unit' : 'Energy Unit', 'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

# Adding GHG emissions from: 
# 'Incineration of Waste', 
# 'Electrical Transmission and Distribution', 
# 'Other Process Uses of Carbonates'

EPA_GHGI_maxyear = np.max(ob_EPA_GHGI.df_ghgi['Year'])
EPA_GHGI_addn_em = ob_EPA_GHGI.df_ghgi.loc[(ob_EPA_GHGI.df_ghgi['Economic Sector'] == 'Electric Power') & 
   (ob_EPA_GHGI.df_ghgi['Year'] == EPA_GHGI_maxyear)]

EPA_GHGI_addn_em = EPA_GHGI_addn_em.\
    groupby(['Year', 'Source', 'Emissions Type', 'Unit']).\
        agg({'GHG Emissions' : 'sum'}).reset_index()
        
EPA_GHGI_addn_em_agg = EPA_GHGI_addn_em.groupby(['Emissions Type', 'Unit']).agg({'GHG Emissions' : 'sum'}).reset_index()
         
# unit conversion
EPA_GHGI_addn_em_agg [['Unit', 'GHG Emissions']] = ob_units.unit_convert_df (
    EPA_GHGI_addn_em_agg [['Unit', 'GHG Emissions']], Unit='Unit', Value='GHG Emissions', if_given_unit = True, 
    given_unit = elec_gen_em_agg['Emissions Unit'].unique()[0]).copy()

elec_gen_em_agg = pd.merge(elec_gen_em_agg, EPA_GHGI_addn_em_agg, 
                               how='left', left_on='Formula', right_on='Emissions Type')

elec_gen_em_agg['Total Emissions'] = elec_gen_em_agg['Total Emissions'] + elec_gen_em_agg['GHG Emissions']

elec_gen_em_agg.rename(columns={'Case_x' : 'Case'}, inplace=True)

elec_gen_em_agg['Mitigation Case'] = '-'

elec_gen_em_agg = elec_gen_em_agg.groupby(['Case', 'Mitigation Case', 'Sector', 'End Use Application',
                                           'Energy carrier', 'Formula', 
                                           'Year', 'Energy Unit', 'Emissions Unit']).agg({'Total Emissions' : 'sum',
                                                                           'Electricity Production' : 'sum'}).reset_index()

elec_gen_em_agg['CI'] = elec_gen_em_agg['Total Emissions'] / elec_gen_em_agg['Electricity Production']
elec_gen_em_agg['Mitigation Case'] = '-'

if save_interim_files == True:
    elec_gen_em_agg[cols_elec_CI].to_csv(interim_path_prefix + '\\' + f_elec_CI)

# Separate non-electric, non-electric NEU, and electric activities --> merge to ef data frames and calculate total emissions

activity_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] == 'Electricity',:]

activity_non_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] != 'Electricity',:]

neu_energy_carriers = ['Hydrocarbon Gas Liquid Feedstocks',
                       'Petrochemical Feedstocks',
                       'Lubricants',
                       'Asphalt and Road Oil']
activity_non_elec_neu = activity_non_elec.loc[activity_non_elec['Energy carrier'].isin(neu_energy_carriers), : ]
activity_non_elec = activity_non_elec.loc[~activity_non_elec['Energy carrier'].isin(neu_energy_carriers), : ]

# Map direct combustion wrt energy carrier for non-electric. For electric, map aggregrate CIs that we calculated and then calculate the net emissions and GWPs
activity_elec = pd.merge(activity_elec, elec_gen_em_agg[['Year', 'Energy carrier', 'Formula', 'Emissions Unit', 'CI']], 
         how='left', on=['Year', 'Energy carrier'])

activity_non_elec = pd.merge(activity_non_elec, ob_ef.ef, 
         how='left', on=['Case', 'Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 'End Use Application', 'Year'])

activity_non_elec_neu = pd.merge(activity_non_elec_neu, neu_EF_GREET[['Energy carrier', 'Flow Name', 'Emissions Type', 'EF Numerator', 'EF', 'Scope']], 
         how='left', left_on=['Energy carrier'], right_on = ['Energy carrier'])
activity_non_elec_neu.rename(columns={'EF' : 'CI',
                                      'Emissions Type' : 'Formula',
                                      'EF Numerator' : 'Emissions Unit',
                                      'Scope_y' : 'Scope'}, inplace=True)

activity_non_elec.rename(columns={'Reference case' : 'CI',
                                  'Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

activity_elec['Total Emissions'] = activity_elec['Value'] * activity_elec['CI']
activity_elec['Scope'] = 'Electricity, Combustion'

activity_non_elec['Total Emissions'] = activity_non_elec['Value'] * activity_non_elec['CI']
activity_non_elec['Scope'] = 'Direct, Combustion'

activity_non_elec_neu['Total Emissions'] = activity_non_elec_neu['Value'] * activity_non_elec_neu['CI']

# Re-arrange columns
activity_elec['Mitigation Case'] = '-'
activity_elec = activity_elec[model_col_list]

activity_non_elec['Mitigation Case'] = '-'
activity_non_elec = activity_non_elec[model_col_list]

activity_non_elec_neu['Mitigation Case'] = '-'
activity_non_elec_neu = activity_non_elec_neu[model_col_list]

# Generate the Environmental Matrix
activity_BAU = pd.concat ([ob_EPA_GHGI.activity_non_combust_exp, activity_elec, activity_non_elec, activity_non_elec_neu], axis=0).reset_index(drop=True)

# Calculate LCIA metric
activity_BAU = pd.merge(activity_BAU, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_BAU['LCIA_estimate'] = activity_BAU['Total Emissions'] * activity_BAU['GWP']

activity_BAU.loc[~activity_BAU['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_BAU.loc[~activity_BAU['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_BAU['Mitigation Case'] = '-'

print("Status: Saving activity_reference case table to file ..")
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))

#%%

"""
Generating Electric power mitigation scenarios
"""

print("Status: Constructing Electric generation Mitigation scenario ..")

# subsetting electric generation data from mitigation modeling
elec_gen_mtg = ob_elec.NREL_elec['generation'].\
    groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 'Energy carrier', 'Energy Unit'], as_index=False). \
    agg({'Electricity Production' : 'sum'}).reset_index()

# Merge and calculate electric generation considering on T&D loss
elec_gen_mtg = pd.merge(elec_gen_mtg, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
elec_gen_mtg['Electricity Production'] = elec_gen_mtg['Electricity Production'] * (1 - elec_gen_mtg['loss_frac'])

electric_gen = pd.concat([electric_gen, elec_gen_mtg], axis = 0).reset_index(drop=True)
if save_interim_files == True:
    electric_gen[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)

# Merge emission factors for fuel-feedstock combustion used for electricity generation with net electricity generation
elec_gen_ef_mtg = pd.merge(ob_elec.NREL_elec['generation'][['Sector', 'Subsector', 'Case', 'Mitigation Case',
                                                            'Generation Type','Year', 'Energy carrier', 
                                                            'Energy carrier type', 'Electricity Production', 'Energy Unit']],
                           ob_ef.ef_electric, 
                           how='left',
                           on=['Sector', 'Subsector', 'Case', 'Year', 'Energy carrier', 'Energy carrier type']).reset_index()

# Calculate net emission by GHG species, from electricity generation    
elec_gen_ef_mtg['Total Emissions'] = elec_gen_ef_mtg['Reference case'] * elec_gen_ef_mtg['Electricity Production'] 

# Rename and re-arrange columns
elec_gen_ef_mtg.rename(columns={'Reference case' : 'EF_withElec',
                                'Elec0' : 'EF_Elec0'}, inplace = True)
elec_gen_ef_mtg[['Basis',
                 'Fuel Pool']] = '-'

# Save electric gen environmental matrix
if save_interim_files == True:
    tempdf = pd.concat([electric_gen_ef[cols_elec_env], elec_gen_ef_mtg[cols_elec_env] ], axis=0).reset_index(drop=True)
    tempdf.to_csv(interim_path_prefix + '\\' + f_elec_env)
    del tempdf
        
# Aggregrate emissions
electric_gen_ef_mtg_agg = elec_gen_ef_mtg.groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 'Energy carrier', 
                                                   'Flow Name', 'Formula', 'Energy Unit', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   
                                               
if save_interim_files == True:
    tempdf = electric_gen_ef_agg.groupby(['Case', 'Mitigation Case', 'Sector',
                                          'Energy carrier', 'Formula', 
                                          'Year', 'EF_Unit (Numerator)'], as_index=False).agg({'Total Emissions' : 'sum'})
    tempdf = pd.concat([tempdf[cols_elec_env_agg], electric_gen_ef_mtg_agg[cols_elec_env_agg]], axis=0).reset_index()
    tempdf.to_csv(interim_path_prefix + '\\' + f_elec_env_agg)
    del tempdf
 
# merging the electricity production data with the total emissions data    
elec_gen_em_mtg_agg = pd.merge(elec_gen_mtg, electric_gen_ef_mtg_agg, how='left', on=['Sector', 'Subsector', 'Case', 
                        'Mitigation Case', 'Year', 'Energy carrier', 'Energy Unit']).reset_index(drop=True).drop(columns=['loss_frac']) 

elec_gen_em_mtg_agg.rename(columns={
    'Unit' : 'Energy Unit', 
    'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

elec_gen_em_mtg_agg['CI'] = elec_gen_em_mtg_agg['Total Emissions'] / elec_gen_em_mtg_agg['Electricity Production']

if save_interim_files == True:
    tempdf = pd.concat([elec_gen_em_agg[cols_elec_CI], elec_gen_em_mtg_agg[cols_elec_CI]], axis=0).reset_index(drop=True)
    tempdf.to_csv(interim_path_prefix + '\\' + f_elec_CI)
    del tempdf

# constructing the Electricity mitigation matrix calculating difference in Electricity grid CIs

elec_gen_em_mtg_agg_m = pd.merge(elec_gen_em_agg, elec_gen_em_mtg_agg, 
         how='outer', on = ['Year', 'Sector', 'Energy carrier', 'Formula',
                'Energy Unit', 'Emissions Unit'] ).reset_index(drop=True)

elec_gen_em_mtg_agg_m.rename(columns={'Case_y' : 'Case',
                                      'Mitigation Case_y' : 'Mitigation Case',
                                      'CI_x' : 'CI_ref_case_elec', 
                                      'CI_y' : 'CI_elec_mtg',
                                      'Total Emissions_x' : 'Total Emissions_ref_case',
                                      'Total Emissions_y' : 'Total Emissions_mtg_elec',
                                      'Electricity Production_x' : 'Electricity Production_ref_case',
                                      'Electricity Production_y' : 'Electricity Production_mtg_elec'}, inplace=True)
elec_gen_em_mtg_agg_m.drop(columns=['Case_x', 'Mitigation Case_x'], inplace=True)
elec_gen_em_mtg_agg_m ['CI_diff_elec_mtg_ref_case'] = elec_gen_em_mtg_agg_m  ['CI_elec_mtg'] - elec_gen_em_mtg_agg_m ['CI_ref_case_elec']

if save_interim_files == True:
    elec_gen_em_mtg_agg_m.to_csv(interim_path_prefix + '\\' + 'interim_electric_ref_mtg_agg_CI.csv')

# Constructing mitigation scenarios for Electricity based activities
activity_mtg_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] == 'Electricity', : ]

activity_mtg_elec = pd.merge(activity_mtg_elec, elec_gen_em_mtg_agg_m[['Case', 'Year', 
                                                   'Formula',
                                                   'Emissions Unit', 'Energy Unit', 
                                                   'CI_diff_elec_mtg_ref_case']], 
                             how='left', 
                             on=['Year']).reset_index(drop=True)

activity_mtg_elec['Total Emissions'] = activity_mtg_elec['Value'] * activity_mtg_elec['CI_diff_elec_mtg_ref_case']

activity_mtg_elec.rename(columns={'Case_y' : 'Case',
                                  'CI_diff_elec_mtg_ref_case' : 'CI',
                                  'Emissions Type' : 'Formula'}, inplace=True)
activity_mtg_elec['Scope'] = 'Electricity, Combustion'

# Calculate LCIA metric
activity_mtg_elec = pd.merge(activity_mtg_elec, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_elec['LCIA_estimate'] = activity_mtg_elec['Total Emissions'] * activity_mtg_elec['GWP']

activity_mtg_elec.loc[~activity_mtg_elec['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_elec.loc[~activity_mtg_elec['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

# Adding 'Mitigation Case' to model column list
activity_BAU['Mitigation Case'] = '-'
activity_mtg_elec['Mitigation Case'] = '-'
activity_mtg_elec = activity_mtg_elec[model_col_list]

activity_BAU = pd.concat([activity_BAU, activity_mtg_elec], axis=0).reset_index(drop=True)

if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for Residential and Commercial sectors with SCOUT Model
"""

print("Status: Constructing Residential and Commercial sectors Mitigation scenario ..")

# Creating activity data table for both reference case and SCOUT mitigation case
activity_ref_mtg = ob_eia.EIA_data['energy_demand'].copy()
activity_ref_mtg['Mitigation Case'] = '-'

ob_scout = SCOUT(ob_units, input_path_SCOUT, input_path_corr)

activity_mtg_scout = ob_scout.df_scout.copy()

# Concatenate to activity data frame and save
temp = activity_mtg_scout.copy()
temp[['AEO Case', 'Basis', 'Generation Type', 'Fuel Pool']] = '-'
temp = temp[['Data Source', 'AEO Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application',
              'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
              'Value', 'Case', 'Generation Type', 'Fuel Pool']]
activity_ref_mtg = pd.concat([activity_ref_mtg, temp.copy()], axis=0).reset_index(drop=True)
del temp

if save_interim_files == True:
    activity_ref_mtg.to_csv(interim_path_prefix + '\\' + f_interim_activity)
    activity_ref_mtg[cols_activity_out].to_csv(output_path_prefix + '\\' + f_out_activity)

# Separate electric and non electric activities
activity_mtg_scout_elec = activity_mtg_scout.loc[activity_mtg_scout['Energy carrier'] == 'Electricity', : ]
activity_mtg_scout = activity_mtg_scout.loc[~(activity_mtg_scout['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_scout = pd.merge(activity_mtg_scout, corr_EF_GREET.loc[corr_EF_GREET['Scope'] == 'Direct, Combustion', :], how='left', 
                             on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                 'End Use Application']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_scout = pd.merge(activity_mtg_scout, ob_ef.ef_raw, 
                             how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to SCOUT
activity_mtg_scout_elec = pd.merge(activity_mtg_scout_elec, 
                                   elec_gen_em_mtg_agg_m[['Flow Name', 'Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                                   how='left',
                                   on=['Year'])
activity_mtg_scout_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)

activity_mtg_scout.rename(columns={'End Use Application_x' : 'End Use Application',
                               'Unit (Numerator)' : 'Emissions Unit',
                               'Unit (Denominator)' : 'Energy Unit',
                               'Reference case' : 'CI'}, inplace=True)
activity_mtg_scout.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

# Concatenate electric and non-electric activities
activity_mtg_scout = pd.concat([activity_mtg_scout, activity_mtg_scout_elec], axis = 0).reset_index(drop=True)

activity_mtg_scout['Total Emissions'] = activity_mtg_scout['Value'] * activity_mtg_scout['CI']

# Calculate LCIA metric
activity_mtg_scout = pd.merge(activity_mtg_scout, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_scout['LCIA_estimate'] = activity_mtg_scout['Total Emissions'] * activity_mtg_scout['GWP']

activity_mtg_scout.loc[~activity_mtg_scout['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_scout.loc[~activity_mtg_scout['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_mtg_scout[['AEO Case', 'Basis', 'Fuel Pool']] = '-'
activity_mtg_scout = activity_mtg_scout[activity_BAU.columns]

#activity_mtg_scout = activity_mtg_scout[model_col_list]

# Mapping EIA AEO sector, etc. to SCOUT conventions
temp_activity = activity_BAU.loc[(activity_BAU['Sector'].isin(corr_EIA_SCOUT['Sector'].unique()) ) &
                                 (activity_BAU['Subsector'].isin(corr_EIA_SCOUT['Subsector'].unique())) &
                                 (activity_BAU['End Use Application'].isin(corr_EIA_SCOUT['EIA: End Use Application'].unique())) &
                                 (activity_BAU['Energy carrier'].isin(corr_EIA_SCOUT['EIA: Energy carrier'].unique())) &
                                 (activity_BAU['Energy carrier type'].isin(corr_EIA_SCOUT['EIA: Energy carrier type'].unique())), : ]

activity_BAU =  activity_BAU.loc[~(activity_BAU['Sector'].isin(corr_EIA_SCOUT['Sector'].unique()) ) |
                                 ~(activity_BAU['Subsector'].isin(corr_EIA_SCOUT['Subsector'].unique())) |
                                 ~(activity_BAU['End Use Application'].isin(corr_EIA_SCOUT['EIA: End Use Application'].unique())) |
                                 ~(activity_BAU['Energy carrier'].isin(corr_EIA_SCOUT['EIA: Energy carrier'].unique())) |
                                 ~(activity_BAU['Energy carrier type'].isin(corr_EIA_SCOUT['EIA: Energy carrier type'].unique())), : ]

temp_activity = pd.merge(temp_activity, 
         corr_EIA_SCOUT[['Sector', 'Subsector', 'EIA: End Use Application', 'SCOUT: End Use Application', 
                         'EIA: Energy carrier', 'EIA: Energy carrier type', 'Energy carrier']].drop_duplicates(), 
         how='left', 
         left_on=['Sector', 'Subsector', 'End Use Application', 'Energy carrier', 'Energy carrier type'], 
         right_on=['Sector', 'Subsector', 'EIA: End Use Application', 'EIA: Energy carrier', 'EIA: Energy carrier type']).reset_index(drop=True)

temp_activity.drop(columns=['Energy carrier_x', 'EIA: Energy carrier', 'EIA: Energy carrier type', 
                           'End Use Application'], inplace=True)
temp_activity.rename(columns={'Energy carrier_y' : 'Energy carrier',
                             'SCOUT: End Use Application' : 'End Use Application'}, inplace=True)

# Concatenating to environmental matrix
activity_BAU = pd.concat([activity_BAU, 
                          temp_activity[activity_BAU.columns], 
                          activity_mtg_scout[activity_BAU.columns]], axis=0).reset_index(drop=True)
del temp_activity

if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for Transportation sector with VISION/Tempo Models
"""

print("Status: Constructing Transportation sector Mitigation scenario ..")

activity_mtg_vision = ob_VISION.vision

temp_activity = activity_ref_mtg.loc[(activity_ref_mtg['Case'] == 'Reference case') &
                                     (activity_ref_mtg['Sector'].isin(activity_mtg_vision['Sector'].unique())) &
                                     (activity_ref_mtg['Subsector'].isin(activity_mtg_vision['Subsector'].unique())) & 
                                     (activity_ref_mtg['End Use Application'].isin(activity_mtg_vision['End Use Application'].unique())), :]
activity_mtg_vision = pd.merge(activity_mtg_vision, temp_activity,
                             how='left',
                             on=['Sector', 'Subsector', 'End Use Application', 'Energy carrier', 
                                 'Energy carrier type', 'Year']).reset_index(drop=True)

# Calculate the relative value between reference case and the mitigation case
activity_mtg_vision['Value'] = activity_mtg_vision['Value_x'] - activity_mtg_vision['Value_y'] ## Mitigation case - Reference case

activity_mtg_vision.loc[activity_mtg_vision['Energy carrier type'] == 'FT-Diesel', 'Value'] = \
    activity_mtg_vision.loc[activity_mtg_vision['Energy carrier type'] == 'FT-Diesel', 'Value_x']

activity_mtg_vision.rename(columns={'Data Source_x' : 'Data Source',
                                    'Unit_x' : 'Unit',
                                    'Case_x' : 'Case'}, inplace=True)
activity_mtg_vision = activity_mtg_vision[temp_activity.columns]

activity_ref_mtg = pd.concat([activity_ref_mtg, activity_mtg_vision.copy()], axis=0).reset_index(drop=True)

if save_interim_files == True:
    activity_ref_mtg.to_csv(interim_path_prefix + '\\' + f_interim_activity)
    activity_ref_mtg[cols_activity_out].to_csv(output_path_prefix + '\\' + f_out_activity)
  
del temp_activity

# Seperate electric and non-electric activities
activity_mtg_vision_elec = activity_mtg_vision.loc[activity_mtg_vision['Energy carrier'] == 'Electricity', : ]
activity_mtg_vision = activity_mtg_vision.loc[~(activity_mtg_vision['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_vision = pd.merge(activity_mtg_vision, corr_EF_GREET.loc[corr_EF_GREET['Scope'] == 'Direct, Combustion', :], how='left', 
                               on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_vision = pd.merge(activity_mtg_vision, ob_ef.ef_raw, 
                               how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

#temp_identify = activity_mtg_vision.loc[activity_mtg_vision['Reference case'].isna(), ['Case', 'Scope', 'GREET Pathway']].drop_duplicates()

# Merge NREL mitigation scenario electricity CIs to VISION
activity_mtg_vision_elec = pd.merge(activity_mtg_vision_elec, 
                                   elec_gen_em_mtg_agg_m[['Flow Name', 'Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                                   how='left',
                                   on=['Year'])
activity_mtg_vision_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)

activity_mtg_vision.rename(columns={'Unit (Numerator)' : 'Emissions Unit',
                               'Unit (Denominator)' : 'Energy Unit',
                               'Reference case' : 'CI'}, inplace=True)
activity_mtg_vision.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

# Concatenate electric and non-electric activities
activity_mtg_vision = pd.concat([activity_mtg_vision, activity_mtg_vision_elec], axis = 0).reset_index(drop=True)

activity_mtg_vision['Total Emissions'] = activity_mtg_vision['Value'] * activity_mtg_vision['CI']

# Calculate LCIA metric
activity_mtg_vision = pd.merge(activity_mtg_vision, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_vision['LCIA_estimate'] = activity_mtg_vision['Total Emissions'] * activity_mtg_vision['GWP']

activity_mtg_vision.loc[~activity_mtg_vision['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_vision.loc[~activity_mtg_vision['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_mtg_vision[['AEO Case', 'Basis', 'Fuel Pool']] = '-'
activity_mtg_vision = activity_mtg_vision[activity_BAU.columns]

# Concatenating to main activity matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_vision], axis=0).reset_index(drop=True)

if save_interim_files == True:
   activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
   activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))

# next steps
# change values from absolute to relative
# append to the activity matrix
# merge with GREET EFs for non electric 
# merge with EERE electric EFs for electric
# merge with the environmental matrix

#%%
"""
Generating mitigation scenarios for Agriculture sector
"""

print("Status: Constructing Agriculture sector Mitigation scenario ..")

# Defining targetted Diesel to Electricity use ratio in 2050 year
D2E_mtg_2050 = 0.99
# Defining the relative efficiency of directly using Diesel compared to directly using Electricity
D2E_relative_eff = 0.40/0.90 # considering 40% energy from diesel used into activity and 90% electricity energy used into activity

# Subsetting Reference case energy demand for Agriculture sector
activity_mtg_ag = ob_eia.EIA_data['energy_demand']
activity_mtg_ag = activity_mtg_ag.loc[activity_mtg_ag['Sector']=='Agriculture', : ].copy()

# Implementing On-farm Electrification for Diesel use: mitigate Diesel use with Electricity use

# Subsetting with and without Diesel on farm use activities
activity_mtg_ag_d = activity_mtg_ag.loc[(activity_mtg_ag['End Use Application'] == 'On farm energy use') &
                                        (activity_mtg_ag['Energy carrier'] == 'Diesel'), : ]
activity_mtg_ag = activity_mtg_ag.loc[~(activity_mtg_ag['End Use Application'] == 'On farm energy use') |
                                      ~(activity_mtg_ag['Energy carrier'] == 'Diesel'), : ]

# Defining series of linearly increasing fraction of Electricity implementation and replacing Diesel
mtg_ag_df = pd.DataFrame({'Year' : np.linspace(min(activity_mtg_ag['Year']), max(activity_mtg_ag['Year']), max(activity_mtg_ag['Year']) - min(activity_mtg_ag['Year']) + 1 ), 
                          'mtg_frac' : np.linspace(0, D2E_mtg_2050, max(activity_mtg_ag['Year']) - min(activity_mtg_ag['Year']) + 1 ) } )

activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, mtg_ag_df, how='left', on='Year').reset_index(drop=True)

# Identifying the amount of diesel use and electricity use
activity_mtg_ag_d['Value Elec Use'] = activity_mtg_ag_d['Value'] * activity_mtg_ag_d['mtg_frac'] * D2E_relative_eff
activity_mtg_ag_d['Value Diesel Use'] = -1 * activity_mtg_ag_d['Value'] * activity_mtg_ag_d['mtg_frac'] # relative Diesel use, mitigation case - reference case

# Rows with Electricity use
temp_activity = activity_mtg_ag_d.drop(columns = ['Value', 'Value Diesel Use'])
temp_activity.rename(columns={'Value Elec Use' : 'Value'}, inplace=True)
temp_activity['Energy carrier'] = 'Electricity'
temp_activity['Energy carrier type'] = 'U.S. Average Grid Mix'

activity_mtg_ag_d.drop(columns = ['Value', 'Value Elec Use'], inplace=True)
activity_mtg_ag_d.rename(columns={'Value Diesel Use' : 'Value'}, inplace=True)

# Concatenate data frames to get electricity and diesel use-separated activities into one data frame
activity_mtg_ag_d = pd.concat([activity_mtg_ag_d, temp_activity], axis=0).reset_index(drop=True)
del temp_activity

activity_mtg_ag_d['Fuel Pool'] = 'Electricity'
activity_mtg_ag_d['Case'] = 'Mitigation'
activity_mtg_ag_d['Mitigation Case'] = 'On-Farm Mitigation'

# Append to activity matrix and save
activity_ref_mtg = pd.concat([activity_ref_mtg, activity_mtg_ag_d.copy()], axis=0).reset_index(drop=True)

if save_interim_files == True:
    activity_ref_mtg.to_csv(interim_path_prefix + '\\' + f_interim_activity)
    activity_ref_mtg[cols_activity_out].to_csv(output_path_prefix + '\\' + f_out_activity)

# Seperate electric and non-electric activities
activity_mtg_ag_d_elec = activity_mtg_ag_d.loc[activity_mtg_ag_d['Energy carrier'] == 'Electricity', : ]
activity_mtg_ag_d = activity_mtg_ag_d.loc[~(activity_mtg_ag_d['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, corr_EF_GREET.loc[corr_EF_GREET['Scope'] == 'Direct, Combustion', :], how='left', 
                               on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, ob_ef.ef_raw, 
                               how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to VISION
activity_mtg_ag_d_elec = pd.merge(activity_mtg_ag_d_elec, 
                                   elec_gen_em_mtg_agg_m[['Flow Name', 'Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                                   how='left',
                                   on=['Year'])
activity_mtg_ag_d_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)

activity_mtg_ag_d.rename(columns={'Unit (Numerator)' : 'Emissions Unit',
                               'Unit (Denominator)' : 'Energy Unit',
                               'Reference case' : 'CI'}, inplace=True)
activity_mtg_ag_d.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

# Concatenate electric and non-electric activities
activity_mtg_ag_d = pd.concat([activity_mtg_ag_d, activity_mtg_ag_d_elec], axis = 0).reset_index(drop=True)

activity_mtg_ag_d['Total Emissions'] = activity_mtg_ag_d['Value'] * activity_mtg_ag_d['CI']

# Calculate LCIA metric
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_ag_d['LCIA_estimate'] = activity_mtg_ag_d['Total Emissions'] * activity_mtg_ag_d['GWP']

activity_mtg_ag_d.loc[~activity_mtg_ag_d['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_ag_d.loc[~activity_mtg_ag_d['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_mtg_ag_d[['AEO Case', 'Basis']] = '-'

# Concatenating to main activity matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_ag_d], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)


print( 'Elapsed time: ' + str(datetime.now() - init_time))

#%%