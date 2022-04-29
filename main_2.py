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

f_corr_ghgs = 'corr_ghgi_emissions_categories.csv'

# defining the intermediate and final data table files and their columns
f_interim_activity = 'interim_activity_ref_mtg_cases.csv'
f_interim_env = 'interim_env_ref_mtg_cases.csv'
f_out_activity = 'activity_ref_mtg_cases.csv'
f_out_env = 'env_ref_mtg_cases.csv'
f_elec_net_gen = 'interim_elec_gen.csv'
f_elec_env = 'interim_elec_gen_env.csv'
f_elec_env_agg = 'interim_elec_gen_env_agg.csv'
f_elec_CI = 'interim_elec_gen_CI.csv'
f_industrial = 'industrial_flows.csv'

cols_activity_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Unit', 'Value']

cols_env_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Scope', 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Formula', 'Emissions Category, Detailed', 'Emissions Category, Aggregate',
                'Emissions Unit', 'Total Emissions', 'LCIA_estimate']

cols_elec_net_gen = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                     'Energy carrier', 'Energy carrier type', 'Generation Type', 'Year',
                     'Unit', 'Electricity Production']

cols_elec_env = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool', 'Generation Type',
                 'Scope', 'Formula', 'Emissions Category, Detailed', 'Emissions Category, Aggregate',
                 'Year', 'EF_Unit (Numerator)', 'Total Emissions']

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

# Mitigation scenario design and target parameters
Ag_mtg_params = {'D2E_mtg_2050' : 1.0, # targetted Diesel to Electricity use ratio in 2050 year
                 'D2E_relative_eff' : 0.40/0.90, # The relative efficiency of directly using Diesel compared to directly using Electricity. Considering 40% energy from diesel used into activity and 90% electricity energy used into activity
                 'manure_mgmt' : 1.0, # Target percentage of reduced GHG emissions from manure management activities. Ag / Anaerobic Digestion / Manure MGMT / CH4, N2O
                 'soil_N2O' : 1.0, # Target percentage of reduced GHG emissions from precisiion farming activitis. Ag / Precision Farming / Soil N2O / N2O
                 'rice_cultv' : 1.0 # Target percentage of reduced GHG emissions from rice cultivation. Ag / Improved Water and Residue MGMT / Rice Cultivation / CH4
                }

# T&D assumption, constant or calculated
# T_and_D_loss_constant = True
# T_and_D_loss = 0.06

# parameter to print out additional information when code is running
verbose = True

#%%

# import packages
import pandas as pd
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
from utilities import Utilities
from collections import Counter

#%%
# Utility functions

def save_activity_mx (df_to, df, save_interim_files):    
    df_to = pd.concat([df_to.copy(), df.copy()], axis=0).reset_index(drop=True)

    if save_interim_files == True:
        df_to.to_csv(interim_path_prefix + '\\' + f_interim_activity)
        df_to[cols_activity_out].to_csv(output_path_prefix + '\\' + f_out_activity)
        
    return df_to.copy()

#%%

init_time = datetime.now()

# Create data class objects

# Unit conversion class object
ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)

# Utilities class object
ob_utils = Utilities()

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
ob_VISION = VISION(ob_units, input_path_VISION, input_path_corr)

# GREET emission factor load
ob_ef = GREET_EF(input_path_GREET )
                      
# Data tables for correspondence across data sets
corr_EF_GREET = pd.read_excel(input_path_corr + '\\' + f_corr_ef_greet, sheet_name = sheet_corr_ef_greet, header = 3)
corr_EIA_SCOUT = pd.read_excel(input_path_corr + '\\' + f_corr_EIA_SCOUT, sheet_name = sheet_corr_EIA_SCOUT, header = 3, index_col=None)
corr_ghgs = pd.read_csv(input_path_corr + '\\' + f_corr_ghgs, header = 3, index_col=None)

# Life Cycle Impact Assessment metrics table
lcia_data = pd.read_excel(input_path_EPA + '\\' + f_lcia, sheet_name = f_lcia_sheet)         
lcia_select = lcia_data.loc[ (lcia_data['LCIA Method'] == LCIA_Method) & (lcia_data['timeframe_years'] == lcia_timeframe) ]

# Loading Non-energy use EFs
neu_EF_GREET = pd.read_excel(input_path_neu + '\\' + f_neu, sheet_name = sheet_neu, header = 3)

# Loading industrial data for constructing mitigation scenarios 
bulk_chem = pd.read_csv(input_path_EPA + '\\' + f_industrial)
bulk_chem.drop(columns=['notes'], inplace=True)

#%%

#%%

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
# Two data frames, electric_gen_interim and electric_gen created to group by separately for output files
electric_gen_interim = ob_eia.EIA_data['energy_supply'].groupby(['Year', 'Sector', 'End Use', 'Energy carrier', 
                                                                 'Energy carrier type', 'Generation Type', 'Unit']).\
                                                agg({'Value' : 'sum'}).reset_index().\
                                                rename(columns = {'Value' : 'Electricity Production'})
electric_gen_interim = pd.merge(electric_gen_interim, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
electric_gen_interim['Electricity Production'] = electric_gen_interim['Electricity Production'] * (1 - electric_gen_interim['loss_frac'])
electric_gen_interim.rename(columns={'End Use' : 'End Use Application'}, inplace=True)
electric_gen_interim['Case'] = 'Reference Case'
electric_gen_interim[['Mitigation Case', 'Subsector']] = '-'

electric_gen = ob_eia.EIA_data['energy_supply'].groupby(['Year', 'Sector', 'End Use', 'Energy carrier', 'Unit']).\
                                                agg({'Value' : 'sum'}).reset_index().\
                                                rename(columns = {'Value' : 'Electricity Production'})
electric_gen = pd.merge(electric_gen, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
electric_gen['Electricity Production'] = electric_gen['Electricity Production'] * (1 - electric_gen['loss_frac'])
electric_gen.rename(columns={'End Use' : 'End Use Application'}, inplace=True)
electric_gen['Case'] = 'Reference Case'
electric_gen[['Mitigation Case', 'Subsector']] = '-'

if save_interim_files == True:
    electric_gen_interim[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)

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

# Adding non-combustion upstream emissions fron Incineration of Waste', 'Electrical Transmission and Distribution', and 'Other Process Uses of Carbonates'
ob_EPA_GHGI.activity_elec_non_combust_exp[['GREET Pathway', 'Generation Type', 
                                           'Energy Unit', 'Electricity Production',                                             
                                           'EF_Unit (Denominator)', 
                                           'EF_withElec', 'Mitigation Case']] = '-'
ob_EPA_GHGI.activity_elec_non_combust_exp.rename(columns={'Emissions Unit' : 'EF_Unit (Numerator)'}, inplace=True)
# unit conversion
ob_EPA_GHGI.activity_elec_non_combust_exp [['EF_Unit (Numerator)', 'Total Emissions']] = ob_units.unit_convert_df (
    ob_EPA_GHGI.activity_elec_non_combust_exp [['EF_Unit (Numerator)', 'Total Emissions']], Unit='EF_Unit (Numerator)', Value='Total Emissions', if_given_unit = True, 
    given_unit = electric_gen_ef['EF_Unit (Numerator)'].unique()[0]).copy()

electric_gen_ef = pd.concat([electric_gen_ef, ob_EPA_GHGI.activity_elec_non_combust_exp[electric_gen_ef.columns]], axis=0).reset_index(drop=True)

if save_interim_files == True:
    electric_gen_ef = pd.merge(electric_gen_ef, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
    electric_gen_ef[cols_elec_env].to_csv(interim_path_prefix + '\\' + f_elec_env)

# Aggregrate emissions
electric_gen_ef_agg = electric_gen_ef.groupby(['Year', 'Sector', 'End Use Application', 'Energy carrier', 'Flow Name', 'Formula', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   
                                                
electric_gen_ef_agg['Case'] = 'Reference Case'
electric_gen_ef_agg['Mitigation Case'] = '-'
if save_interim_files == True:
    electric_gen_ef_agg[cols_elec_env_agg].to_csv(interim_path_prefix + '\\' + f_elec_env_agg)
 
# merging the electricity production data with the total emissions data    
elec_gen_em_agg = pd.merge(electric_gen, electric_gen_ef_agg, 
                           how='left', 
                           on=['Year', 'Sector', 'End Use Application', 'Energy carrier']). \
                  reset_index(drop=True).drop(columns=['loss_frac']) 
elec_gen_em_agg.rename(columns={
    'Unit' : 'Energy Unit', 'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

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

# Ammonia Industry Reference case adjustment as per increase in production per shipment revenue
activity_non_combust_ammonia = ob_EPA_GHGI.activity_non_combust_exp.loc[(ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Industrial') & 
                                                                       (ob_EPA_GHGI.activity_non_combust_exp['Subsector'] == 'Ammonia Production'), :]

activity_non_combust_oth = ob_EPA_GHGI.activity_non_combust_exp.loc[~((ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Industrial') & 
                                                                       (ob_EPA_GHGI.activity_non_combust_exp['Subsector'] == 'Ammonia Production')), :]
 
activity_non_combust_ammonia = pd.merge(activity_non_combust_ammonia, 
                                        ob_eia.EIA_data['chemical_industry_supp'][['Sector', 'Parameter', 'Year', 'frac_increase']],
                                        how='left',
                                        left_on=['Sector', 'Subsector', 'Year'],
                                        right_on=['Sector', 'Parameter', 'Year']).reset_index(drop=True)
activity_non_combust_ammonia['End Use Application'] = activity_non_combust_ammonia['Parameter']
activity_non_combust_ammonia['Subsector'] = 'Bulk Chemical Industry'

activity_non_combust_ammonia['Total Emissions'] = activity_non_combust_ammonia['Total Emissions'] * activity_non_combust_ammonia['frac_increase'] 

ob_EPA_GHGI.activity_non_combust_exp = pd.concat([activity_non_combust_ammonia, activity_non_combust_oth], axis=0).reset_index(drop=True)

ob_EPA_GHGI.activity_non_combust_exp.drop(columns=['Parameter', 'frac_increase'], inplace=True)
ob_EPA_GHGI.activity_non_combust_exp['Case'] = 'Reference case'
ob_EPA_GHGI.activity_non_combust_exp['Mitigation Case'] = '-'

# Generate the Environmental Matrix
activity_BAU = pd.concat ([ob_EPA_GHGI.activity_non_combust_exp, activity_elec, activity_non_elec, activity_non_elec_neu], axis=0).reset_index(drop=True)

del activity_non_combust_ammonia, activity_non_combust_oth

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
    activity_BAU = pd.merge(activity_BAU, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
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

# Separate grouping variables for saving 
tempdf = ob_elec.NREL_elec['generation'].\
    groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 
             'Energy carrier', 'Energy carrier type', 'Generation Type',
             'Energy Unit'], as_index=False). \
    agg({'Electricity Production' : 'sum'}).reset_index()
tempdf = pd.merge(tempdf, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
tempdf['Electricity Production'] = tempdf['Electricity Production'] * (1 - tempdf['loss_frac'])
electric_gen_interim = pd.concat([electric_gen, tempdf], axis = 0).reset_index(drop=True)
if save_interim_files == True:
    electric_gen_interim[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)
del tempdf

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
    tempdf = elec_gen_ef_mtg.copy()
    tempdf = pd.merge(tempdf, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
    tempdf = pd.concat([electric_gen_ef, tempdf[cols_elec_env] ], axis=0).reset_index(drop=True)
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

activity_mtg_elec['Case'] = 'Mitigation'
activity_mtg_elec['Mitigation Case'] = 'NREL Electric Power Decarb'
#activity_mtg_elec = activity_mtg_elec[model_col_list]

activity_mtg_elec = pd.merge(activity_mtg_elec, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
activity_BAU = pd.concat([activity_BAU, activity_mtg_elec], axis=0).reset_index(drop=True)

activity_BAU.drop(columns=['Case_x'], inplace=True)

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
activity_ref_mtg = save_activity_mx(activity_ref_mtg, temp.copy(), save_interim_files)
del temp

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

activity_mtg_scout[['AEO Case', 'Basis', 'Fuel Pool', 'Generation Type']] = '-'
#activity_mtg_scout = activity_mtg_scout[activity_BAU.columns]

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

activity_mtg_scout = pd.merge(activity_mtg_scout, corr_ghgs, how='left', on='Formula').reset_index(drop=True)

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

# save to activity matrix
activity_ref_mtg = save_activity_mx(activity_ref_mtg, activity_mtg_vision.copy(), save_interim_files)
  
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

activity_mtg_vision = pd.merge(activity_mtg_vision, corr_ghgs, how='left', on='Formula').reset_index(drop=True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_vision], axis=0).reset_index(drop=True)

if save_interim_files == True:
   activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
   activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))

# next steps
# change values from absolute to relative
# append to the Environment matrix
# merge with GREET EFs for non electric 
# merge with EERE electric EFs for electric
# merge with the environmental matrix

#%%
"""
Generating mitigation scenarios for Agriculture sector
"""

print("Status: Constructing Agriculture sector Mitigation scenario ..")
    
# Subsetting Reference case energy demand for Agriculture sector
activity_mtg_ag = ob_eia.EIA_data['energy_demand']
activity_mtg_ag = activity_mtg_ag.loc[activity_mtg_ag['Sector']=='Agriculture', : ].copy()

# Implementing On-farm Electrification for Diesel use: mitigate Diesel use with Electricity use

# Subsetting with and without Diesel on farm use activities
activity_mtg_ag_d = activity_mtg_ag.loc[(activity_mtg_ag['End Use Application'] == 'On farm energy use') &
                                        (activity_mtg_ag['Energy carrier'] == 'Diesel'), : ]
activity_mtg_ag = activity_mtg_ag.loc[~(activity_mtg_ag['End Use Application'] == 'On farm energy use') |
                                      ~(activity_mtg_ag['Energy carrier'] == 'Diesel'), : ]

# Creating series of linearly increasing fraction of Electricity implementation and replacing Diesel
mtg_ag_df = ob_utils.trend_linear(activity_mtg_ag[['Year']], 'Year', 0, Ag_mtg_params['D2E_mtg_2050'])

activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, mtg_ag_df, how='left', on='Year').reset_index(drop=True)

# Identifying the amount of diesel use and electricity use
activity_mtg_ag_d['Value Elec Use'] = activity_mtg_ag_d['Value'] * activity_mtg_ag_d['mtg_frac'] * Ag_mtg_params['D2E_relative_eff']
activity_mtg_ag_d['Value Diesel Use'] = -1 * activity_mtg_ag_d['Value'] * activity_mtg_ag_d['mtg_frac'] # relative Diesel use, mitigation case - reference case
activity_mtg_ag_d.drop(columns=['mtg_frac'], inplace=True)

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
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  activity_mtg_ag_d.copy(), save_interim_files)

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

# Concatenating to main Environment matrix
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
activity_BAU = pd.concat([activity_BAU, activity_mtg_ag_d], axis=0).reset_index(drop=True)

"""
Mitigation Option:

<Setor / Mitigation Option / Subsector / GHGs>

Ag / Anaerobic Digestion / Manure MGMT / CH4, N2O
Ag / Precision Farming / Soil N2O / N2O
Ag / Improved Water and Residue MGMT / Rice Cultivation / CH4

LULUCF/ Sustainable Farming / Croppland remaining Cropland / CO2
"""

# Implementing mitigation scenarios for additional agriculture subsectors 

ag_mtg_subsector = ['Manure Management', 
                     'N2O from Agricultural Soil Management',
                     'Rice Cultivation']

activity_mtg_ag = ob_EPA_GHGI.activity_non_combust_exp.loc[(ob_EPA_GHGI.activity_non_combust_exp['Case'] == 'Reference case') &
                                                           (ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Agriculture') &
                                                           (ob_EPA_GHGI.activity_non_combust_exp['Subsector'].isin(ag_mtg_subsector)), : ]

# Ag / Anaerobic Digestion / Manure MGMT / CH4, N2O
mtg_ag_manure = activity_mtg_ag.loc[activity_mtg_ag['Subsector'] == 'Manure Management', : ]
trend_reduce = ob_utils.trend_linear(mtg_ag_manure[['Year']], 'Year', 0 , Ag_mtg_params['manure_mgmt'])
mtg_ag_manure = pd.merge(mtg_ag_manure, trend_reduce, how='left', on='Year')
mtg_ag_manure['Total Emissions'] = -1 * mtg_ag_manure['Total Emissions'] * mtg_ag_manure['mtg_frac']
mtg_ag_manure['Case'] = 'Mitigation'
mtg_ag_manure['Mitigation Case'] = 'Manure Management, linear reduction'

#Ag / Precision Farming / Soil N2O / N2O
mtg_ag_N2O = activity_mtg_ag.loc[activity_mtg_ag['Subsector'] == 'N2O from Agricultural Soil Management', : ]
trend_reduce = ob_utils.trend_linear(mtg_ag_N2O[['Year']], 'Year', 0 , Ag_mtg_params['rice_cultv'])
mtg_ag_N2O = pd.merge(mtg_ag_N2O, trend_reduce, how='left', on='Year')
mtg_ag_N2O['Total Emissions'] = -1 * mtg_ag_N2O['Total Emissions'] * mtg_ag_N2O['mtg_frac']
mtg_ag_N2O['Case'] = 'Mitigation'
mtg_ag_N2O['Mitigation Case'] = 'Soil N2O emissions, linear reduction'

#Ag / Improved Water and Residue MGMT / Rice Cultivation / CH4
mtg_ag_rice = activity_mtg_ag.loc[activity_mtg_ag['Subsector'] == 'Rice Cultivation', : ]
trend_reduce = ob_utils.trend_linear(mtg_ag_rice[['Year']], 'Year', 0 , Ag_mtg_params['soil_N2O'])
mtg_ag_rice = pd.merge(mtg_ag_rice, trend_reduce, how='left', on='Year')
mtg_ag_rice['Total Emissions'] = -1 * mtg_ag_rice['Total Emissions'] * mtg_ag_rice['mtg_frac']
mtg_ag_rice['Case'] = 'Mitigation'
mtg_ag_rice['Mitigation Case'] = 'Rice Cultivation, linear reduction'

# Concatenate the mitigation scenarios
activity_mtg_ag_d = pd.concat([mtg_ag_manure, mtg_ag_N2O, mtg_ag_rice], axis=0).reset_index(drop=True)

# Calculate LCIA metric
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_ag_d['LCIA_estimate'] = activity_mtg_ag_d['Total Emissions'] * activity_mtg_ag_d['GWP']

activity_mtg_ag_d.loc[~activity_mtg_ag_d['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_ag_d.loc[~activity_mtg_ag_d['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, corr_ghgs, how='left', on='Formula').reset_index(drop=True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_ag_d], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
    

print( 'Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for LULUCF
"""

print("Status: Constructing LULUCF sector Mitigation scenario ..")

n_years = 30

cropland_2050 = 137.234 # million Ha of cropland available in 2050 year

c_seq_rate = 0.404 * 44.01 / 12.01 # CO2 MT per million Ha increased carbon sequestration rate. Conventional sequestration rate is 0.105 MT C per million Ha, that is assumed to increase to 5 MT C per Ha

net_seq = c_seq_rate * cropland_2050 # CO2 MT in 2050

net_seq_yearly = net_seq / n_years # CO2 MT per year

activity_mtg_lulucf = pd.DataFrame({'Year' : [x for x in range(2020, 2051)],
                                    'Total Emissions' : [(-1 * net_seq_yearly * x)  for x in range(0, n_years+1)] })

activity_mtg_lulucf['Case' ] = 'Mitigation'
activity_mtg_lulucf['Mitigation Case'] = 'LULUCF: Sustainable Farming'
activity_mtg_lulucf['Sector'] = 'LULUCF'
activity_mtg_lulucf['Subsector'] = 'Cropland remaining cropland'
activity_mtg_lulucf['End Use Application'] = 'Sustainable farming'
activity_mtg_lulucf['Formula'] = 'CO2'
activity_mtg_lulucf['Unit'] = 'mmmt'

# Calculate LCIA metric
activity_mtg_lulucf = pd.merge(activity_mtg_lulucf, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_lulucf['LCIA_estimate'] = activity_mtg_lulucf['Total Emissions'] * activity_mtg_lulucf['GWP']

# Create rest of the empty columns
activity_mtg_lulucf [ list(( Counter(activity_BAU.columns) - Counter(activity_mtg_lulucf.columns )).elements()) ] = '-'

activity_mtg_lulucf = pd.merge(activity_mtg_lulucf, corr_ghgs, how='left', on='Formula').reset_index(drop=True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_lulucf], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
    

print( 'Elapsed time: ' + str(datetime.now() - init_time))


#%%
"""
Generating mitigation scenarios for the Industrial sector
"""
# Declaring parameters for Industry mitigation sectors
Id_mtg_params = {'mtg_paper' : 0.32, # target efficiency improvement across all activities of paper industries
                 'mtg_food' : 0.37,   # target efficiency improvement across all activities of food industry
                 'mtg_bulk_chemicals' : 13   # target efficiency improvement across all bulk chemicals except green ammonia
                 }
Id_mtg_switching = {'mtg_NG_to_H2' : 0.3, # target switching of N2 to H2
                    'mtg_fossilH2_to_renewableH2' : 1} # target implementation of renewable H2 in place of fossil hydrogen

ammonia_ng_frac_for_heatandpower = 0.283 # fraction of natural gas used for heat and power

print("Status: Constructing Industrial sector Mitigation scenario ..")

# Designing mitigation scenarios for paper industry
print("      : Paper Industry")

# Implementing efficiency improvements
mtg_id_paper_ef = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                       (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Paper Industry'), : ],
                                                  'Year', 'Value', trend_start_val=0, trend_end_val=Id_mtg_params['mtg_paper']).copy()
mtg_id_paper_ef['Case'] = 'Mitigation'
mtg_id_paper_ef['Mitigation Case'] = 'Paper Industry, efficiency improvements'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  mtg_id_paper_ef.copy(), save_interim_files)

# Implementing fuel switching, NG to Electricity, after implementing efficiency improvements
mtg_id_paper_fsng = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_paper_fsng = mtg_id_paper_fsng.fillna(value='-')
mtg_id_paper_fsng = mtg_id_paper_fsng.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fsng = \
    ob_utils.fuel_switching(mtg_id_paper_fsng,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['NG_to_Elec'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_paper_fsng['Case'] = 'Mitigation'
mtg_id_paper_fsng['Mitigation Case'] = 'Paper Industry, fuel switching Natural Gas to Electricity'

# Implementing fuel switching, Steam Coal to Electricity, after implementing efficiency improvements
mtg_id_paper_fssc = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
mtg_id_paper_fssc = mtg_id_paper_fssc.fillna(value='-')
mtg_id_paper_fssc = mtg_id_paper_fssc.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fssc = \
    ob_utils.fuel_switching(mtg_id_paper_fssc,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Coal_to_Elec'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_paper_fssc['Case'] = 'Mitigation'
mtg_id_paper_fssc['Mitigation Case'] = 'Paper Industry, fuel switching Steam Coal to Electricity'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_fsng, save_interim_files)
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_fssc, save_interim_files)

# Implementing fuel switching H2 blend to NG
mtg_id_paper_fsngh2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                           (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                           (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_paper_fsngh2 = mtg_id_paper_fsngh2.fillna(value='-')
mtg_id_paper_fsngh2 = mtg_id_paper_fsngh2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fsngh2 = \
    ob_utils.fuel_switching_H2NG(mtg_id_paper_fsngh2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            trend_start_val=0, trend_end_val=Id_mtg_switching['mtg_NG_to_H2'])
mtg_id_paper_fsngh2['Case'] = 'Mitigation'
mtg_id_paper_fsngh2['Mitigation Case'] = 'Paper Industry, fuel switching Natural Gas to Hydrogen'                                    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_fsngh2, save_interim_files)

# Mitigation scenario for switching from fossil H2 and renewable H2
mtg_id_paper_h2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                       (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                       (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                       (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]
mtg_id_paper_h2 = mtg_id_paper_h2.fillna(value='-')
mtg_id_paper_h2 = mtg_id_paper_h2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                           'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                           'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_h2 = \
    ob_utils.fuel_switching(mtg_id_paper_h2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=Id_mtg_switching['mtg_fossilH2_to_renewableH2'])
mtg_id_paper_h2['Case'] = 'Mitigation'
mtg_id_paper_h2['Mitigation Case'] = 'Paper Industry, fuel switching Fossil H2 to renewable H2'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_h2, save_interim_files)    

# Desigining mitigation scenarios for the Food industry

print("      : Food Industry")

# Implementing efficiency improvements
mtg_id_food_ef = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                       (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Food Industry'), : ],
                                                  'Year', 'Value', trend_start_val=0, trend_end_val=Id_mtg_params['mtg_food']).copy()
mtg_id_food_ef['Case'] = 'Mitigation'
mtg_id_food_ef['Mitigation Case'] = 'Food Industry, efficiency improvements'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  mtg_id_food_ef.copy(), save_interim_files)

# Implementing fuel switching, Steam Coal to Natural Gas, after implementing efficiency improvements
mtg_id_food_fssc = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Food Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
mtg_id_food_fssc = mtg_id_food_fssc.fillna(value='-')
mtg_id_food_fssc = mtg_id_food_fssc.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_food_fssc = \
    ob_utils.fuel_switching(mtg_id_food_fssc,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_food_fssc['Case'] = 'Mitigation'
mtg_id_food_fssc['Mitigation Case'] = 'Food Industry, fuel switching Steam Coal to Natural Gas'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_food_fssc, save_interim_files)

# Implementing fuel switching H2 blend to NG
mtg_id_food_fsngh2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                           (activity_ref_mtg['Subsector'] == 'Food Industry') &
                                           (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_food_fsngh2 = mtg_id_food_fsngh2.fillna(value='-')
mtg_id_food_fsngh2 = mtg_id_food_fsngh2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
mtg_id_food_fsngh2 = \
    ob_utils.fuel_switching_H2NG(mtg_id_food_fsngh2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            trend_start_val=0, trend_end_val=Id_mtg_switching['mtg_NG_to_H2'])
mtg_id_food_fsngh2['Case'] = 'Mitigation'
mtg_id_food_fsngh2['Mitigation Case'] = 'Food Industry, fuel switching Natural Gas to Hydrogen'                                    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_food_fsngh2, save_interim_files)

# Mitigation scenario for switching from fossil H2 and renewable H2
mtg_id_food_h2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                       (activity_ref_mtg['Subsector'] == 'Food Industry') &
                                       (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                       (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]
mtg_id_food_h2 = mtg_id_food_h2.fillna(value='-')
mtg_id_food_h2 = mtg_id_food_h2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                           'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                           'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_food_h2 = \
    ob_utils.fuel_switching(mtg_id_food_h2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=Id_mtg_switching['mtg_fossilH2_to_renewableH2'])
mtg_id_food_h2['Case'] = 'Mitigation'
mtg_id_food_h2['Mitigation Case'] = 'Food Industry, fuel switching Fossil H2 to renewable H2'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_food_h2, save_interim_files)    


# Design mitigation scenarios for Ammonia industry based on GHGI data

print("      : Ammonia Industry")

# combustion emissions

# unit conversion for file loaded values
bulk_chem.loc[ : , ['activity_unit', 'activity_value']] = \
  ob_units.unit_convert_df(bulk_chem.loc[ : , ['activity_unit', 'activity_value']],
   Unit = 'activity_unit', Value = 'activity_value')
 
# Expand data to all years
bulk_chem['Year'] = decarb_year_min
bulk_chem_exp = bulk_chem.copy()
for yr in range(decarb_year_min+1, decarb_year_max+1): # [a,)
    bulk_chem['Year'] = yr
    bulk_chem_exp = pd.concat ([bulk_chem_exp, bulk_chem], axis=0).copy().reset_index(drop=True)

# Create mitigation scenarios for Green ammonia
bulk_chem_amm = bulk_chem_exp.loc[bulk_chem_exp['Type'].isin(['Conventional Ammonia', 'Green Ammonia']), : ].copy()
        
# Scale the activity based on increase in shipment over the years
bulk_chem_amm = pd.merge(bulk_chem_amm, ob_eia.EIA_data['chemical_industry_supp']. \
                         loc[ob_eia.EIA_data['chemical_industry_supp']['Parameter'] == 'Ammonia Production', ['Year', 'frac_increase']].drop_duplicates(),
                         how='left',
                         on=['Year']).reset_index(drop=True)

bulk_chem_amm['activity_value'] = bulk_chem_amm['activity_value'] * bulk_chem_amm['frac_increase']

bulk_green_amm = bulk_chem_amm.loc[bulk_chem_amm['Type']== 'Green Ammonia', : ].copy()
bulk_conv_amm = bulk_chem_amm.loc[bulk_chem_amm['Type']== 'Conventional Ammonia', : ].copy()

# Trend for Green ammonia implementation over years as mitigation scenarios
ob_utils.model_2d_ammonia() # model run
bulk_green_amm['mtg_frac'] = [ob_utils.trend_2d_ammonia(x) for x in bulk_green_amm['Year']] # model predict

bulk_green_amm['activity_value'] = bulk_green_amm['activity_value'] * bulk_green_amm['mtg_frac']

bulk_green_amm['Value'] = bulk_green_amm['activity_value'] * bulk_green_amm['energy_value'] # absolute amount of green ammonia coming online

bulk_conv_amm = pd.merge(bulk_green_amm, 
                         bulk_conv_amm[['Year', 'End Use Application', 'Energy carrier', 'Energy carrier type', 'energy_value']],
                         how='left',
                         on=['Year', 'End Use Application', 'Energy carrier', 'Energy carrier type']).reset_index(drop=True)
bulk_conv_amm['Value'] = -1 * bulk_conv_amm['activity_value'] * bulk_conv_amm['energy_value_y'] # absolute amount of conventional ammonia going offline

colnames = ['Mitigation Case', 'Sector', 'Subsector', 'Data Source', 
            'End Use Application', 'Energy carrier', 'Energy carrier type', 
            'Year', 'energy_unit_numerator', 'Value']
bulk_conv_amm['Mitigation Case'] = 'Bulk Chenical Industry, Green Ammonia, removal of conventional ammonia'
bulk_green_amm['Mitigation Case'] = 'Bulk Chenical Industry, Green Ammonia'

bulk_chem_amm = pd.concat([bulk_conv_amm[colnames], bulk_green_amm[colnames]], axis=0).reset_index(drop=True)

bulk_chem_amm['Case'] = 'Mitigation'

bulk_chem_amm.loc[bulk_chem_amm['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
bulk_chem_amm.loc[bulk_chem_amm['Energy carrier'] == 'Natural Gas', 'Scope'] = 'Direct, Combustion'

bulk_chem_amm[['AEO Case',
              'Generation Type',
              'Fuel Pool',
              'Basis']] = '-'

bulk_chem_amm.rename(columns={'energy_unit_numerator' : 'Unit'}, inplace=True)

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_amm, save_interim_files) 

# Implementing efficiency improvement

# Firstly, get the activity for bulk chemical industries, excluding green ammonia only, but include reduction in conventional ammonia
bulk_chem_ef = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_ef = bulk_chem_ef.loc[bulk_chem_ef['Mitigation Case'] != 'Bulk Chenical Industry, Green Ammonia', : ]
bulk_chem_ef = bulk_chem_ef.fillna(value='-')
bulk_chem_ef = bulk_chem_ef.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
bulk_chem_ef = ob_utils.efficiency_improvement(bulk_chem_ef, 'Year', 'Value', trend_start_val=0, trend_end_val=Id_mtg_params['mtg_bulk_chemicals']).copy()
bulk_chem_ef['Case'] = 'Mitigation'
bulk_chem_ef['Mitigation Case'] = 'Bulk Chemical Industry, efficiency improvements'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_ef, save_interim_files) 

# Implement Fuel Switching {all} to Electricity for 61% (process heating) x 30% (low quality heat) of all fuel uses (except green ammonia) to Electricity
bulk_chem_fs = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_fs = bulk_chem_fs.loc[bulk_chem_fs['Mitigation Case'] != 'Bulk Chenical Industry, Green Ammonia', : ]
bulk_chem_fs = bulk_chem_fs.fillna(value='-')
bulk_chem_fs = bulk_chem_fs.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
# declaring low quality process heat
bulk_chem_fs['Value'] = bulk_chem_fs['Value'] * 0.61 * 0.30
# Fuel switching
# Identify all the unique fuels to switch to electricity
# Perform switching
fuels =  bulk_chem_fs['Energy carrier'].unique()   

bulk_chem_fs_mtg = \
pd.concat([
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Natural Gas', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['NG_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Diesel', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Diesel_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Other Petroleum', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Other_Petroleum_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Petroleum Coke', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Petroleum_Coke_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Propane', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Propane_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Residual Fuel Oil', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Residual_fuel_oil_to_Elec'], 
                        trend_start_val=0, trend_end_val=1),
ob_utils.fuel_switching(bulk_chem_fs.loc[bulk_chem_fs['Energy carrier'] == 'Steam Coal', : ],
                        'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                        'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Coal_to_Elec'], 
                        trend_start_val=0, trend_end_val=1)
])

bulk_chem_fs_mtg['Case'] = 'Mitigation'
bulk_chem_fs_mtg['Mitigation Case'] = 'Bulk Chemical Industry, fuel switching {all} to Electricity'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_fs_mtg, save_interim_files) 

# Fuel Switching, remaining Steam Coal to NG
bulk_chem_fs_mtg = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                        (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_fs_mtg = bulk_chem_fs_mtg.fillna(value='-')
bulk_chem_fs_mtg = bulk_chem_fs_mtg.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                             'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                             'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
bulk_chem_fs_mtg = ob_utils.fuel_switching(bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] == 'Steam Coal', : ],
                                           'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                                           'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                                           trend_start_val=0, trend_end_val=1)
bulk_chem_fs_mtg['Case'] = 'Mitigation'
bulk_chem_fs_mtg['Mitigation Case'] = 'Bulk Chemical Industry, fuel switching Steam Coal to Natural Gas'   

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_fs_mtg, save_interim_files)                      

# non-combustion emissions
ghgi_mtg_am = ob_EPA_GHGI.activity_non_combust_exp.loc[(ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Industrial') & 
                                                       (ob_EPA_GHGI.activity_non_combust_exp['Subsector'] == 'Bulk Chemical Industry') & 
                                                       (ob_EPA_GHGI.activity_non_combust_exp['End Use Application'] == 'Ammonia Production'), :].copy()

ghgi_mtg_am['mtg_frac'] = [ob_utils.trend_2d_ammonia(x) for x in ghgi_mtg_am['Year']]

ghgi_mtg_am['Total Emissions'] = -1 * ghgi_mtg_am['Total Emissions'] * ghgi_mtg_am['mtg_frac'] # reduction in GHGI emissions due to ammonia production

ghgi_mtg_am['Case'] = 'Mitigation'
ghgi_mtg_am['Mitigation Case'] = 'Bulk Chenical Industry, Green Ammonia'
ghgi_mtg_am['Scope'] = 'Direct, Non-Combustion'

"""
# Designing mitigation scenarios for the bulk chemical industry
mtg_id_chem = activity_mtg_id.loc[activity_mtg_id['Subsector'] == 'Bulk Chemical Industry', : ].copy()

mtg_id_chem['Mitigation Case'] = 'Bulk Chemical Industry, fuel switching and efficiency improvements'

# Designing mitigation scenarios for the refining industry
mtg_id_refi = activity_mtg_id.loc[activity_mtg_id['Subsector'] == 'Refining Industry', : ].copy()

mtg_id_refi['Mitigation Case'] = 'Refining Industry, fuel switching and efficiency improvements'

# Defining mitigation scenarios for the cement and lime industry
mtg_id_cheli = activity_mtg_id.loc[activity_mtg_id['Subsector'] == 'Cement and Lime Industry', : ].copy()

mtg_id_cheli['Mitigation Case'] = 'Cement and Lime Industry, fuel switching and efficiency improvements'

# Defining mitigation scenarios for the iron and steel industry
mtg_id_iron = activity_mtg_id.loc[activity_mtg_id['Subsector'] == 'Iron and Steel Industry', : ].copy()

mtg_id_iron['Mitigation Case'] = 'Iron and Steel Industry, fuel switching and efficiency improvements'

# Defining mitigation scenarios for all other industries
mtg_id_oth = activity_mtg_id.loc[~(activity_mtg_id['Subsector'].\
                                   isin(['Paper Industry', 'Food Industry', 'Bulk Chemical Industry', 
                                         'Refining Industry', 'Cement and Lime Industry', 'Iron and Steel Industry'])), : ]
"""

# Seperate electric and non-electric activities
activity_mtg_id = activity_ref_mtg.loc[(activity_ref_mtg['Case'] == 'Mitigation') &
                                       (activity_ref_mtg['Sector'] == 'Industrial'), : ]
activity_mtg_id_elec = activity_mtg_id.loc[activity_mtg_id['Energy carrier'] == 'Electricity', : ]
activity_mtg_id = activity_mtg_id.loc[~(activity_mtg_id['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_id = pd.merge(activity_mtg_id, corr_EF_GREET.loc[corr_EF_GREET['Scope'] == 'Direct, Combustion', :], how='left', 
                               on=['Sector', 'Scope', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_id = pd.merge(activity_mtg_id, ob_ef.ef_raw, 
                           how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to VISION
activity_mtg_id_elec = pd.merge(activity_mtg_id_elec, 
                                   elec_gen_em_mtg_agg_m[['Flow Name', 'Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                                   how='left',
                                   on=['Year'])
activity_mtg_id_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)

activity_mtg_id.rename(columns={'Unit (Numerator)' : 'Emissions Unit',
                               'Unit (Denominator)' : 'Energy Unit',
                               'Reference case' : 'CI'}, inplace=True)
activity_mtg_id.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

# Concatenate electric and non-electric activities
activity_mtg_id = pd.concat([activity_mtg_id, activity_mtg_id_elec], axis = 0).reset_index(drop=True)

activity_mtg_id['Total Emissions'] = activity_mtg_id['Value'] * activity_mtg_id['CI']

# Concatenate non-combustion mitigation scope for ammonia industry
activity_mtg_id = pd.concat([activity_mtg_id, ghgi_mtg_am], axis=0).reset_index(drop=True)

# Calculate LCIA metric
activity_mtg_id = pd.merge(activity_mtg_id, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_id['LCIA_estimate'] = activity_mtg_id['Total Emissions'] * activity_mtg_id['GWP']

# unit conversions
activity_mtg_id.loc[~activity_mtg_id['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_id.loc[~activity_mtg_id['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_mtg_id = pd.merge(activity_mtg_id, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
  
# Create rest of the empty columns
activity_mtg_id [ list(( Counter(activity_BAU.columns) - Counter(activity_mtg_id.columns )).elements()) ] = '-'

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_id], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( 'Elapsed time: ' + str(datetime.now() - init_time))


#%%
"""
Generating mitigation scenarios for the Other sectors including other industries
"""

print("Status: Constructing Other sectors' Mitigation scenario ..")




#%%
"""
Mitigation scenario of replacing natural gas based Hydrogen to other feedstock or renewable hydrogen
"""
