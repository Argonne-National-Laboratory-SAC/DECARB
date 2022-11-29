# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 

Created on Mon Jan 10 20:08:36 2022

@authors: Saurajyoti Kar and Greg Zaimes
"""

#%%
# Analysis parameters

# Update the _prefix paths based on your local Box folder location

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # psth to the Github local repository

input_path_prefix = code_path_prefix + '\\Data\\1_input_files'
interim_path_prefix = code_path_prefix + '\\Data\\2_intermediate_files'
output_path_prefix = code_path_prefix + '\\Data\\3_output_files'

# Declaring paths for data loading
input_path_params = input_path_prefix + '\\Parameters'
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
input_path_biofuels = input_path_prefix + '\\Biofuels'

# Load Input parameters
f_input_params = 'input_vals.csv'

# LCIA factors
f_lcia = 'gwp factors.xlsx'
f_lcia_sheet = 'Tidy'

# Non energy use EFs file name
f_neu = 'neu_efs.xlsx'
sheet_neu = 'Sheet1'

# Declaring correlation filenames
f_eia = 'EIA Dataset.csv'
f_NREL_elec_option = 'report - All Options EFS.xlsx'

#_biofuel_decarb = 'DECARB Biofuel Mitigation.csv'

f_corr_ef_greet = 'corr_EF_GREET.xlsx'
sheet_corr_ef_greet = 'corr_EF_GREET'

f_corr_ef_greet_supply_chain = 'corr_EF_GREET_SUPPLY_CHAIN.csv'
#sheet_corr_ef_greet_supply_chain = 'corr_EF_GREET'

f_ef_greet_supply_chain = 'GREET_EF_SUPPLY_CHAIN.csv'
#sheet_ef_greet_supply_chain = 'EF_GREET_SUPPLY_CHAIN'

f_corr_EIA_SCOUT = 'corr_EERE_SCOUT.xlsx'
sheet_corr_EIA_SCOUT = 'Mapping EIA_to_Scout'

f_corr_ghgs = 'corr_ghgi_emissions_categories.csv'

f_corr_ghgi_sources_EERE = 'corr_ghgi_sources_EERE.csv'
f_corr_carbon_content_biofuels = 'corr_carbon_content_biofuels.csv'

# defining the intermediate and final data table files and their columns
f_interim_activity = 'interim_activity_ref_mtg_cases.csv'
f_interim_env = 'interim_env_ref_mtg_cases.csv'
f_out_activity = 'activity_ref_mtg_cases.csv'
f_out_env = 'env_ref_mtg_cases.csv'
f_elec_net_gen = 'interim_elec_gen.csv'
f_elec_env = 'interim_elec_gen_env.csv'
f_elec_env_agg = 'interim_elec_gen_env_agg.csv'
f_elec_CI = 'interim_elec_gen_CI.csv'
f_industrial_energy = 'industrial_activity_energy.csv'
f_industrial_quantity = 'industrial_activity_quantity.csv'
f_biofuels = 'biofuels.csv'

cols_activity_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Unit', 'Value']

cols_env_out = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Scope', 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Formula', 'Emissions Category, Detailed', 'Emissions Category, Aggregate',
                'Emissions Unit', 'Total Emissions', 'LCIA_estimate']

cols_elec_net_gen = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                     'Energy carrier', 'Energy carrier type', 'Generation Type', 'Year',
                     'Energy Unit', 'Electricity Production']

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
#LCIA_Method = 'AR4' # QA can use AR4, but model should be based on AR5
#lcia_timeframe = 100

# EIA AEO data cases
#EIA_AEO_case_option = ['Reference case']

# Mitigation scenario design and target parameters
#Ag_mtg_params = {'D2E_mtg_2050' : 1.0, # targetted Diesel to Electricity use ratio in 2050 year
#                 'D2E_relative_eff' : 0.40/0.90, # The relative efficiency of directly using Diesel compared to directly using Electricity. Considering 40% energy from diesel used into activity and 90% electricity energy used into activity
#                 'manure_mgmt' : 1.0, # Target percentage of reduced GHG emissions from manure management activities. Ag / Anaerobic Digestion / Manure MGMT / CH4, N2O
#                 'soil_N2O' : 1.0, # Target percentage of reduced GHG emissions from precisiion farming activitis. Ag / Precision Farming / Soil N2O / N2O
#                 'rice_cultv' : 1.0 # Target percentage of reduced GHG emissions from rice cultivation. Ag / Improved Water and Residue MGMT / Rice Cultivation / CH4
#                }

# T&D assumption, constant or calculated
# T_and_D_loss_constant = True
# T_and_D_loss = 0.06

# parameter to print out additional information when code is running
verbose = True

#%%

# import packages
import pandas as pd
import numpy as np
import os
from datetime import datetime
from collections import Counter

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
from CCS_implementation import CCS_implementation


#%%

# Loading in import values
input_params = pd.read_csv(input_path_params + '\\' + f_input_params, header = 3).drop('Description', axis=1)
input_params = input_params.set_index('Parameter Name')['Value'].to_dict()
for param in input_params: 
    try: 
        input_params[param] = float(input_params[param])
    except: 
        continue

# Utility functions

def save_activity_mx (df_to, df, save_interim_files):    
    df_to = pd.concat([df_to.copy(), df.copy()], axis=0).reset_index(drop=True)

    if save_interim_files == True:
        df_to.to_csv(interim_path_prefix + '\\' + f_interim_activity)
        df_to[cols_activity_out].to_csv(output_path_prefix + '\\' + f_out_activity)
        
    return df_to.copy()

# Calculate emission factors for lime production
# Calculation from pg. 271 of EPA GHGI Inventory of Greenhouse Gas Emissions and Sinks: 1990-2019
def calc_ef_clinker (frac_CaO = 0.650) :
    # Formula: EF_clinker = 0.650 CaO × [(44.01 g/mole CO2) ÷ (56.08 g/mole CaO)] = 0.510 tons CO2/ton clinker    
    return  frac_CaO * 44.01 /56.08 # metric ton CO2 per metric ton clinker production

def calc_high_calcium_lime ():
    # [(44.01 g/mole CO2) ÷ (56.08 g/mole CaO)] × (0.9500 CaO/lime) = 0.7455 g CO2/g lime
    return 0.7455 # metric ton CO2 per metric ton high calcium lime

def calc_dolomitic_lime ():
    # [(88.02 g/mole CO2) ÷ (96.39 g/mole CaO)] × (0.9500 CaO/lime) = 0.8675 g CO2/g lime
    return 0.8675 # metric ton CO2 per metric ton dolomitic lime

#%%

init_time = datetime.now()

# Create data class objects

# Import GREET Supply Chain EF's and Correspondence files
corr_ef_greet_supply_chain = pd.read_csv(input_path_corr + '\\' + f_corr_ef_greet_supply_chain,
                                           header = 3) 

ef_greet_supply_chain = pd.read_csv(input_path_GREET + '\\' + f_ef_greet_supply_chain,
                                      header = 3)

# Unit conversion class object
ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)

# Utilities class object
ob_utils = Utilities()

# CCS implementation class
ob_ccs = CCS_implementation(input_path_prefix)

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

# Import Biofuel Supply Data
biofuel = pd.read_csv(input_path_biofuels + '\\' + f_biofuels)

# GREET emission factor load
ob_ef = GREET_EF(input_path_GREET )
                      
# Data tables for correspondence across data sets
corr_EF_GREET = pd.read_excel(input_path_corr + '\\' + f_corr_ef_greet, sheet_name = sheet_corr_ef_greet, header = 3)
corr_EIA_SCOUT = pd.read_excel(input_path_corr + '\\' + f_corr_EIA_SCOUT, sheet_name = sheet_corr_EIA_SCOUT, header = 3, index_col=None)
corr_ghgs = pd.read_csv(input_path_corr + '\\' + f_corr_ghgs, header = 3, index_col=None)
corr_ghgi_sources_EERE = pd.read_csv(input_path_corr + '\\' + f_corr_ghgi_sources_EERE, header = 3, index_col=None)
corr_carbon_content_biofuels = pd.read_csv(input_path_corr + '\\' + f_corr_carbon_content_biofuels, header = 3, index_col=None)

# Life Cycle Impact Assessment metrics table
lcia_data = pd.read_excel(input_path_EPA + '\\' + f_lcia, sheet_name = f_lcia_sheet)         
lcia_select = lcia_data.loc[ (lcia_data['LCIA Method'] == input_params["LCIA_Method"]) & (lcia_data['timeframe_years'] == input_params["lcia_timeframe"]) ]

# Loading Non-energy use EFs
neu_EF_GREET = pd.read_excel(input_path_neu + '\\' + f_neu, sheet_name = sheet_neu, header = 3)

# Loading industrial data for constructing mitigation scenarios 
id_quantity = pd.read_csv(input_path_EPA + '\\' + f_industrial_quantity)
id_energy = pd.read_csv(input_path_EPA + '\\' + f_industrial_energy)
id_quantity.drop(columns=['Table'], inplace=True)
id_energy.drop(columns=['notes'], inplace=True)

# Loading biofuels mitigation data
#mtg_biofuel = pd.read_csv(input_path_biofuel + '\\' + f_biofuel_decarb)

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
ob_ef.ef = pd.merge(corr_EF_GREET.loc[ :, ~(corr_EF_GREET.columns.isin(['GREET Tab', 'GREET Version'])) ],
                    ob_ef.ef,
                    how='left',on=['GREET Pathway', 'Scope']).reset_index(drop=True)

# Filter combustion data for electricity generation 
ob_ef.ef_electric = ob_ef.ef.loc[ob_ef.ef['Scope'].isin(['Electricity, Combustion'])].copy()

ob_ef.ef_electric.rename(columns = {'Unit (Numerator)' : 'EF_Unit (Numerator)',
                                    'Unit (Denominator)' : 'EF_Unit (Denominator)'}, inplace = True)                

# Calculate aggregrated electricity generation and merge T&D loss
# Two data frames, electric_gen_interim and electric_gen created to group by separately for output files
electric_gen_interim = ob_eia.EIA_data['energy_supply'].groupby(['Year', 'Sector', 'End Use', 'Energy carrier', 
                                                                 'Energy carrier type', 'Generation Type', 'Unit']).\
                                                agg({'Value' : 'sum'}).reset_index().\
                                                rename(columns = {'Value' : 'Electricity Production'})
electric_gen_interim = pd.merge(electric_gen_interim, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
electric_gen_interim['Electricity Production'] = electric_gen_interim['Electricity Production'] * (1 - electric_gen_interim['loss_frac'])
electric_gen_interim.rename(columns={'End Use' : 'End Use Application',
                                     'Unit' : 'Energy Unit'}, inplace=True)
electric_gen_interim['Case'] = 'Reference case'
electric_gen_interim[['Mitigation Case', 'Subsector']] = '-'

if save_interim_files == True:
    electric_gen_interim[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)

electric_gen = ob_eia.EIA_data['energy_supply'].groupby(['Year', 'Sector', 'End Use', 'Energy carrier', 'Unit']).\
                                                agg({'Value' : 'sum'}).reset_index().\
                                                rename(columns = {'Value' : 'Electricity Production'})
electric_gen = pd.merge(electric_gen, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
electric_gen['Electricity Production'] = electric_gen['Electricity Production'] * (1 - electric_gen['loss_frac'])
electric_gen.rename(columns={'End Use' : 'End Use Application'}, inplace=True)
electric_gen['Case'] = 'Reference case'
electric_gen[['Mitigation Case', 'Subsector']] = '-'

# Calculate Total emissions
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
electric_gen_ef_agg = electric_gen_ef.groupby(['Year', 'Sector', 'Formula', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   

electric_gen_ef_agg['End Use Application'] = 'Electricity Generation'
electric_gen_ef_agg['Energy carrier'] = 'Electricity'                                                
electric_gen_ef_agg['Case'] = 'Reference case'
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
elec_gen_em_agg['Subsector'] = 'Electric Power Sector'

elec_gen_em_agg = elec_gen_em_agg.groupby(['Case', 'Mitigation Case', 'Sector', 'End Use Application',
                                           'Energy carrier', 'Formula', 
                                           'Year', 'Energy Unit', 'Emissions Unit']).agg({'Total Emissions' : 'sum',
                                                                           'Electricity Production' : 'sum'}).reset_index()

elec_gen_em_agg['CI'] = elec_gen_em_agg['Total Emissions'] / elec_gen_em_agg['Electricity Production']
elec_gen_em_agg['Mitigation Case'] = '-'

if save_interim_files == True:
    tempdf = elec_gen_em_agg[cols_elec_CI].copy()    
    tempdf = pd.merge(tempdf, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
    tempdf['LCIA_estimate'] = tempdf['CI'] * tempdf['GWP']
    tempdf.to_csv(interim_path_prefix + '\\' + f_elec_CI)
    del tempdf

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

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%

"""
Generating Electric power mitigation scenarios
"""

print("Status: Constructing Electric generation Mitigation scenario ..")

elec_gen_mtg = ob_elec.NREL_elec['generation'].\
    groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case',
             'Generation Type','Year', 'Energy carrier', 
             'Energy carrier type', 'Energy Unit']). \
    agg({'Electricity Production' : 'sum'}).reset_index()

elec_gen_mtg

# T&D loss
elec_gen_mtg = pd.merge(elec_gen_mtg, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year').reset_index(drop=True)
elec_gen_mtg['Electricity Production'] = elec_gen_mtg['Electricity Production'] * (1 - elec_gen_mtg['loss_frac'])
elec_gen_mtg.drop(columns=['loss_frac'], inplace=True)

# Separate grouping variables for saving 
tempdf = ob_elec.NREL_elec['generation'].\
         groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 
                  'Energy carrier', 'Energy carrier type', 'Generation Type',
                  'Energy Unit']). \
         agg({'Electricity Production' : 'sum'}).reset_index()
tempdf = pd.merge(tempdf, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year').reset_index(drop=True)
tempdf['Electricity Production'] = tempdf['Electricity Production'] * (1 - tempdf['loss_frac'])
tempdf.drop(columns=['loss_frac'], inplace=True)
electric_gen_interim = pd.concat([electric_gen_interim, tempdf], axis = 0).reset_index(drop=True)

if save_interim_files == True:
    electric_gen_interim[cols_elec_net_gen].to_csv(interim_path_prefix + '\\' + f_elec_net_gen)
del tempdf

# Merge emission factors with net electricity generation
elec_gen_ef_mtg = pd.merge(elec_gen_mtg,
                           ob_ef.ef_electric, 
                           how='left',
                           on=['Sector', 'Subsector', 'Case', 'Year', 'Energy carrier', 'Energy carrier type']).reset_index(drop=True)

# Calculate net emission by GHG species, from electricity generation    
elec_gen_ef_mtg['Total Emissions'] = elec_gen_ef_mtg['Reference case'] * elec_gen_ef_mtg['Electricity Production'] 

# Rename and re-arrange columns
elec_gen_ef_mtg.rename(columns={'Reference case' : 'EF_withElec',
                                'Elec0' : 'EF_Elec0'}, inplace = True)
elec_gen_ef_mtg[['Basis',
                 'Fuel Pool']] = '-'

# adding non-combustion emissions
tempdf = ob_EPA_GHGI.activity_elec_non_combust_exp.copy()
tempdf['Case'] = 'Mitigation'
tempdf['EF_Elec0'] = '-'
tempdf = tempdf[elec_gen_ef_mtg.columns]
elec_gen_ef_mtg = pd.concat([elec_gen_ef_mtg, tempdf], axis=0).reset_index(drop=True)
del tempdf

tempdf = elec_gen_ef_mtg.copy()
tempdf = pd.merge(tempdf, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
electric_gen_ef = pd.concat([electric_gen_ef, tempdf[cols_elec_env] ], axis=0).reset_index(drop=True)

# Save electric gen environmental matrix
if save_interim_files == True:
    electric_gen_ef.to_csv(interim_path_prefix + '\\' + f_elec_env)

del tempdf
        
# Aggregrate emissions
electric_gen_ef_mtg_agg = elec_gen_ef_mtg.groupby(['Case', 'Sector', 'Formula', 
                                                   'Year', 'EF_Unit (Numerator)']).agg({'Total Emissions' : 'sum'}).reset_index() 
electric_gen_ef_mtg_agg['End Use Application'] = 'Electricity Generation'
electric_gen_ef_mtg_agg['Energy carrier'] = 'Electricity'
electric_gen_ef_mtg_agg['Subsector'] = 'Electric Power Sector'
electric_gen_ef_mtg_agg['Mitigation Case'] = 'NREL Electric Power Decarb'

electric_gen_ef_agg = pd.concat([electric_gen_ef_agg, electric_gen_ef_mtg_agg[cols_elec_env_agg]], axis=0).reset_index(drop=True)                                               

if save_interim_files == True:    
    electric_gen_ef_agg.to_csv(interim_path_prefix + '\\' + f_elec_env_agg)
 
# Calculate total emissions 
elec_gen_mtg = elec_gen_mtg.groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Energy carrier', 
                                     'Year', 'Energy Unit']).agg({'Electricity Production' : 'sum'}).reset_index()
elec_gen_em_mtg_agg = pd.merge(elec_gen_mtg, electric_gen_ef_mtg_agg, how='left', on=['Sector', 'Subsector', 'Case', 
                                                                                      'Year', 'Energy carrier']).\
                      reset_index(drop=True)

elec_gen_em_mtg_agg.rename(columns={
    'Unit' : 'Energy Unit', 
    'EF_Unit (Numerator)' : 'Emissions Unit',
    'Mitigation Case_x' : 'Mitigation Case'}, inplace=True)
elec_gen_em_mtg_agg.drop(columns=['Mitigation Case_y'], inplace=True)

elec_gen_em_mtg_agg['CI'] = elec_gen_em_mtg_agg['Total Emissions'] / elec_gen_em_mtg_agg['Electricity Production']

elec_gen_em_agg = pd.concat([elec_gen_em_agg, elec_gen_em_mtg_agg], axis=0).reset_index(drop=True)

if save_interim_files == True:
    tempdf = elec_gen_em_agg[cols_elec_CI].copy()    
    tempdf = pd.merge(tempdf, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
    tempdf['LCIA_estimate'] = tempdf['CI'] * tempdf['GWP']
    tempdf.to_csv(interim_path_prefix + '\\' + f_elec_CI)

# constructing the Electricity mitigation matrix calculating difference in Electricity grid CIs

tempdf = elec_gen_em_agg.loc[elec_gen_em_agg['Case'] == 'Reference case', : ][['Sector', 'End Use Application', 'Year', 
                                                                               'Energy carrier', 'Formula', 'Energy Unit', 'Emissions Unit',
                                                                               'Total Emissions', 'Electricity Production', 'CI']]
elec_gen_em_mtg_agg_m = pd.merge(tempdf, elec_gen_em_mtg_agg[['Case', 'Mitigation Case', 'Year', 'Formula', 'Energy Unit', 'Emissions Unit', 'Total Emissions', 'Electricity Production', 'CI']], 
                                 how='left', on = ['Year', 'Formula', 'Energy Unit', 'Emissions Unit'] ).reset_index(drop=True)
del tempdf

elec_gen_em_mtg_agg_m.rename(columns={'Case_y' : 'Case',
                                      'Mitigation Case_y' : 'Mitigation Case',
                                      'CI_x' : 'CI_ref_case_elec', 
                                      'CI_y' : 'CI_elec_mtg',
                                      'Total Emissions_x' : 'Total Emissions_ref_case',
                                      'Total Emissions_y' : 'Total Emissions_mtg_elec',
                                      'Electricity Production_x' : 'Electricity Production_ref_case',
                                      'Electricity Production_y' : 'Electricity Production_mtg_elec'}, inplace=True)

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

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for Residential and Commercial sectors with SCOUT Model
"""

print("Status: Constructing Residential and Commercial sectors Mitigation scenario ..")

# Creating activity data table for both reference case and SCOUT mitigation case
activity_ref_mtg = ob_eia.EIA_data['energy_demand'].copy()
activity_ref_mtg.loc[activity_ref_mtg['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion' 
activity_ref_mtg.loc[activity_ref_mtg['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion' 
activity_ref_mtg['Mitigation Case'] = '-'

ob_scout = SCOUT(ob_units, input_path_SCOUT, input_path_corr)

activity_mtg_scout = ob_scout.df_scout.copy()

# Concatenate to activity data frame and save
temp = activity_mtg_scout.copy()
temp[['AEO Case', 'Basis', 'Generation Type', 'Fuel Pool']] = '-'
temp = temp[['Data Source', 'AEO Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 'Scope',
              'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
              'Value', 'Case', 'Generation Type', 'Fuel Pool']]
activity_ref_mtg = save_activity_mx(activity_ref_mtg, temp.copy(), save_interim_files)
del temp

# Separate electric and non electric activities
activity_mtg_scout_elec = activity_mtg_scout.loc[activity_mtg_scout['Energy carrier'] == 'Electricity', : ]
activity_mtg_scout = activity_mtg_scout.loc[~(activity_mtg_scout['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_scout = pd.merge(activity_mtg_scout, corr_EF_GREET, how='left', 
                             on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                 'End Use Application']).reset_index(drop=True)
activity_mtg_scout.drop(columns=['Scope_y'], inplace=True)
activity_mtg_scout.rename(columns={'Scope_x' : 'Scope'}, inplace=True)

# Merge GREET EF
activity_mtg_scout = pd.merge(activity_mtg_scout, ob_ef.ef_raw, 
                             how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to SCOUT
activity_mtg_scout_elec = pd.merge(activity_mtg_scout_elec, 
                                   elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
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

# GGZ: Maping Energy Demand Matrix so that the flows use the SCOUT conventions.

activity_ref_mtg = pd.merge(activity_ref_mtg, 
         corr_EIA_SCOUT[['Sector', 'Subsector', 'EIA: End Use Application', 'SCOUT: End Use Application', 
                         'EIA: Energy carrier', 'EIA: Energy carrier type', 'Energy carrier', 'Energy carrier type']].drop_duplicates(), 
         how='left', 
         left_on=['Sector', 'Subsector', 'End Use Application', 'Energy carrier', 'Energy carrier type'], 
         right_on=['Sector', 'Subsector', 'EIA: End Use Application', 'EIA: Energy carrier', 'EIA: Energy carrier type'])

activity_ref_mtg.loc[activity_ref_mtg['SCOUT: End Use Application'].notnull(),'End Use Application'] = activity_ref_mtg.loc[activity_ref_mtg['SCOUT: End Use Application'].notnull(),'SCOUT: End Use Application']
activity_ref_mtg.loc[activity_ref_mtg['Energy carrier_y'].notnull(),'Energy carrier_x'] = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier_y'].notnull(),'Energy carrier_y']
activity_ref_mtg.loc[activity_ref_mtg['Energy carrier type_y'].notnull(),'Energy carrier type_x'] = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier type_y'].notnull(),'Energy carrier type_y']

activity_ref_mtg = activity_ref_mtg.drop(columns = {'EIA: End Use Application',
       'SCOUT: End Use Application', 'EIA: Energy carrier',
       'EIA: Energy carrier type', 'Energy carrier_y',
       'Energy carrier type_y'})

activity_ref_mtg = activity_ref_mtg.rename(columns = {'Energy carrier_x': 'Energy carrier',
                         'Energy carrier type_x': 'Energy carrier type'})

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for Transportation sector with VISION/Tempo Models
"""

print("Status: Constructing Transportation sector Mitigation scenario ..")

activity_mtg_vision = ob_VISION.vision.copy()

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
activity_mtg_vision['Mitigation Case'] = 'Transportation, VISION scenarios'
activity_mtg_vision.loc[activity_mtg_vision['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
activity_mtg_vision.loc[activity_mtg_vision['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'
activity_mtg_vision = activity_mtg_vision[temp_activity.columns]

# save to activity matrix
activity_ref_mtg = save_activity_mx(activity_ref_mtg, activity_mtg_vision.copy(), save_interim_files)
  
del temp_activity

# Seperate electric and non-electric activities
activity_mtg_vision_elec = activity_mtg_vision.loc[activity_mtg_vision['Energy carrier'] == 'Electricity', : ]
activity_mtg_vision = activity_mtg_vision.loc[~(activity_mtg_vision['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_vision = pd.merge(activity_mtg_vision, corr_EF_GREET, how='left', 
                               on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application', 'Scope']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_vision = pd.merge(activity_mtg_vision, ob_ef.ef_raw, 
                               how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to VISION
activity_mtg_vision_elec = pd.merge(activity_mtg_vision_elec, 
                                   elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
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

print( '    Elapsed time: ' + str(datetime.now() - init_time))

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
mtg_ag_df = ob_utils.trend_linear(activity_mtg_ag[['Year']], 'Year', 0, input_params['Ag_D2E_mtg_2050'])

activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, mtg_ag_df, how='left', on='Year').reset_index(drop=True)

# Identifying the amount of diesel use and electricity use
activity_mtg_ag_d['Value Elec Use'] = activity_mtg_ag_d['Value'] * activity_mtg_ag_d['mtg_frac'] * input_params['Ag_D2E_relative_eff']
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
activity_mtg_ag_d.loc[activity_mtg_ag_d['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
activity_mtg_ag_d.loc[activity_mtg_ag_d['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  activity_mtg_ag_d.copy(), save_interim_files)

# Seperate electric and non-electric activities
activity_mtg_ag_d_elec = activity_mtg_ag_d.loc[activity_mtg_ag_d['Energy carrier'] == 'Electricity', : ]
activity_mtg_ag_d = activity_mtg_ag_d.loc[~(activity_mtg_ag_d['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, corr_EF_GREET, how='left', 
                               on=['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application', 'Scope']).reset_index(drop=True)

# Merge GREET EF
activity_mtg_ag_d = pd.merge(activity_mtg_ag_d, ob_ef.ef_raw, 
                               how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

# Merge NREL mitigation scenario electricity CIs to VISION
activity_mtg_ag_d_elec = pd.merge(activity_mtg_ag_d_elec, 
                                   elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
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
trend_reduce = ob_utils.trend_linear(mtg_ag_manure[['Year']], 'Year', 0 , input_params['Ag_manure_mgmt'])
mtg_ag_manure = pd.merge(mtg_ag_manure, trend_reduce, how='left', on='Year')
mtg_ag_manure['Total Emissions'] = -1 * mtg_ag_manure['Total Emissions'] * mtg_ag_manure['mtg_frac']
mtg_ag_manure['Case'] = 'Mitigation'
mtg_ag_manure['Mitigation Case'] = 'Manure Management, linear reduction'

#Ag / Precision Farming / Soil N2O / N2O
mtg_ag_N2O = activity_mtg_ag.loc[activity_mtg_ag['Subsector'] == 'N2O from Agricultural Soil Management', : ]
trend_reduce = ob_utils.trend_linear(mtg_ag_N2O[['Year']], 'Year', 0 , input_params['Ag_rice_cultv'])
mtg_ag_N2O = pd.merge(mtg_ag_N2O, trend_reduce, how='left', on='Year')
mtg_ag_N2O['Total Emissions'] = -1 * mtg_ag_N2O['Total Emissions'] * mtg_ag_N2O['mtg_frac']
mtg_ag_N2O['Case'] = 'Mitigation'
mtg_ag_N2O['Mitigation Case'] = 'Soil N2O emissions, linear reduction'

#Ag / Improved Water and Residue MGMT / Rice Cultivation / CH4
mtg_ag_rice = activity_mtg_ag.loc[activity_mtg_ag['Subsector'] == 'Rice Cultivation', : ]
trend_reduce = ob_utils.trend_linear(mtg_ag_rice[['Year']], 'Year', 0 , input_params['Ag_soil_N2O'])
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

activity_mtg_ag_d.drop(columns=['mtg_frac'], inplace=True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_ag_d], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
    

print( '    Elapsed time: ' + str(datetime.now() - init_time))

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
activity_mtg_lulucf['Emissions Unit'] = 'mmmt'
activity_mtg_lulucf['Scope'] = 'Direct, Non-Combustion'

# Calculate LCIA metric
activity_mtg_lulucf = pd.merge(activity_mtg_lulucf, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_lulucf['LCIA_estimate'] = activity_mtg_lulucf['Total Emissions'] * activity_mtg_lulucf['GWP']

# Create rest of the empty columns
activity_mtg_lulucf [ list(( Counter(activity_BAU.columns) - Counter(activity_mtg_lulucf.columns )).elements()) ] = '-'
activity_mtg_lulucf.drop(columns=['Emissions Category, Detailed', 'Emissions Category, Aggregate'], inplace=True)

activity_mtg_lulucf = pd.merge(activity_mtg_lulucf, corr_ghgs, how='left', on='Formula').reset_index(drop=True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_lulucf], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Generating mitigation scenarios for the Industrial sector
"""
# Declaring parameters for Industry mitigation sectors
#Id_mtg_params = {'mtg_paper' : 0.32, # target efficiency improvement across all activities of paper industries
#                 'mtg_food' : 0.37,   # target efficiency improvement across all activities of food industry
#                 'mtg_bulk_chemicals' : 0.13,   # target efficiency improvement across all bulk chemicals except green ammonia
#                 'mtg_clinker_new_tech' : 0.30,  # improvement in cement production technology over years
#                 'mtg_cement_lime' : 0.10, # target efficiency of cement and lime industry
#                 'mtg_refinery' : 0.13, # target efficiency improvement of refining industry
#                 'mtg_ironandsteel' : 0.13 } # target efficiency improvenent of iron and steel industry 
ef_mtg_clinker_replace = 0 # mt CO2 emissions per mt CO2 clinker production

#Id_mtg_switching = {'mtg_NG_to_H2' : 0.3, # target switching of NG to H2, default 0.3
#                    'mtg_NG_to_H2_refineries' : 0.7,
#                    'mtg_NG_to_H2_ironandsteel' : 0.3, # target switching of NG to H2
#                    'mtg_fossilH2_to_renewableH2' : 1.0} # target implementation of renewable H2 in place of fossil hydrogen

#ammonia_ng_frac_for_heatandpower = 0.283 # fraction of natural gas used for heat and power

print("Status: Constructing Industrial sector Mitigation scenario ..")

# Designing mitigation scenarios for paper industry
print("      : Paper Industry")

# Implementing efficiency improvements
mtg_id_paper_ef = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                       (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Paper Industry'), : ],
                                                  'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_paper']).copy()
mtg_id_paper_ef['Case'] = 'Mitigation'
mtg_id_paper_ef['Mitigation Case'] = 'Paper Industry, efficiency improvements'
mtg_id_paper_ef.loc[mtg_id_paper_ef['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_paper_ef.loc[mtg_id_paper_ef['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_ef.copy(), save_interim_files)

# Implementing fuel switching, NG to Electricity, after implementing efficiency improvements
mtg_id_paper_fsng = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_paper_fsng = mtg_id_paper_fsng.fillna(value='-')
mtg_id_paper_fsng = mtg_id_paper_fsng.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Scope', 'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fsng = \
    ob_utils.fuel_switching(mtg_id_paper_fsng,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['NG_to_Elec'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_paper_fsng['Case'] = 'Mitigation'
mtg_id_paper_fsng['Mitigation Case'] = 'Paper Industry, fuel switching Natural Gas to Electricity'
mtg_id_paper_fsng.loc[mtg_id_paper_fsng['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_paper_fsng.loc[mtg_id_paper_fsng['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Implementing fuel switching, Steam Coal to Electricity, after implementing efficiency improvements
mtg_id_paper_fssc = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
mtg_id_paper_fssc = mtg_id_paper_fssc.fillna(value='-')
mtg_id_paper_fssc = mtg_id_paper_fssc.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Scope', 'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fssc = \
    ob_utils.fuel_switching(mtg_id_paper_fssc,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Electricity', 'U.S. Average Grid Mix', ob_units.feedstock_convert['Coal_to_Elec'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_paper_fssc['Case'] = 'Mitigation'
mtg_id_paper_fssc['Mitigation Case'] = 'Paper Industry, fuel switching Steam Coal to Electricity'  
mtg_id_paper_fssc.loc[mtg_id_paper_fssc['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_paper_fssc.loc[mtg_id_paper_fssc['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion' 

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_fsng, save_interim_files)
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_fssc, save_interim_files)

# Implementing fuel switching NG to H2 blend
mtg_id_paper_fsngh2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                           (activity_ref_mtg['Subsector'] == 'Paper Industry') &
                                           (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_paper_fsngh2 = mtg_id_paper_fsngh2.fillna(value='-')
mtg_id_paper_fsngh2 = mtg_id_paper_fsngh2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Scope','Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_fsngh2 = \
    ob_utils.fuel_switching_H2NG(mtg_id_paper_fsngh2,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['Ind_mtg_NG_to_H2'])
mtg_id_paper_fsngh2['Case'] = 'Mitigation'
mtg_id_paper_fsngh2['Mitigation Case'] = 'Paper Industry, fuel switching Natural Gas to Hydrogen' 
mtg_id_paper_fsngh2.loc[mtg_id_paper_fsngh2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_paper_fsngh2.loc[mtg_id_paper_fsngh2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'                                  

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
                                           'Scope','Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_paper_h2 = \
    ob_utils.fuel_switching(mtg_id_paper_h2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['Ind_mtg_fossilH2_to_renewableH2'])
mtg_id_paper_h2['Case'] = 'Mitigation'
mtg_id_paper_h2['Mitigation Case'] = 'Paper Industry, fuel switching Fossil H2 to renewable H2'
mtg_id_paper_h2.loc[mtg_id_paper_h2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_paper_h2.loc[mtg_id_paper_h2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_paper_h2, save_interim_files)    

#%%
# Desigining mitigation scenarios for the Food industry

print("      : Food Industry")

# Implementing efficiency improvements
mtg_id_food_ef = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                       (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Food Industry'), : ],
                                                  'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_food']).copy()
mtg_id_food_ef['Case'] = 'Mitigation'
mtg_id_food_ef['Mitigation Case'] = 'Food Industry, efficiency improvements'
mtg_id_food_ef.loc[mtg_id_food_ef['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_food_ef.loc[mtg_id_food_ef['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  mtg_id_food_ef.copy(), save_interim_files)

# Implementing fuel switching, Steam Coal to Natural Gas, after implementing efficiency improvements
mtg_id_food_fssc = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Food Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
mtg_id_food_fssc = mtg_id_food_fssc.fillna(value='-')
mtg_id_food_fssc = mtg_id_food_fssc.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                               'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                               'Scope', 'Generation Type', 'Fuel Pool']).\
                                              agg({'Value' : 'sum'}).reset_index()
mtg_id_food_fssc = \
    ob_utils.fuel_switching(mtg_id_food_fssc,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                            trend_start_val=0, trend_end_val=1)
mtg_id_food_fssc['Case'] = 'Mitigation'
mtg_id_food_fssc['Mitigation Case'] = 'Food Industry, fuel switching Steam Coal to Natural Gas'  
mtg_id_food_fssc.loc[mtg_id_food_fssc['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_food_fssc.loc[mtg_id_food_fssc['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_food_fssc, save_interim_files)

# Implementing fuel switching H2 blend to NG
mtg_id_food_fsngh2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                           (activity_ref_mtg['Subsector'] == 'Food Industry') &
                                           (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_food_fsngh2 = mtg_id_food_fsngh2.fillna(value='-')
mtg_id_food_fsngh2 = mtg_id_food_fsngh2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Scope', 'Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
mtg_id_food_fsngh2 = \
    ob_utils.fuel_switching_H2NG(mtg_id_food_fsngh2,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['Ind_mtg_NG_to_H2'])
mtg_id_food_fsngh2['Case'] = 'Mitigation'
mtg_id_food_fsngh2['Mitigation Case'] = 'Food Industry, fuel switching Natural Gas to Hydrogen'  
mtg_id_food_fsngh2.loc[mtg_id_food_fsngh2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_food_fsngh2.loc[mtg_id_food_fsngh2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'                                 

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
                                           'Scope', 'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_food_h2 = \
    ob_utils.fuel_switching(mtg_id_food_h2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['Ind_mtg_fossilH2_to_renewableH2'])
mtg_id_food_h2['Case'] = 'Mitigation'
mtg_id_food_h2['Mitigation Case'] = 'Food Industry, fuel switching Fossil H2 to renewable H2'
mtg_id_food_h2.loc[mtg_id_food_h2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_food_h2.loc[mtg_id_food_h2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'   

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_food_h2, save_interim_files)    

#%%
# Design mitigation scenarios for Ammonia industry based on GHGI data

print("      : Bulk Chemicals Industry, Ammonia")

# combustion emissions

# unit conversion for file loaded values
id_quantity.loc[ : , ['activity_unit', 'activity_value']] = \
  ob_units.unit_convert_df(id_quantity.loc[ : , ['activity_unit', 'activity_value']],
   Unit = 'activity_unit', Value = 'activity_value')
 
# Expand data to all years
id_quantity['Year'] = decarb_year_min
id_quantity_exp = id_quantity.copy()
for yr in range(decarb_year_min+1, decarb_year_max+1): # [a,)
    id_quantity['Year'] = yr
    id_quantity_exp = pd.concat ([id_quantity_exp, id_quantity], axis=0).copy().reset_index(drop=True)

# Create mitigation scenarios for ammonia
mtg_green_amm = id_quantity_exp.loc[id_quantity_exp['Type'].isin(['Green Ammonia']), : ].copy()
       
# Scale the activity based on increase in shipment over the years
mtg_green_amm = pd.merge(mtg_green_amm, ob_eia.EIA_data['chemical_industry_supp']. \
                         loc[ob_eia.EIA_data['chemical_industry_supp']['Parameter'] == 'Ammonia Production', ['Year', 'frac_increase']].drop_duplicates(),
                         how='left',
                         on=['Year']).reset_index(drop=True)
mtg_green_amm['activity_value'] = mtg_green_amm['activity_value'] * mtg_green_amm['frac_increase']

# Trend for Green ammonia implementation over years as mitigation scenarios
ob_utils.model_2d_ammonia() # model run
mtg_green_amm['mtg_frac'] = [ob_utils.trend_2d_ammonia(x) for x in mtg_green_amm['Year']] # model predict
mtg_green_amm['activity_value'] = mtg_green_amm['activity_value'] * mtg_green_amm['mtg_frac'] # metric Ton of green ammonia coming online

# Reduction in conventional ammonia     
mtg_conv_amm = mtg_green_amm.copy()
mtg_conv_amm['Type'] = 'Conventional Ammonia'
mtg_conv_amm['activity_value'] = -1 * mtg_conv_amm['activity_value'] # metric Ton of conventional ammonia going offline

mtg_green_amm = pd.merge(mtg_green_amm, id_energy,
                         how='left',
                         on=['Sector', 'Subsector', 'Type']).reset_index(drop=True)
mtg_conv_amm = pd.merge(mtg_conv_amm, id_energy,
                        how='left',
                        on=['Sector', 'Subsector', 'Type']).reset_index(drop=True)
mtg_green_amm['Value'] = mtg_green_amm['activity_value'] * mtg_green_amm['energy_value'] # mmbtu green ammonia energy demand, coming online
mtg_conv_amm['Value'] = mtg_conv_amm['activity_value'] * mtg_conv_amm['energy_value'] # mmbtu conventional ammonia energy demand, going offline
mtg_amm = pd.concat([mtg_green_amm, mtg_conv_amm], axis=0).reset_index(drop=True)
mtg_amm.drop(columns=['Type', 'activity_unit', 'activity_value', 'frac_increase', 'mtg_frac', 'energy_unit_denominator', 'energy_value'], inplace=True)
mtg_amm = mtg_amm.groupby(['Data Source', 'Sector', 'Subsector', 'Year', 'End Use Application',
                           'Energy carrier', 'Energy carrier type', 'energy_unit_numerator']).\
                  agg({'Value' : 'sum'}).reset_index()

mtg_amm.rename(columns={'energy_unit_numerator' : 'Unit'}, inplace=True)
mtg_amm.loc[mtg_amm['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_amm.loc[mtg_amm['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'
mtg_amm['Case'] = 'Mitigation'
mtg_amm['Mitigation Case'] = 'Bulk Chemical Industry, Green Ammonia' 
         
mtg_amm[['AEO Case',
         'Generation Type',
         'Fuel Pool',
         'Basis']] = '-'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_amm, save_interim_files) 
del mtg_conv_amm, mtg_green_amm, mtg_amm

#%%

# Design mitigation scenarios for the Bulk chemicals industry

print("      : Bulk Chemicals Industry, overall")

# Implementing efficiency improvement
bulk_chem_ef = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                    (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_ef = bulk_chem_ef.fillna(value='-')
bulk_chem_ef = bulk_chem_ef.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
bulk_chem_ef = ob_utils.efficiency_improvement(bulk_chem_ef, 'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_bulk_chemicals']).copy()
bulk_chem_ef['Case'] = 'Mitigation'
bulk_chem_ef['Mitigation Case'] = 'Bulk Chemical Industry, efficiency improvements'
bulk_chem_ef.loc[bulk_chem_ef['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
bulk_chem_ef.loc[bulk_chem_ef['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'   

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_ef, save_interim_files) 

# Implement Fuel Switching {all} to Electricity for 61% (process heating) x 30% (low quality heat) of all fuel uses (except green ammonia) to Electricity
bulk_chem_fs = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_fs = bulk_chem_fs.loc[bulk_chem_fs['Mitigation Case'] != 'Bulk Chemical Industry, Green Ammonia', : ]
bulk_chem_fs = bulk_chem_fs.fillna(value='-')
bulk_chem_fs = bulk_chem_fs.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
# declaring low quality process heat
bulk_chem_fs['Value'] = bulk_chem_fs['Value'] * 0.61 * 0.30

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
bulk_chem_fs_mtg['Mitigation Case'] = 'Bulk Chemical Industry, fuel switching for low quality heat to Electricity'  
bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_fs_mtg, save_interim_files) 

# Fuel Switching, remaining Steam Coal to NG
bulk_chem_fs_mtg = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                        (activity_ref_mtg['Subsector'] == 'Bulk Chemical Industry'), : ]
bulk_chem_fs_mtg = bulk_chem_fs_mtg.fillna(value='-')
bulk_chem_fs_mtg = bulk_chem_fs_mtg.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                             'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                             'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
bulk_chem_fs_mtg = ob_utils.fuel_switching(bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] == 'Steam Coal', : ],
                                           'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                                           'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                                           trend_start_val=0, trend_end_val=1)
bulk_chem_fs_mtg['Case'] = 'Mitigation'
bulk_chem_fs_mtg['Mitigation Case'] = 'Bulk Chemical Industry, fuel switching Steam Coal to Natural Gas'
bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
bulk_chem_fs_mtg.loc[bulk_chem_fs_mtg['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'      

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, bulk_chem_fs_mtg, save_interim_files)                      

# non-combustion emissions
ghgi_mtg_am = ob_EPA_GHGI.activity_non_combust_exp.loc[(ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Industrial') & 
                                                       (ob_EPA_GHGI.activity_non_combust_exp['Subsector'] == 'Bulk Chemical Industry') & 
                                                       (ob_EPA_GHGI.activity_non_combust_exp['End Use Application'] == 'Ammonia Production'), :].copy()

ghgi_mtg_am['mtg_frac'] = [ob_utils.trend_2d_ammonia(x) for x in ghgi_mtg_am['Year']]

ghgi_mtg_am['Total Emissions'] = -1 * ghgi_mtg_am['Total Emissions'] * ghgi_mtg_am['mtg_frac'] # reduction in GHGI emissions due to ammonia production

ghgi_mtg_am['Case'] = 'Mitigation'
ghgi_mtg_am['Mitigation Case'] = 'Bulk Chemical Industry, Green Ammonia'
ghgi_mtg_am.loc[ghgi_mtg_am['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Non-Combustion'
ghgi_mtg_am.loc[ghgi_mtg_am['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Non-Combustion'

#%%
# Constructing mitigation scenarios for the Cement and Lime Industry

print("      : Cement and Lime Industry")

# Create Reference case for Cement Industry
id_cement = id_quantity_exp.loc[id_quantity_exp['Type'].isin(['Clinker Production']), : ].copy()
        
# Scale the activity based on increase in shipment over the years
id_cement = pd.merge(id_cement, ob_eia.EIA_data['chemical_industry_supp']. \
                           loc[ob_eia.EIA_data['chemical_industry_supp']['Parameter'] == 'Cement', ['Year', 'frac_increase']].drop_duplicates(),
                           how='left',
                           on=['Year']).reset_index(drop=True)
id_cement['activity_value'] = id_cement['activity_value'] * id_cement['frac_increase'] # metric ton

# Create Reference case for Lime Industry
id_lime = id_quantity_exp.loc[id_quantity_exp['Type'].isin(['High-Calcium Lime', 'Dolomitic Lime']), : ].copy()

# Scale the activity based on increase in shipment over the years
id_lime = pd.merge(id_lime, ob_eia.EIA_data['chemical_industry_supp']. \
                   loc[ob_eia.EIA_data['chemical_industry_supp']['Parameter'] == 'Cement', ['Year', 'frac_increase']].drop_duplicates(),
                   how='left',
                   on=['Year']).reset_index(drop=True)
id_lime['activity_value'] = id_lime['activity_value'] * id_lime['frac_increase'] # metric ton

# Calculate total emissions
id_cement['energy_value'] = calc_ef_clinker()
id_lime.loc[id_lime['Type'] == 'High-Calcium Lime', 'energy_value'] = calc_high_calcium_lime()
id_lime.loc[id_lime['Type'] == 'Dolomitic Lime', 'energy_value'] = calc_dolomitic_lime()

# Concatenate cement and lime scenarios
id_cement_lime = pd.concat([id_cement, id_lime], axis=0).reset_index(drop=True)

id_cement_lime['Total Emissions'] = id_cement_lime['activity_value'] * id_cement_lime['energy_value'] # metric ton x metric ton CO2/metric ton = metric ton CO2

id_cement_lime['End Use Application'] = id_cement_lime['Type']
id_cement_lime['energy_unit_numerator'] = 'mt' # MT CO2
id_cement_lime['energy_unit_denominator'] = 'mt' # MT cement and lime
id_cement_lime['Case'] = 'Reference case'
id_cement_lime['Scope'] = 'Direct, Non-Combustion'
id_cement_lime['Formula'] = 'CO2'
id_cement_lime.rename(columns={'energy_unit_numerator' : 'Emissions Unit'}, inplace=True)
id_cement_lime[['AEO Case', 'Basis', 'Fuel Pool', 
                'Flow Name', 'Unit', 'Value', 'CI', 'Mitigation Case']] = '-'

# unit conversion
tempdf = id_cement_lime.copy()
tempdf.loc[ : , ['Emissions Unit', 'Total Emissions']] = \
  ob_units.unit_convert_df(tempdf.loc[ : , ['Emissions Unit', 'Total Emissions']],
   Unit = 'Emissions Unit', Value = 'Total Emissions',
   if_given_category = True, unit_category = 'Emissions')

# Replacing the existing reference case for Cement and Lime with calculated reference case
activity_non_combust_oth = ob_EPA_GHGI.activity_non_combust_exp.loc[~((ob_EPA_GHGI.activity_non_combust_exp['Sector'] == 'Industrial') & 
                                                                      (ob_EPA_GHGI.activity_non_combust_exp['Subsector'] == 'Cement and Lime Industry') ), : ]
tempdf[['Energy carrier', 'Energy carrier type']] = '-'
ob_EPA_GHGI.activity_non_combust_exp = pd.concat([activity_non_combust_oth, tempdf[activity_non_combust_oth.columns]], axis=0).reset_index(drop=True)
del tempdf

# designing mitigation scenario for clinker (cement) and Lime non-combustion emissions
id_cement_lime_mtg = ob_utils.efficiency_improvement(id_cement_lime,
                                                      'Year', 'activity_value', 
                                                      trend_start_val=0, trend_end_val=input_params['Ind_mtg_clinker_new_tech']).copy()
id_cement_lime_mtg['Total Emissions'] = id_cement_lime_mtg['activity_value'] * ( id_cement_lime_mtg['energy_value'] - ef_mtg_clinker_replace)

id_cement_lime_mtg['Emissions Unit'] = id_cement_lime_mtg['activity_unit']

# unit conversion
id_cement_lime_mtg.loc[ : , ['Emissions Unit', 'Total Emissions']] = \
  ob_units.unit_convert_df(id_cement_lime_mtg.loc[ : , ['Emissions Unit', 'Total Emissions']],
   Unit = 'Emissions Unit', Value = 'Total Emissions',
   if_given_category = True, unit_category = 'Emissions')

id_cement_lime_mtg['Case'] = 'Mitigation'
id_cement_lime_mtg['Mitigation Case'] = 'Cement and Lime Industry, cement chemistry'
id_cement_lime_mtg['Scope'] = 'Direct, Non-Combustion'

# Design mitigation scenarios for clinker and lime for combustion emissions
# Implement efficiency improvement across all energy carriers
id_cement_lime_ef = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Cement and Lime Industry'), : ]
id_cement_lime_ef = id_cement_lime_ef.fillna(value='-')
id_cement_lime_ef = id_cement_lime_ef.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
id_cement_lime_ef = ob_utils.efficiency_improvement(id_cement_lime_ef, 'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_cement_lime']).copy()
id_cement_lime_ef['Case'] = 'Mitigation'
id_cement_lime_ef['Mitigation Case'] = 'Cement and Lime Industry, efficiency improvements'
id_cement_lime_ef.loc[id_cement_lime_ef['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
id_cement_lime_ef.loc[id_cement_lime_ef['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, id_cement_lime_ef, save_interim_files) 

# Implementing fuel switching, Steam Coal to Natural Gas, after implementing efficiency improvements
id_cement_lime_fssc = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                         (activity_ref_mtg['Subsector'] == 'Cement and Lime Industry') &
                                         (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
id_cement_lime_fssc = id_cement_lime_fssc.fillna(value='-')
id_cement_lime_fssc = id_cement_lime_fssc.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
id_cement_lime_fssc = \
    ob_utils.fuel_switching(id_cement_lime_fssc,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                            trend_start_val=0, trend_end_val=1)
id_cement_lime_fssc['Case'] = 'Mitigation'
id_cement_lime_fssc['Mitigation Case'] = 'Cement and Lime Industry, fuel switching Steam Coal to Natural Gas' 
id_cement_lime_fssc.loc[id_cement_lime_fssc['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
id_cement_lime_fssc.loc[id_cement_lime_fssc['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'  

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, id_cement_lime_fssc, save_interim_files)

# Implementing fuel switching NG to H2 blend
id_cement_lime_fsngh2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                           (activity_ref_mtg['Subsector'] == 'Cement and Lime Industry') &
                                           (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
id_cement_lime_fsngh2 = id_cement_lime_fsngh2.fillna(value='-')
id_cement_lime_fsngh2 = id_cement_lime_fsngh2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                                   'Scope', 'Generation Type', 'Fuel Pool']).\
                                                  agg({'Value' : 'sum'}).reset_index()
id_cement_lime_fsngh2 = \
    ob_utils.fuel_switching_H2NG(id_cement_lime_fsngh2,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['Ind_mtg_NG_to_H2'])
id_cement_lime_fsngh2['Case'] = 'Mitigation'
id_cement_lime_fsngh2['Mitigation Case'] = 'Cement and Lime Industry, fuel switching Natural Gas to Hydrogen'
id_cement_lime_fsngh2.loc[id_cement_lime_fsngh2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
id_cement_lime_fsngh2.loc[id_cement_lime_fsngh2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'                                    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, id_cement_lime_fsngh2, save_interim_files)

# Mitigation scenario for switching from fossil H2 and renewable H2
id_cement_lime_h2 = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                       (activity_ref_mtg['Subsector'] == 'Cement and Lime Industry') &
                                       (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                       (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]
id_cement_lime_h2 = id_cement_lime_h2.fillna(value='-')
id_cement_lime_h2 = id_cement_lime_h2.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                           'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                           'Scope', 'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
id_cement_lime_h2 = \
    ob_utils.fuel_switching(id_cement_lime_h2,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['Ind_mtg_fossilH2_to_renewableH2'])
id_cement_lime_h2['Case'] = 'Mitigation'
id_cement_lime_h2['Mitigation Case'] = 'Cement and Lime Industry, fuel switching Fossil H2 to renewable H2'
id_cement_lime_h2.loc[id_cement_lime_h2['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
id_cement_lime_h2.loc[id_cement_lime_h2['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, id_cement_lime_h2, save_interim_files)  

#%%

# Designing mitigation scenarios for the refining industry

print("      : Refining Industry")

mtg_id_refi = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                   (activity_ref_mtg['Subsector'] == 'Refining Industry'), : ]
mtg_id_refi = mtg_id_refi.fillna(value='-')
mtg_id_refi = mtg_id_refi.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
# Implementing efficiency improvements
mtg_id_refi = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                   (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Refining Industry'), : ],
                                                  'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_refinery']).copy()
mtg_id_refi['Case'] = 'Mitigation'
mtg_id_refi['Mitigation Case'] = 'Refining Industry, efficiency improvements'
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_refi, save_interim_files)

# Implementing fuel switching NG to H2 blend
mtg_id_refi = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                   (activity_ref_mtg['Subsector'] == 'Refining Industry') &
                                   (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_refi = mtg_id_refi.fillna(value='-')
mtg_id_refi = mtg_id_refi.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                   'Scope', 'Generation Type', 'Fuel Pool']).\
                          agg({'Value' : 'sum'}).reset_index()
mtg_id_refi = \
    ob_utils.fuel_switching_H2NG(mtg_id_refi,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['Ind_mtg_NG_to_H2_refineries'])
mtg_id_refi['Case'] = 'Mitigation'
mtg_id_refi['Mitigation Case'] = 'Refinery Industry, fuel switching Natural Gas to Hydrogen' 
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_refi, save_interim_files)  

# Mitigation scenario for switching from fossil H2 and renewable H2
mtg_id_refi = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                       (activity_ref_mtg['Subsector'] == 'Refining Industry') &
                                       (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                       (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]
mtg_id_refi = mtg_id_refi.fillna(value='-')
mtg_id_refi = mtg_id_refi.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                           'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                           'Scope', 'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_refi = \
    ob_utils.fuel_switching(mtg_id_refi,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['Ind_mtg_fossilH2_to_renewableH2'])
mtg_id_refi['Case'] = 'Mitigation'
mtg_id_refi['Mitigation Case'] = 'Refining Industry, fuel switching Fossil H2 to renewable H2'
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_refi.loc[mtg_id_refi['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_refi, save_interim_files) 

#%%

# Designing mitigation scenarios for the Iron & Steel industry

print("      : Iron & Steel Industry")

mtg_id_iron = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                   (activity_ref_mtg['Subsector'] == 'Iron and Steel Industry'), : ]
mtg_id_iron = mtg_id_iron.fillna(value='-')
mtg_id_iron = mtg_id_iron.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                     'Scope', 'Generation Type', 'Fuel Pool']).\
                            agg({'Value' : 'sum'}).reset_index()
# Implementing efficiency improvements
mtg_id_iron = ob_utils.efficiency_improvement(ob_eia.EIA_data['energy_demand'].loc[(ob_eia.EIA_data['energy_demand']['Sector']=='Industrial') &
                                                                                   (ob_eia.EIA_data['energy_demand']['Subsector'] == 'Iron and Steel Industry'), : ],
                                              'Year', 'Value', trend_start_val=0, trend_end_val=input_params['Ind_mtg_ironandsteel']).copy()
mtg_id_iron['Case'] = 'Mitigation'
mtg_id_iron['Mitigation Case'] = 'Iron and Steel Industry, efficiency improvements'
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'    

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_iron, save_interim_files)

# Implementing fuel switching NG to H2 blend
mtg_id_iron = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                   (activity_ref_mtg['Subsector'] == 'Iron and Steel Industry') &
                                   (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_id_iron = mtg_id_iron.fillna(value='-')
mtg_id_iron = mtg_id_iron.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                   'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                   'Scope', 'Generation Type', 'Fuel Pool']).\
                          agg({'Value' : 'sum'}).reset_index()
mtg_id_iron = \
    ob_utils.fuel_switching_H2NG(mtg_id_iron,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['Ind_mtg_NG_to_H2_ironandsteel'])
mtg_id_iron['Case'] = 'Mitigation'
mtg_id_iron['Mitigation Case'] = 'Iron and Steel Industry, fuel switching Natural Gas to Hydrogen' 
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_iron, save_interim_files)  

# Mitigation scenario for switching from fossil H2 and renewable H2
mtg_id_iron = activity_ref_mtg.loc[(activity_ref_mtg['Sector'] == 'Industrial') & 
                                       (activity_ref_mtg['Subsector'] == 'Iron and Steel Industry') &
                                       (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                       (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]
mtg_id_iron = mtg_id_iron.fillna(value='-')
mtg_id_iron = mtg_id_iron.groupby(['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                                           'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit',
                                           'Scope', 'Generation Type', 'Fuel Pool']).\
                                    agg({'Value' : 'sum'}).reset_index()
mtg_id_iron = \
    ob_utils.fuel_switching(mtg_id_iron,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['Ind_mtg_fossilH2_to_renewableH2'])
mtg_id_iron['Case'] = 'Mitigation'
mtg_id_iron['Mitigation Case'] = 'Iron and Steel Industry, fuel switching Fossil H2 to renewable H2'
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_id_iron.loc[mtg_id_iron['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_id_iron, save_interim_files) 

#%%

# LCIA metric calculation

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
                                   elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
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

# Concatenate non-combustion mitigation scope for ammonia, lime and cement industries
activity_mtg_id = pd.concat([activity_mtg_id, ghgi_mtg_am, id_cement_lime, id_cement_lime_mtg], axis=0).reset_index(drop=True)

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

# Drop not needed columns
activity_mtg_id = activity_mtg_id[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, activity_mtg_id], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

#%%

# Implement CCS for industrial sectors and selected subsectors

print("      : CCS implementation for Industry subsectors")

ob_ccs.implement_ccs(activity_BAU, 'Industrial')
ob_ccs.calc_ccs_activity(ob_units)

ob_ccs.ccs_process['End Use Application'] = '-'
ob_ccs.ccs_process['Mitigation Case'] = 'Industrial, CCS implementation'
ob_ccs.ccs_process[['Data Source', 'AEO Case', 'Basis', 'Unit', 'Generation Type', 'Fuel Pool']] = '-'
ob_ccs.ccs_process = ob_ccs.ccs_process.loc[~ob_ccs.ccs_process['LCIA_estimate'].isna(), : ]

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, ob_ccs.ccs_process[activity_ref_mtg.columns], save_interim_files) 

# Calculate LCIA for CCS process energy demands
df_elec = ob_ccs.ccs_process.loc[ob_ccs.ccs_process['Energy carrier'] == 'Electricity', : ].reset_index(drop=True)
df = ob_ccs.ccs_process.loc[~(ob_ccs.ccs_process['Energy carrier'] == 'Electricity'), : ].reset_index(drop=True)

# Merge GREET correspondence table
df = pd.merge(df, corr_EF_GREET, how='left', 
              on=['Sector', 'Subsector', 'Scope', 'Energy carrier', 'Energy carrier type', 
                  'End Use Application']).reset_index(drop=True)

# Merge GREET EF
df = pd.merge(df, ob_ef.ef_raw, 
              how='left', on=['Case', 'Scope', 'Year', 'Formula', 'GREET Pathway']).reset_index(drop=True)
df.rename(columns={'Unit (Denominator)' : 'Energy Unit',
                   'Reference case' : 'CI'}, inplace=True)
df['Emissions Unit'] = df['Unit (Numerator)']

df['Total Emissions'] = df['Value'] * df['CI'] # grams GHGs

df.drop(columns=['unit_numerator', 'unit_denominator', 'Value', 'Unit (Numerator)', 'Energy Unit', 'CI',
                 'GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0', 'Flow Name'], inplace=True)

# Merge NREL mitigation scenario electricity CIs to VISION
df_elec = pd.merge(df_elec, 
                   elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                   how='left',
                   on=['Year', 'Formula']).reset_index(drop=True)
df_elec.rename(columns={'CI_elec_mtg' : 'CI',
                        'Emissions Unit_y' : 'Emissions Unit'}, inplace=True)

df_elec['Total Emissions'] = df_elec['Value'] * df_elec['CI'] # grams GHGs

df_elec.drop(columns=['unit_numerator', 'unit_denominator', 'Value', 
                      'Emissions Unit_x', 'Energy Unit', 'CI'], inplace=True)

# Concatenate electric and non-electric activities
mtg_id_ccs = pd.concat([df, df_elec], axis = 0).reset_index(drop=True)

del df, df_elec

# Calculate LCIA metric
mtg_id_ccs = pd.merge(mtg_id_ccs, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
mtg_id_ccs['Total Emissions'] = mtg_id_ccs['Total Emissions'].astype('float64')
mtg_id_ccs['LCIA_estimate'] = mtg_id_ccs['Total Emissions'] * mtg_id_ccs['GWP']

# unit conversions
mtg_id_ccs.loc[~mtg_id_ccs['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(mtg_id_ccs.loc[~mtg_id_ccs['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

ob_ccs.env_df['Mitigation Case'] = 'Industrial, CCS implementation'
ob_ccs.env_df['Case'] = 'Mitigation'
ob_ccs.env_df.drop(columns=['Marker', 'frac'], inplace=True)

mtg_id_ccs = pd.concat([mtg_id_ccs, ob_ccs.env_df], axis = 0).reset_index(drop=True)

mtg_id_ccs = pd.merge(mtg_id_ccs, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
  
# Create rest of the empty columns
mtg_id_ccs [ list(( Counter(activity_BAU.columns) - Counter(mtg_id_ccs.columns )).elements()) ] = '-'

# Drop not needed columns
mtg_id_ccs = mtg_id_ccs[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_id_ccs], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Global Mitigation scenario of replacing Steam Coal with NG and consequently with Hydrogen --> renewable Hydrogen
"""
print("Status: Constructing global Mitigation scenarios ..")

# Do not apply to any of the current decarb scenarios in industrial sector
mtg_global = activity_ref_mtg.loc[~(activity_ref_mtg['Subsector'].isin(['Paper Industry', 'Food Industry', 
                                                                        'Cement and Lime Industry', 'Refining Industry',
                                                                        'Bulk Chemical Industry',
                                                                        'Iron and Steel Industry'])) & 
                                  (activity_ref_mtg['Energy carrier'] == 'Steam Coal'), : ]
mtg_global = mtg_global.fillna(value='-')
mtg_global = mtg_global.groupby(['Sector', 'Subsector', 'End Use Application',
                                     'Energy carrier', 'Energy carrier type', 'Year']).\
                            agg({'Value' : 'sum'}).reset_index()
                            
mtg_global[['Data Source', 'AEO Case', 'Basis', 'Generation Type', 'Fuel Pool']] = '-'
mtg_global['Unit'] = 'MMBtu'
mtg_global['Scope'] = 'Direct, Combustion'
                            
# Implementing fuel switching, Steam Coal to Natural Gas
mtg_global = \
    ob_utils.fuel_switching(mtg_global,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Natural Gas', 'U.S. Average Mix', ob_units.feedstock_convert['Coal_to_NG'], 
                            trend_start_val=0, trend_end_val=1)
mtg_global['Case'] = 'Mitigation'
mtg_global['Mitigation Case'] = 'Global, fuel switching Steam Coal to Natural Gas'
mtg_global.loc[mtg_global['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_global.loc[mtg_global['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'
                            
# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg,  mtg_global.copy(), save_interim_files)
                            
# Implementing fuel switching NG to H2 blend
mtg_global = activity_ref_mtg.loc[~(activity_ref_mtg['Subsector'].isin(['Paper Industry', 'Food Industry', 
                                                                        'Cement and Lime Industry', 'Refining Industry',
                                                                        'Bulk Chemical Industry',
                                                                        'Iron and Steel Industry'])) & 
                                  (activity_ref_mtg['Energy carrier'] == 'Natural Gas'), : ]
mtg_global = mtg_global.fillna(value='-')
mtg_global = mtg_global.loc[~(mtg_global['Value'] == '-'), : ]
mtg_global = mtg_global.groupby(['Sector', 'Subsector', 'End Use Application',
                                 'Energy carrier', 'Energy carrier type', 'Year']).\
                          agg({'Value' : 'sum'}).reset_index()

mtg_global[['Data Source', 'AEO Case', 'Basis', 'Generation Type', 'Fuel Pool']] = '-'
mtg_global['Unit'] = 'MMBtu'
mtg_global['Scope'] = 'Direct, Combustion'
mtg_global['Value'] = mtg_global['Value'] .astype('float64')

mtg_global = \
    ob_utils.fuel_switching_H2NG(mtg_global,
                            'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Natural Gas', 
                            min_val=0, max_val=input_params['global_mtg_NG_to_H2'])

mtg_global['Case'] = 'Mitigation'
mtg_global['Mitigation Case'] = 'Global, fuel switching Natural Gas to Hydrogen' 
mtg_global.loc[mtg_global['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_global.loc[mtg_global['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_global, save_interim_files)  

# Mitigation scenario for switching from fossil H2 and renewable H2
mtg_global = activity_ref_mtg.loc[~(activity_ref_mtg['Subsector'].isin(['Refining Industry', 'Food Industry', 
                                                                         'Paper Industry', 'Bulk Chemical Industry', 
                                                                         'Cement and Lime Industry', 'Iron and Steel Industry'])) &
                                  (activity_ref_mtg['Energy carrier'] == 'Hydrogen') &
                                  (activity_ref_mtg['Energy carrier type'] == 'Natural Gas'), : ]

mtg_global = mtg_global.fillna(value='-')
mtg_global = mtg_global.groupby(['Sector', 'Subsector', 'End Use Application',
                                 'Energy carrier', 'Energy carrier type', 'Year']).\
                                    agg({'Value' : 'sum'}).reset_index()

mtg_global[['Data Source', 'AEO Case', 'Basis', 'Generation Type', 'Fuel Pool']] = '-'
mtg_global['Unit'] = 'MMBtu'
mtg_global['Scope'] = 'Direct, Combustion'

mtg_global = \
    ob_utils.fuel_switching(mtg_global,
                            'Year', 'Value', 'Energy carrier', 'Energy carrier type', 
                            'Hydrogen', 'Renewables', 1, 
                            trend_start_val=0, trend_end_val=input_params['global_mtg_fossilH2_to_renewableH2'])

mtg_global['Case'] = 'Mitigation'
mtg_global['Mitigation Case'] = 'Global, fuel switching Fossil H2 to renewable H2'
mtg_global.loc[mtg_global['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
mtg_global.loc[mtg_global['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'

# Append to activity matrix and save
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_global, save_interim_files) 


# Seperate electric and non-electric activities
mtg_global = activity_ref_mtg.loc[(activity_ref_mtg['Case'] == 'Mitigation') &
                                       (activity_ref_mtg['Mitigation Case'].isin(['Global, fuel switching Steam Coal to Natural Gas',
                                                                                  'Global, fuel switching Natural Gas to Hydrogen',
                                                                                  'Global, fuel switching Fossil H2 to renewable H2'])), : ]
#mtg_global_elec = mtg_global.loc[mtg_global['Energy carrier'] == 'Electricity', : ]
mtg_global = mtg_global.loc[~(mtg_global['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
mtg_global = pd.merge(mtg_global, corr_EF_GREET, how='left', 
                               on=['Sector', 'Scope', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application']).reset_index(drop=True)

# Merge GREET EF
mtg_global = pd.merge(mtg_global, ob_ef.ef_raw, 
                           how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])
"""
# Merge NREL mitigation scenario electricity CIs to VISION
mtg_global_elec = pd.merge(mtg_global_elec, 
                           elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                           how='left',
                           on=['Year', 'Emissions Unit'])
mtg_global_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)
"""
mtg_global.rename(columns={'Unit (Denominator)' : 'Energy Unit',
                           'Reference case' : 'CI'}, inplace=True)
mtg_global.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

# Concatenate electric and non-electric activities
#mtg_global = pd.concat([mtg_global, mtg_global_elec], axis = 0).reset_index(drop=True)

mtg_global['Total Emissions'] = mtg_global['Value'] * mtg_global['CI']

# Calculate LCIA metric
mtg_global = pd.merge(mtg_global, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
mtg_global['LCIA_estimate'] = mtg_global['Total Emissions'] * mtg_global['GWP']
mtg_global.rename(columns={'Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

# unit conversions
mtg_global.loc[~mtg_global['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(mtg_global.loc[~mtg_global['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

mtg_global = pd.merge(mtg_global, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
  
# Create rest of the empty columns
mtg_global [ list(( Counter(activity_BAU.columns) - Counter(mtg_global.columns )).elements()) ] = '-'

# Drop not needed columns
mtg_global = mtg_global[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_global], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time))

#%%
"""
Biofuel Mitigation Strategy
"""
print("Status: Constructing Biofuel Mitigation Scenario ..")

print("      : Sustainable Aviation Fuels")

# Subset Jet-Like Biofuels
biofuel_sub = biofuel.loc[biofuel['Energy carrier'].isin(['Sustainable Aviation Fuel']), : ].copy()

# Rename columns to avoid merge conflicts
biofuel_sub.rename(columns = {'Value' :'Biofuel Value',
                              'Energy carrier' : 'Biofuel',
                              'Energy carrier type' : 'Biofuel type'}, inplace=True)

# Determine relative fraction of SAF fuels
biofuel_sub_agg = biofuel_sub.groupby(['Year', 'Unit'], as_index = False)['Biofuel Value'].sum().reset_index()
biofuel_sub_agg.rename(columns = {'Biofuel Value' : 'Agg Biofuel Value'}, inplace=True)
biofuel_sub_frac = pd.merge(biofuel_sub, biofuel_sub_agg, how='left', on = "Year").reset_index(drop=True)
biofuel_sub_frac['Biofuel Ratio'] = biofuel_sub_frac['Biofuel Value'] / biofuel_sub_frac['Agg Biofuel Value'] 
biofuel_sub_frac = biofuel_sub_frac[['Year','Biofuel','Biofuel type','Biofuel Ratio']]

# Subset Energy Demand Matrix into associated fossil fuel pools
conv_fuel = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier'].isin(['Jet Fuel'])]
conv_fuel = conv_fuel.groupby(['Sector', 'Subsector', 'End Use Application',
                         'Energy carrier', 'Energy carrier type', 'Year',
                         'Scope'], as_index = False)['Value'].sum()

# Calculate the fraction of Biofuel to Petroleum fuel in the Fuel Pool
conv_fuel_agg = conv_fuel.groupby(['Year'], as_index = False)['Value'].sum()
conv_fuel_agg = conv_fuel_agg.rename(columns = {'Value':'Petroleum'})
conv_fuel_agg = pd.merge(biofuel_sub_agg, conv_fuel_agg, how='left', on = ['Year']).reset_index(drop=True)
conv_fuel_agg['Ratio'] = conv_fuel_agg['Agg Biofuel Value'] / conv_fuel_agg['Petroleum'] 

# Petroleum Jet Fuel Comming Offline
mtg_biof = pd.merge(conv_fuel, conv_fuel_agg[['Year', 'Ratio']], how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_off = mtg_biof.copy()
mtg_biof_off['Value'] = mtg_biof_off['Value'] * mtg_biof_off['Ratio'] * -1
mtg_biof_off.loc[:, 'Case' ] = 'Mitigation'
mtg_biof_off.loc[:,'Mitigation Case' ] = 'Biofuels, SAF'
mtg_biof_off.loc[:,'Fuel Pool' ] = 'Jet'
mtg_biof_off.loc[:, 'Unit'] = 'mmbtu'
mtg_biof_off.drop(columns = {'Ratio'}, inplace = True)

# Update Energy Demand Matrix
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_off, save_interim_files) 

# SAF Coming online. Drop all biofuel fractions those having zero production (Biofuel Ratio = 0)
biofuel_sub_frac = biofuel_sub_frac.loc[biofuel_sub_frac['Biofuel Ratio'] != 0, : ]
mtg_biof_on = pd.merge(mtg_biof, biofuel_sub_frac, how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_on['Value'] = mtg_biof_on['Value'] * mtg_biof_on['Ratio'] * mtg_biof_on['Biofuel Ratio']  
mtg_biof_on['Case' ] = 'Mitigation'
mtg_biof_on['Mitigation Case'] = 'Biofuels, SAF'
mtg_biof_on['Fuel Pool'] = 'Jet'
mtg_biof_on.loc[:, 'Unit'] = 'mmbtu'
mtg_biof_on.drop(columns={'Energy carrier', 'Energy carrier type', 'Ratio', 'Biofuel Ratio'}, inplace=True)
mtg_biof_on.rename(columns={'Biofuel' : 'Energy carrier', 'Biofuel type' : 'Energy carrier type'}, inplace=True)

activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_on, save_interim_files)

    
print("      : Diesel-like Biofuels")

# Subset Diesel-Like Biofuels
biofuel_sub = biofuel.loc[biofuel['Energy carrier'].isin(['Biodiesel',
                                                          'FT-Diesel',
                                                          'Renewable Diesel']), : ].copy()

# Rename columns to avoid merge conflicts
biofuel_sub.rename(columns = {'Value' :'Biofuel Value',
                              'Energy carrier' : 'Biofuel',
                              'Energy carrier type' : 'Biofuel type'}, inplace=True)

# Determine relative fraction of SAF fuels
biofuel_sub_agg = biofuel_sub.groupby(['Year', 'Unit'], as_index = False)['Biofuel Value'].sum().reset_index()
biofuel_sub_agg.rename(columns = {'Biofuel Value' : 'Agg Biofuel Value'}, inplace=True)
biofuel_sub_frac = pd.merge(biofuel_sub, biofuel_sub_agg, how='left', on = "Year").reset_index(drop=True)
biofuel_sub_frac['Biofuel Ratio'] = biofuel_sub_frac['Biofuel Value'] / biofuel_sub_frac['Agg Biofuel Value'] 
biofuel_sub_frac = biofuel_sub_frac[['Year','Biofuel','Biofuel type','Biofuel Ratio']]

# Subset Energy Demand Matrix into associated fossil fuel pools
conv_fuel = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier type'].isin(['Petroleum Distillate'])]
conv_fuel = conv_fuel.groupby(['Sector', 'Subsector', 'End Use Application',
                         'Energy carrier', 'Energy carrier type', 'Year',
                         'Scope'], as_index = False)['Value'].sum()

# Calculate the fraction of Biofuel to Petroleum fuel in the Fuel Pool
conv_fuel_agg = conv_fuel.groupby(['Year'], as_index = False)['Value'].sum()
conv_fuel_agg = conv_fuel_agg.rename(columns = {'Value':'Petroleum'})
conv_fuel_agg = pd.merge(biofuel_sub_agg, conv_fuel_agg, how='left', on = ['Year']).reset_index(drop=True)
conv_fuel_agg['Ratio'] = conv_fuel_agg['Agg Biofuel Value'] / conv_fuel_agg['Petroleum'] 

# Diesel like fuel going offline
mtg_biof = pd.merge(conv_fuel, conv_fuel_agg[['Year', 'Ratio']], how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_off = mtg_biof.copy()
mtg_biof_off['Value'] = mtg_biof_off['Value'] * mtg_biof_off['Ratio'] * -1
mtg_biof_off['Case' ] = 'Mitigation'
mtg_biof_off['Mitigation Case' ] = 'Biofuels, Diesel'
mtg_biof_off['Fuel Pool' ] = 'Diesel'
mtg_biof_off['Unit'] = 'mmbtu'
mtg_biof_off.drop(columns = {'Ratio'}, inplace = True)

# Update Energy Demand Matrix
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_off, save_interim_files) 

# Renewable diesel Coming online. Drop all biofuel fractions those having zero production (Biofuel Ratio = 0)
biofuel_sub_frac = biofuel_sub_frac.loc[biofuel_sub_frac['Biofuel Ratio'] != 0, : ]
mtg_biof_on = pd.merge(mtg_biof, biofuel_sub_frac, how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_on = mtg_biof_on.loc[mtg_biof_on['Ratio'] != 0, : ]
mtg_biof_on['Value'] = mtg_biof_on['Value'] * mtg_biof_on['Ratio'] * mtg_biof_on['Biofuel Ratio']  
mtg_biof_on['Case' ] = 'Mitigation'
mtg_biof_on['Mitigation Case'] = 'Biofuels, Diesel'
mtg_biof_on['Fuel Pool'] = 'Diesel'
mtg_biof_on.loc[:, 'Unit'] = 'mmbtu'
mtg_biof_on.drop(columns={'Energy carrier', 'Energy carrier type', 'Ratio', 'Biofuel Ratio'}, inplace=True)
mtg_biof_on.rename(columns={'Biofuel' : 'Energy carrier', 'Biofuel type' : 'Energy carrier type'}, inplace=True)

activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_on, save_interim_files)


print("      : Gasoline-like Biofuels")

# Subset Diesel-Like Biofuels
biofuel_sub = biofuel.loc[biofuel['Energy carrier'].isin(['Renewable Gasoline']), : ].copy()

# Rename columns to avoid merge conflicts
biofuel_sub.rename(columns = {'Value' :'Biofuel Value',
                              'Energy carrier' : 'Biofuel',
                              'Energy carrier type' : 'Biofuel type'}, inplace=True)

# Determine relative fraction of SAF fuels
biofuel_sub_agg = biofuel_sub.groupby(['Year', 'Unit'], as_index = False)['Biofuel Value'].sum().reset_index()
biofuel_sub_agg.rename(columns = {'Biofuel Value' : 'Agg Biofuel Value'}, inplace=True)
biofuel_sub_frac = pd.merge(biofuel_sub, biofuel_sub_agg, how='left', on = "Year").reset_index(drop=True)
biofuel_sub_frac['Biofuel Ratio'] = biofuel_sub_frac['Biofuel Value'] / biofuel_sub_frac['Agg Biofuel Value'] 
biofuel_sub_frac = biofuel_sub_frac.loc[~ biofuel_sub_frac['Biofuel Ratio'].isna(), : ]
biofuel_sub_frac = biofuel_sub_frac[['Year','Biofuel','Biofuel type','Biofuel Ratio']]

# Subset Energy Demand Matrix into associated fossil fuel pools
conv_fuel = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier type'].isin(['Petroleum Gasoline'])]
conv_fuel = conv_fuel.groupby(['Sector', 'Subsector', 'End Use Application',
                         'Energy carrier', 'Energy carrier type', 'Year',
                         'Scope'], as_index = False)['Value'].sum()

# Calculate the fraction of Biofuel to Petroleum fuel in the Fuel Pool
conv_fuel_agg = conv_fuel.groupby(['Year'], as_index = False)['Value'].sum()
conv_fuel_agg = conv_fuel_agg.rename(columns = {'Value':'Petroleum'})
conv_fuel_agg = pd.merge(biofuel_sub_agg, conv_fuel_agg, how='left', on = ['Year']).reset_index(drop=True)
conv_fuel_agg['Ratio'] = conv_fuel_agg['Agg Biofuel Value'] / conv_fuel_agg['Petroleum'] 

# Petroleum Jet Fuel Comming Offline
mtg_biof = pd.merge(conv_fuel, conv_fuel_agg[['Year', 'Ratio']], how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_off = mtg_biof.copy()
mtg_biof_off['Value'] = mtg_biof_off['Value'] * mtg_biof_off['Ratio'] * -1
mtg_biof_off.loc[:, 'Case' ] = 'Mitigation'
mtg_biof_off.loc[:,'Mitigation Case' ] = 'Biofuels, Gasoline'
mtg_biof_off.loc[:,'Fuel Pool' ] = 'Gasoline'
mtg_biof_off.loc[:, 'Unit'] = 'mmbtu'
mtg_biof_off.drop(columns = {'Ratio'}, inplace = True)

# Update Energy Demand Matrix
activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_off, save_interim_files) 

# SAF Coming online. Drop all biofuel fractions those having zero production (Biofuel Ratio = 0)
biofuel_sub_frac = biofuel_sub_frac.loc[biofuel_sub_frac['Biofuel Ratio'] != 0, : ]
mtg_biof_on = pd.merge(mtg_biof, biofuel_sub_frac, how = 'left', on = 'Year').reset_index(drop=True)
mtg_biof_on['Value'] = mtg_biof_on['Value'] * mtg_biof_on['Ratio'] * mtg_biof_on['Biofuel Ratio']  
mtg_biof_on = mtg_biof_on.loc[~ mtg_biof_on['Value'].isna(), : ]
mtg_biof_on['Case' ] = 'Mitigation'
mtg_biof_on['Mitigation Case'] = 'Biofuels, Gasoline'
mtg_biof_on['Fuel Pool'] = 'Gasoline'
mtg_biof_on.loc[:, 'Unit'] = 'mmbtu'
mtg_biof_on.drop(columns={'Energy carrier', 'Energy carrier type', 'Ratio', 'Biofuel Ratio'}, inplace=True)
mtg_biof_on.rename(columns={'Biofuel' : 'Energy carrier', 'Biofuel type' : 'Energy carrier type'}, inplace=True)

activity_ref_mtg = save_activity_mx(activity_ref_mtg, mtg_biof_on, save_interim_files)


# Subset on Biofuel Mitigation Strategies
mtg_biofuels = activity_ref_mtg.loc[(activity_ref_mtg['Case'] == 'Mitigation') &
                                       (activity_ref_mtg['Mitigation Case'].isin(['Biofuels, SAF',
                                                                                  'Biofuels, Diesel',
                                                                                  'Biofuels, Gasoline'])), : ]
# Ensure that only non-electric entries are selected
mtg_biofuels = mtg_biofuels.loc[~(mtg_biofuels['Energy carrier'] == 'Electricity'), : ]

# Merge GREET correspondence table
mtg_biofuels = pd.merge(mtg_biofuels, corr_EF_GREET, how='left', 
                               on=['Sector', 'Scope', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                   'End Use Application']).reset_index(drop=True)

# Merge GREET EF
mtg_biofuels = pd.merge(mtg_biofuels, ob_ef.ef_raw, 
                           how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

mtg_biofuels.rename(columns={'Unit (Denominator)' : 'Energy Unit',
                           'Reference case' : 'CI'}, inplace=True)

# Drop not needed columns
mtg_biofuels.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

mtg_biofuels['Total Emissions'] = mtg_biofuels['Value'] * mtg_biofuels['CI']

# Calculate LCIA metric
mtg_biofuels = pd.merge(mtg_biofuels, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
mtg_biofuels['LCIA_estimate'] = mtg_biofuels['Total Emissions'] * mtg_biofuels['GWP']
mtg_biofuels.rename(columns={'Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

# unit conversions
mtg_biofuels.loc[~mtg_biofuels['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(mtg_biofuels.loc[~mtg_biofuels['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

mtg_biofuels = pd.merge(mtg_biofuels, corr_ghgs, how='left', on='Formula').reset_index(drop=True)
  
# Create rest of the empty columns
mtg_biofuels [ list(( Counter(activity_BAU.columns) - Counter(mtg_biofuels.columns )).elements()) ] = '-'

# Drop not needed columns
mtg_biofuels = mtg_biofuels[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_biofuels], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time)) 

#%%
"""
Calculate LULUCF Impacts from Biofuel Mitigation Strategy

"""

print("Status: Constructing Biofuel LULUCF Impacts ..")

#activity_BAU.head()
#activity_BAU.columns.to_list()

"""
activity_BAU = activity_BAU[['Case',
                             'Mitigation Case',
                             'Sector',
                             'Subsector',
                             'End Use Application',
                             'Scope',
                             'Energy carrier',
                             'Energy carrier type',
                             'Basis',
                             'Fuel Pool',
                             'Year',
                             'Formula',
                             'Emissions Category, Detailed',
                             'Emissions Category, Aggregate',
                             'Emissions Unit',
                             'Total Emissions',
                             'LCIA_estimate']]
"""

# Aboveground Carbon Stock Changes from Biomass Resources
#activity_ref_mtg.to_csv(interim_path_prefix + '\\' + 'test.csv')
# Carbon fraction Biofuels
temp_df = activity_ref_mtg.copy()

# Determine Change in Aboveground Carbon Stocks, based on differences in fuel consumption
temp_df = pd.merge(temp_df,corr_carbon_content_biofuels, how = 'inner')
temp_df['LULUCF'] = temp_df['Value'] * temp_df['Carbon Content (MMmt CO2 / MMBtu)']
temp_df = temp_df[['Energy carrier', 'Energy carrier type', 'Case', 'Value', 'Year', 'LULUCF']]

mit_case_biofuels = temp_df.groupby(['Year'], as_index = False)['LULUCF'].sum()
mit_case_biofuels['Change in Abv C Stock_Mit'] =  mit_case_biofuels['LULUCF']

# Append Updates to Env Matrix
mit_case_biofuels = mit_case_biofuels.drop(columns = {'LULUCF'})
mit_case_biofuels = mit_case_biofuels.rename(columns = {'Change in Abv C Stock_Mit': 'LCIA_estimate'})
mit_case_biofuels['Case'] = 'Mitigation'
mit_case_biofuels['Mitigation Case'] = 'Biofuels, Changes in Above C stock'
mit_case_biofuels['Sector'] = 'LULUCF'
mit_case_biofuels['Subsector'] = 'Changes in Aboveground C stock'
mit_case_biofuels['End Use Application'] = 'Biofuel use, aboveground C'
mit_case_biofuels['Scope'] = 'Direct, Non-Combustion'
mit_case_biofuels['Energy carrier'] = '-'
mit_case_biofuels['Energy carrier type'] = '-'
mit_case_biofuels['Basis'] = '-'
mit_case_biofuels['Fuel Pool'] = '-'
mit_case_biofuels['Formula'] = 'CO2'
mit_case_biofuels['Emissions Category, Detailed'] = 'CO2'
mit_case_biofuels['Emissions Category, Aggregate'] = 'CO2'
mit_case_biofuels['Emissions Unit'] = 'mmmt'
mit_case_biofuels['Total Emissions'] = mit_case_biofuels['LCIA_estimate']

# Create rest of the empty columns
mit_case_biofuels [ list(( Counter(activity_BAU.columns) - Counter(mit_case_biofuels.columns )).elements()) ] = '-'

# Drop not needed columns
mit_case_biofuels = mit_case_biofuels[activity_BAU.columns].copy()

activity_BAU = pd.concat([activity_BAU, mit_case_biofuels], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)


'''
Use the following code if changes are made to which biofuel pools are considered in the calculation of 'Above Ground Biomass'

baseline_case_biofuels = temp_df[(temp_df['Case'] == 'Reference case') & (temp_df['Year'] == 2020)]
baseline_case_biofuels =  baseline_case_biofuels.groupby(['Year'], as_index = False)['LULUCF'].sum()

ref_case_biofuels = temp_df[(temp_df['Case'] == 'Reference case')]
ref_case_biofuels = ref_case_biofuels.groupby(['Year'], as_index = False)['LULUCF'].sum()
ref_case_biofuels['Change in Abv C Stock_Ref'] =  ref_case_biofuels['LULUCF'] - baseline_case_biofuels.loc[0,'LULUCF']

mit_case_biofuels = temp_df.groupby(['Year'], as_index = False)['LULUCF'].sum()
mit_case_biofuels = pd.merge(mit_case_biofuels, ref_case_biofuels[['Change in Abv C Stock_Ref', 'Year']], how = 'left', on = 'Year')
mit_case_biofuels['Change in Abv C Stock_Mit'] =  mit_case_biofuels['LULUCF'] - mit_case_biofuels['Change in Abv C Stock_Ref']

# Append Updates to Env Matrix
ref_case_biofuels = ref_case_biofuels.drop(columns = {'LULUCF'})
ref_case_biofuels = ref_case_biofuels.rename(columns = {'Change in Abv C Stock_Ref': 'LCIA_estimate'})
ref_case_biofuels['Case'] = 'Reference case'
ref_case_biofuels['Mitigation Case'] = '-'
ref_case_biofuels['Sector'] = 'LULUCF'
ref_case_biofuels['Subsector'] = 'Changes in Aboveground C stock'
ref_case_biofuels['End Use Application'] = '-'
ref_case_biofuels['Scope'] = 'Direct, Non-Combustion'
ref_case_biofuels['Energy carrier'] = '-'
ref_case_biofuels['Energy carrier type'] = '-'
ref_case_biofuels['Basis'] = '-'
ref_case_biofuels['Fuel Pool'] = '-'
ref_case_biofuels['Formula'] = 'CO2'
ref_case_biofuels['Emissions Category, Detailed'] = 'CO2'
ref_case_biofuels['Emissions Category, Aggregate'] = 'CO2'
ref_case_biofuels['Emissions Unit'] = 'mmmt'
ref_case_biofuels['Total Emissions'] = ref_case_biofuels['LCIA_estimate']

activity_BAU = pd.concat([activity_BAU, ref_case_biofuels], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# Append Updates to Env Matrix
mit_case_biofuels = mit_case_biofuels.drop(columns = {'LULUCF',
                                                      'Change in Abv C Stock_Ref'})
mit_case_biofuels = mit_case_biofuels.rename(columns = {'Change in Abv C Stock_Mit': 'LCIA_estimate'})
mit_case_biofuels['Case'] = 'Mitigation'
mit_case_biofuels['Mitigation Case'] = 'Biofuels'
mit_case_biofuels['Sector'] = 'LULUCF'
mit_case_biofuels['Subsector'] = 'Changes in Aboveground C stock'
mit_case_biofuels['End Use Application'] = '-'
mit_case_biofuels['Scope'] = 'Direct, Non-Combustion'
mit_case_biofuels['Energy carrier'] = '-'
mit_case_biofuels['Energy carrier type'] = '-'
mit_case_biofuels['Basis'] = '-'
mit_case_biofuels['Fuel Pool'] = '-'
mit_case_biofuels['Formula'] = 'CO2'
mit_case_biofuels['Emissions Category, Detailed'] = 'CO2'
mit_case_biofuels['Emissions Category, Aggregate'] = 'CO2'
mit_case_biofuels['Emissions Unit'] = 'mmmt'
mit_case_biofuels['Total Emissions'] = mit_case_biofuels['LCIA_estimate']

activity_BAU = pd.concat([activity_BAU, mit_case_biofuels], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
'''

# Consider GHG Emissions from SOC from Cellulosic Biomass

cellulosic_etoh = activity_ref_mtg.copy()
cellulosic_etoh = cellulosic_etoh[cellulosic_etoh['Case'] == 'Mitigation']
cellulosic_etoh = cellulosic_etoh.loc[(cellulosic_etoh['Energy carrier type'].isin(['Ethanol, Cellulosic', 'ETJ, Cellulosic ethanol'])) & \
                             (~activity_ref_mtg['Energy carrier'].isin(['Renewable Diesel', 'Renewable Gasoline'])), : ]
 
# Calculate cellulosic fuel yields (Metric Tonnes Dry Biomass / MMBtu Fuel)
fuel_yields = pd.DataFrame(data = [('Ethanol, Cellulosic', 0.150),
                                   ('ETJ, Cellulosic ethanol', 0.215)],
                           columns = ['Energy carrier type', 'Fuel Yield'])

cellulosic_etoh = pd.merge(cellulosic_etoh,fuel_yields, how = 'left', on = 'Energy carrier type')

# Biomass yield (ha / Dry Metric Tonne) --> Assume 2 dt/ac for Corn Stover (Based on BT16) --> 0.20 ha / dry MT 
biomass_yield = {'Corn Stover': 0.22}

cellulosic_etoh['Biomass'] = cellulosic_etoh['Value'] * cellulosic_etoh['Fuel Yield'] * biomass_yield['Corn Stover']

# SOC Changes from Cellulosic Biomass [Units MMmt CO2] --> Assumes 0.19 MT C / (ha-yr) x 44/12 (convert from C to CO2) x 10^-6 (Convert from MT to MMmt)
soc_changes = {'Corn Stover': 6.9667*10**-7}

cellulosic_etoh['SOC Change'] = cellulosic_etoh['Biomass'] * soc_changes['Corn Stover']

mit_case_etoh_soc = cellulosic_etoh[['Year', 'SOC Change']]
mit_case_etoh_soc = mit_case_etoh_soc.rename(columns = {'SOC Change': 'LCIA_estimate'})
mit_case_etoh_soc['Case'] = 'Mitigation'
mit_case_etoh_soc['Mitigation Case'] = 'Biofuels, SOC Change'
mit_case_etoh_soc['Sector'] = 'LULUCF'
mit_case_etoh_soc['Subsector'] = 'Cropland Remaining Cropland'
mit_case_etoh_soc['End Use Application'] = 'Biofuel use, SOC change'
mit_case_etoh_soc['Scope'] = 'Direct, Non-Combustion'
mit_case_etoh_soc['Energy carrier'] = '-'
mit_case_etoh_soc['Energy carrier type'] = '-'
mit_case_etoh_soc['Basis'] = '-'
mit_case_etoh_soc['Fuel Pool'] = '-'
mit_case_etoh_soc['Formula'] = 'CO2'
mit_case_etoh_soc['Emissions Category, Detailed'] = 'CO2'
mit_case_etoh_soc['Emissions Category, Aggregate'] = 'CO2'
mit_case_etoh_soc['Emissions Unit'] = 'mmmt'
mit_case_etoh_soc['Total Emissions'] = mit_case_etoh_soc['LCIA_estimate']

# Create rest of the empty columns
mit_case_etoh_soc [ list(( Counter(activity_BAU.columns) - Counter(mit_case_etoh_soc.columns )).elements()) ] = '-'

# Drop not needed columns
mit_case_etoh_soc = mit_case_etoh_soc[activity_BAU.columns].copy()

activity_BAU = pd.concat([activity_BAU, mit_case_etoh_soc], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

#%%
"""
Reduce Emissions from Natural Gas Systems / Abandoned Mines / Landfills

"""

print("Status: Reducing emissions from natural gas systems")

# Reduce Methane emissions from Natural Gas / Petroleum Systems
# In the EIA AEO Reference case, there is already some reductions considered,
# so we need to make sure we only reduce emissions those are still hapenning (positive)

temp_list = []

years = list(range(2020, 2051))
start_yr = 2020 
end_yr = 2050
min_val = 0 
target_methane_leak_reduction_NGsystems = 0.30
k = 0.5
a = 1
for year in years:    
    x_0 = int ( (start_yr + end_yr) /2 )
    val = min_val + (target_methane_leak_reduction_NGsystems - min_val) * pow((1 / (1 + np.exp( -k * (year - x_0)))), a) 
    temp_list.append(val)

ch4_mit_rate_og = pd.DataFrame(data = list(zip(temp_list, years)), columns = ['Methane Reduction %', 'Year'] )

mtg_og_ch4 = activity_BAU.copy()
mtg_og_ch4 = mtg_og_ch4.loc[(mtg_og_ch4['Formula'] == 'CH4') \
                            & (mtg_og_ch4['Case'] == 'Reference case') \
                            & (mtg_og_ch4['Scope'] == 'Direct, Non-Combustion') \
                            & (mtg_og_ch4['Subsector'].isin(['Natural Gas Systems', 'Petroleum Systems']))
                            & ~(mtg_og_ch4['End Use Application'].isin(mtg_og_ch4.loc[mtg_og_ch4['LCIA_estimate'] <= 0, 'End Use Application'].drop_duplicates())), : ]
mtg_og_ch4 = pd.merge(mtg_og_ch4, ch4_mit_rate_og, how = 'left', on = 'Year')

mtg_og_ch4['LCIA_estimate'] = -1 * mtg_og_ch4['LCIA_estimate'] * mtg_og_ch4['Methane Reduction %'] 
mtg_og_ch4['Case'] = 'Mitigation'
mtg_og_ch4['Mitigation Case'] = 'Reduction in Fugitive Methane emissions from O&G'

mtg_og_ch4.drop(columns = {'Methane Reduction %'}, inplace = True)

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_og_ch4], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# Reduce Methane emissions from Abandoned Wells

print("Status: Reduce methane emissions from abandoned wells")

temp_list = []

years = list(range(2020, 2051))
start_yr = 2020 
end_yr = 2050
min_val = 0 
target_methane_leak_reduction_abandoned_wells = 1
k = 0.5
a = 1
for year in years:
    x_0 = int ( (start_yr + end_yr) /2 )
    val = min_val + (target_methane_leak_reduction_abandoned_wells - min_val) * pow((1 / (1 + np.exp( -k * (year - x_0)))), a) 
    temp_list.append(val)

ch4_mit_rate_ab_wells = pd.DataFrame(data = list(zip(temp_list, years)), columns = ['Methane Reduction %', 'Year'] )

mtg_ab_wells_ch4 = activity_BAU.copy()
mtg_ab_wells_ch4 = mtg_ab_wells_ch4.loc[(mtg_ab_wells_ch4['Formula'] == 'CH4') \
                                      & (mtg_ab_wells_ch4['Case'] == 'Reference case') \
                                      & (mtg_ab_wells_ch4['Scope'] == 'Direct, Non-Combustion') \
                                      & (mtg_ab_wells_ch4['Subsector'].isin(['Abandoned Oil and Gas Wells'])), : ]
mtg_ab_wells_ch4 = pd.merge(mtg_ab_wells_ch4, ch4_mit_rate_ab_wells, how = 'left', on = 'Year')

mtg_ab_wells_ch4['LCIA_estimate'] = -1 * mtg_ab_wells_ch4['LCIA_estimate'] * mtg_ab_wells_ch4['Methane Reduction %'] 
mtg_ab_wells_ch4['Case'] = 'Mitigation'
mtg_ab_wells_ch4['Mitigation Case'] = 'Reduction in Fugitive Methane emissions from Abandoned Wells'

mtg_ab_wells_ch4.drop(columns = {'Methane Reduction %'}, inplace = True)

# Drop not needed columns
mtg_ab_wells_ch4 = mtg_ab_wells_ch4[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_ab_wells_ch4], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
    
# Reduce Methane emissions from Landills

print("Status: Reduce methane emissions from Landfills")

biofuel_lfg = activity_ref_mtg.loc[activity_ref_mtg['Energy carrier type'].isin(['FT-Synthesis, Landfill gas']), : ].copy()
biofuel_lfg['Frac'] = biofuel_lfg['Value'] / biofuel_lfg['Value'].max()
biofuel_lfg = biofuel_lfg[['Year', 'Frac']]
biofuel_lfg = biofuel_lfg.groupby(['Year'], as_index=False).agg({'Frac':'mean'})

mtg_lfg = activity_BAU.copy()
mtg_lfg = mtg_lfg[(mtg_lfg['Formula'] == 'CH4') \
                  & (mtg_lfg['Case'] == 'Reference case') \
                  & (mtg_lfg['Scope'] == 'Direct, Non-Combustion') \
                  & (mtg_lfg['Subsector'].isin(['Landfills']))]
mtg_lfg = pd.merge(mtg_lfg, biofuel_lfg, how = 'left', on = 'Year')
mtg_lfg = mtg_lfg.loc[~mtg_lfg['Frac'].isna(), : ]

mtg_lfg['LCIA_estimate'] = -1 * mtg_lfg['LCIA_estimate'] * mtg_lfg['Frac'] 
mtg_lfg['Case'] = 'Mitigation'
mtg_lfg['Mitigation Case'] = 'Biofuels, Reduction in Fugitive Methane Emissions from Landfills'

mtg_lfg.drop(columns = {'Frac'}, inplace = True)

# Drop not needed columns
mtg_lfg = mtg_lfg[activity_BAU.columns].copy()

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_lfg], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time)) 


#%%
"""
Post Processing

"""
print("Status: Add in GREET Supply Chain Impacts for activity changes in mitigation scenarios..")

# Reference case supply chain emissions are already accounted in EPA GHGI non-combustion emissions.

# Calculate GREET EF's as a function of Carbon Intensity (CI) of Electricity
elec_ci = elec_gen_em_agg[['Case', 
                           'Year',
                           'Formula',
                           'CI']]

elec_ci = elec_ci[(elec_ci['Case'] == 'Mitigation') & ~(elec_ci['Formula'] == 'SF6')]


elec_ci = elec_ci[['Year',
                   'Formula',
                   'CI',
                   'Case']]

greet_ts_ef = pd.merge(ef_greet_supply_chain, elec_ci, how = 'left', on = ['Year', 'Formula']).reset_index(drop=True)
greet_ts_ef.drop(columns=['Case_x'], inplace=True)
greet_ts_ef.rename(columns={'Case_y' : 'Case'}, inplace=True)
greet_ts_ef['EF'] = greet_ts_ef['Zero Elec Comb'] + greet_ts_ef['CI'] * greet_ts_ef['Factor']

# Filter End Demand matrix to consider non-electricity flows (electricity-based impacts will be handeled seperately)
temp_df = activity_ref_mtg.copy()    
temp_df = temp_df[(temp_df['Case'] == 'Mitigation') & \
                  ~(temp_df['Energy carrier'] == 'Electricity')]
temp_df = temp_df[~(temp_df['Energy carrier'] == 'Electricity')]
temp_df['Scope'] = "Supply Chain"

temp_df_merge = pd.merge(temp_df, corr_ef_greet_supply_chain, how = 'left', on = ['Sector',
                                                    'Subsector',
                                                    'Scope',
                                                    'Energy carrier',
                                                    'Energy carrier type',
                                                    'End Use Application']).reset_index(drop=True)

temp_df_merge = temp_df_merge.loc[~(temp_df_merge['GREET Pathway'].isnull()), :]

temp_df_merge = pd.merge(temp_df_merge, greet_ts_ef, how = 'left', on = ['GREET Pathway',
                                                     'Year',
                                                     'Case',
                                                     'Scope']
                                                     ).reset_index(drop=True)

temp_df_merge['Total Emissions'] = temp_df_merge['Value'] * temp_df_merge['EF']                                                       
temp_df_merge['Total Emissions'] = temp_df_merge['Total Emissions'] *(10**-12) # convert from g to MMmt

mtg_supply_chain = pd.merge(temp_df_merge, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
mtg_supply_chain['LCIA_estimate'] = mtg_supply_chain['Total Emissions'] * mtg_supply_chain['GWP']

# Concatenating to main Environment matrix
activity_BAU = pd.concat([activity_BAU, mtg_supply_chain], axis=0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)
    
print( '    Elapsed time: ' + str(datetime.now() - init_time)) 

#%%
"""
Post Processing

"""

print("Status: Reformatting Results Dataframes ..")

# Map energy carrier types which are blanks
ec_petroleum = ['Propane',
                'Still Gas',
                'Other Petroleum',
                'Diesel',
                'Hydrocarbon Gas Liquid Feedstocks',
                'Petrochemical Feedstocks']

ec_br = ['Biofuels Heat and Coproducts', 'Renewables']

activity_BAU.loc[activity_BAU['Energy carrier'].isin (ec_petroleum), 'Energy carrier type'] = 'Petroleum'
activity_BAU.loc[activity_BAU['Energy carrier'].isin(ec_br), 'Energy carrier type'] = 'Biofuels and Renewables'

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# Map flows to new 'Waste' sector 

# Create list of specific waste sources
wastes = ['Anaerobic Digestion at Biogas Facilities',
          'Composting',
          'Landfills',
          'Wastewater Treatment and Discharge']

activity_BAU.loc[activity_BAU['Subsector'].isin(wastes), 'Sector'] = 'Waste'

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# Map Non-Combustion Sources to Specific Inventory Sectors

temp_df = activity_BAU.loc[activity_BAU['Sector'].isin(corr_ghgi_sources_EERE['Sector']) & 
                 activity_BAU['Subsector'].isin(corr_ghgi_sources_EERE['Subsector']), :]
temp_df = pd.merge(temp_df, corr_ghgi_sources_EERE, how='left', on=['Sector', 'Subsector']).reset_index(drop=True)
temp_df.drop(columns=['Sector', 'Subsector', 'End Use Application'], inplace=True)
temp_df.rename(columns={'DECARB_Sector' : 'Sector',
                        'DECARB_Subsector' : 'Subsector',
                        'DECARB_End Use Application' : 'End Use Application'}, inplace=True)

activity_BAU = activity_BAU.loc[~( activity_BAU['Sector'].isin(corr_ghgi_sources_EERE['Sector']) & 
                                   activity_BAU['Subsector'].isin(corr_ghgi_sources_EERE['Subsector']) ), :]
activity_BAU = pd.concat([activity_BAU, temp_df], axis = 0).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# Use 'Assigned' Column

col_names = ['Sector', 'Scope', 'Assigned Sector']

data = [('Agriculture', 'Direct, Combustion', 'Agriculture'),
        ('Agriculture', 'Direct, Non-Combustion', 'Agriculture'),
        ('Agriculture', 'Electricity, Combustion', 'Agriculture'),
        ('Agriculture', 'Supply Chain', 'Industrial'),
        ('Residential', 'Direct, Combustion', 'Residential'),
        ('Residential', 'Direct, Non-Combustion', 'Residential'),
        ('Residential', 'Electricity, Combustion', 'Residential'),
        ('Residential', 'Supply Chain', 'Industrial'),
        ('Commercial', 'Direct, Combustion', 'Commercial'),
        ('Commercial', 'Direct, Non-Combustion', 'Commercial'),
        ('Commercial', 'Electricity, Combustion', 'Commercial'),
        ('Commercial', 'Supply Chain', 'Industrial'),
        ('Industrial', 'Direct, Combustion', 'Industrial'),
        ('Industrial', 'Direct, Non-Combustion', 'Industrial'),
        ('Industrial', 'Electricity, Combustion', 'Industrial'),
        ('Industrial', 'Supply Chain', 'Industrial'),
        ('Transportation', 'Direct, Combustion', 'Transportation'),
        ('Transportation', 'Direct, Non-Combustion', 'Transportation'),
        ('Transportation', 'Electricity, Combustion', 'Transportation'),
        ('Transportation', 'Supply Chain', 'Industrial'),
        ('LULUCF', 'Direct, Combustion', 'LULUCF'),
        ('LULUCF', 'Direct, Non-Combustion', 'LULUCF'),
        ('LULUCF', 'Electricity, Combustion', 'LULUCF'),
        ('LULUCF', 'Supply Chain', 'Industrial'),
        ('Waste', 'Direct, Combustion', 'Waste'),
        ('Waste', 'Direct, Non-Combustion', 'Waste'),
        ('Waste', 'Electricity, Combustion', 'Waste'),
        ('Waste', 'Supply Chain', 'Industrial')]

assign_sectors = pd.DataFrame(data = data, columns = col_names)

activity_BAU = pd.merge(activity_BAU, assign_sectors, how = 'left', on = ['Sector', 'Scope']).reset_index(drop=True)

# Save interim and final environmental matrix
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out].to_csv(output_path_prefix + '\\' + f_out_env)

# apply mask for aggregated and disaggregated emissions types

activity_BAU = activity_BAU.drop(columns = {'Emissions Category, Detailed',
                                            'Emissions Category, Aggregate'})

activity_BAU = pd.merge(activity_BAU, corr_ghgs, how = 'left', on = 'Formula').reset_index(drop=True)

cols_env_out_v2 = ['Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 
                'Scope', 'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool',
                'Year', 'Formula', 'Emissions Category, Detailed', 'Emissions Category, Aggregate',
                'Emissions Unit', 'Total Emissions', 'LCIA_estimate', 'Assigned Sector']                        


# updating rows with blank or empty subsector and end use applications
activity_BAU.loc[(activity_BAU['Sector'].isin(['Residential', 'Commercial'])) & 
                 (activity_BAU['Subsector'] == '-') &
                 (activity_BAU['End Use Application'] == '-'), ['Subsector', 'End Use Application']] = 'Other Building Uses'

activity_BAU.loc[(activity_BAU['Sector'].isin(['Residential', 'Commercial'])) & 
                 (activity_BAU['Subsector'] == '-'), 'Subsector'] = 'Building Mechanicals and Electricals'

activity_BAU.loc[(activity_BAU['Sector'].isin(['Agriculture'])) & 
                 (activity_BAU['Subsector'] == '-'), 'Subsector'] = 'On farm Activities'

activity_BAU.loc[(activity_BAU['End Use Application'] == '-, -') |
                 (activity_BAU['End Use Application'] == '-') |
                 (activity_BAU['End Use Application'].isna()), 'End Use Application'] = 'Other End Uses'

"""
activity_BAU.loc[activity_BAU['Sector'].isin(['Glass Industry', 
                                               'Bulk Chemical Industry',
                                               'Other Manufacturing Industry',
                                               'Iron and Steel Industry',
                                               'Aluminum Industry',
                                               'Metal Based Durables Industry']), 'Subsector'] = \
                activity_BAU.loc[activity_BAU['Sector'].isin(['Glass Industry', 
                                                              'Bulk Chemical Industry',
                                                              'Other Manufacturing Industry',
                                                              'Iron and Steel Industry',
                                                              'Aluminum Industry',
                                                              'Metal Based Durables Industry']), 'Sector']


activity_BAU.loc[activity_BAU['Sector'].isin(['Glass Industry', 
                                               'Bulk Chemical Industry',
                                               'Other Manufacturing Industry',
                                               'Iron and Steel Industry',
                                               'Aluminum Industry',
                                               'Metal Based Durables Industry']), 'Sector'] = 'Industrial'
"""

activity_BAU.loc[activity_BAU['Sector'].isin(['Nonmanufacturing Sector']), 'Subsector'] = 'Non-manufacturing'
activity_BAU.loc[activity_BAU['Sector'].isin(['Nonmanufacturing Sector']), 'Sector'] = 'Industrial'
activity_BAU.loc[activity_BAU['Subsector'].isin(['Nonmanufacturing Sector']), 'Subsector'] = 'Non-manufacturing'

activity_BAU = activity_BAU.loc[~activity_BAU['LCIA_estimate'].isna()].copy()

if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + f_interim_env)
    activity_BAU[cols_env_out_v2].to_csv(output_path_prefix + '\\' + f_out_env)

print( '    Elapsed time: ' + str(datetime.now() - init_time)) 

