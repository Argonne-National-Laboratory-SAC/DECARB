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
input_path_corr = input_path_prefix + '\\correspondence_files'
input_path_aggriculture = input_path_prefix + '\\Agriculture'
input_path_industrial = input_path_prefix + '\\Industrial'
input_path_electricity = input_path_prefix + '\\Electricity'
input_path_GREET = input_path_prefix + '\\GREET'
input_path_units = input_path_prefix + '\\Units'
input_path_transport = input_path_prefix + '\\Transportation'
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

# Model data pull and intermediate file saving options
EIA_AEO_fetch_data = False # True for fetching EIA AEO data, False for loading pre-compiled data
EIA_AEO_save_to_file = True # True for saving fetched data and saving it to file
save_interim_files = True

# GWP assumptions
# Note: Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI.
LCIA_Method = 'AR4' # QA can use AR4, but model should be based on AR5
lcia_timeframe = 100

# EIA AEO data case
EIA_AEO_case_option = ['Reference case']

# T&D assumption, constant or calculated
T_and_D_loss_constant = True
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
from Industrial_import import Industrial
from Agriculture_import import Agriculture
from Transportation_VISION_import import Transport_Vision
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

if save_interim_files:
    ob_EPA_GHGI.df_ghgi.to_excel(interim_path_prefix + '//' + 'interim_ob_EPA_GHGI.xlsx')

# NREL Electricity generation data import
ob_elec = NREL_elec( ob_units, input_path_electricity, input_path_corr )

# GREET emission factor load
ob_ef = GREET_EF(input_path_GREET )
                      
# Data tables for correspondence across data sets
corr_EF_GREET = pd.read_excel(input_path_corr + '\\' + f_corr_ef_greet, sheet_name = sheet_corr_ef_greet, header = 3)

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
ob_ef.ef = pd.merge(corr_EF_GREET.loc[:, ~ corr_EF_GREET.columns.isin(['GREET Tab', 'GREET Version'])],
                    ob_ef.ef,
                    how='left',on=['GREET Pathway', 'Scope']).reset_index(drop=True)

ob_ef.ef.to_excel(interim_path_prefix + '\\' + 'temp_ef.xlsx')

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

if save_interim_files == True:
    electric_gen.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen.xlsx')

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

"""
# Adding GHG emissions from incineration of waste from EPA's GHGI, 

EPA_GHGI_maxyear = np.max(ob_EPA_GHGI.df_ghgi['Year'])
EPA_GHGI_addn_em = ob_EPA_GHGI.df_ghgi.loc[(ob_EPA_GHGI.df_ghgi['Source'].isin(
    ['Incineration of Waste', 
     'Electrical Transmission and Distribution', 
     'Other Process Uses of Carbonates'])) & 
   (ob_EPA_GHGI.df_ghgi['Year'] == EPA_GHGI_maxyear) ]

EPA_GHGI_addn_em_agg = EPA_GHGI_addn_em.groupby(['Emissions Type', 'Unit']).agg({'GHG Emissions' : 'sum'}).reset_index()
         
# unit conversion
EPA_GHGI_addn_em_agg [['Unit', 'GHG Emissions']] = ob_units.unit_convert_df (
    EPA_GHGI_addn_em_agg [['Unit', 'GHG Emissions']], Unit='Unit', Value='GHG Emissions', if_given_unit = True, 
    given_unit = electric_gen_ef['EF_Unit (Numerator)'].unique()[0]).copy()

EPA_GHGI_addn_em_agg.rename(columns={'Emissions Type' : 'Formula',
                                     'Unit' : 'EF_Unit (Numerator)',
                                     'GHG Emissions' : 'Total Emissions'}, inplace=True)

EPA_GHGI_addn_em_agg[['AEO Case',
                      'Case',
                      'GREET Pathway',
                      'Sector',
                      'Subsector',
                      'End Use Application',
                      'Energy carrier',
                      'Energy carrier type',
                      'Basis',
                      'Fuel Pool',
                      'Generation Type',
                      'Year',
                      'Energy Unit',
                      'Electricity Production',
                      'Scope',
                      'Flow Name',
                      'EF_Unit (Denominator)', 
                      'EF_withElec'
                      ]] = ''
electric_gen_ef = pd.concat([EPA_GHGI_addn_em_agg, electric_gen_ef], axis = 0).reset_index(drop=True)

"""

if save_interim_files == True:
    electric_gen_ef.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen_emissions.xlsx')

# Aggregrate emissions
electric_gen_ef_agg = electric_gen_ef.groupby(['Year', 'Sector', 'End Use Application', 'Energy carrier', 'Flow Name', 'Formula', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   
                                                
if save_interim_files == True:
    electric_gen_ef_agg.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen_emissions_agg.xlsx')
 
# merging the electricity production data with the total emissions data    
elec_gen_em_agg = pd.merge(electric_gen, electric_gen_ef_agg, how='left', on=['Year', 'Sector', 'End Use Application', 'Energy carrier']).drop(columns=['loss_frac']) 
elec_gen_em_agg.rename(columns={
    'Unit' : 'Energy Unit', 'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

# Adding GHG emissions from incineration of waste from EPA's GHGI, 

EPA_GHGI_maxyear = np.max(ob_EPA_GHGI.df_ghgi['Year'])
EPA_GHGI_addn_em = ob_EPA_GHGI.df_ghgi.loc[(ob_EPA_GHGI.df_ghgi['Source'].isin(
    ['Incineration of Waste', 
     'Electrical Transmission and Distribution', 
     'Other Process Uses of Carbonates'])) & 
   (ob_EPA_GHGI.df_ghgi['Year'] == EPA_GHGI_maxyear) ]

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
elec_gen_em_agg = elec_gen_em_agg.drop(columns=['GHG Emissions'])

elec_gen_em_agg['CI'] = elec_gen_em_agg['Total Emissions'] / elec_gen_em_agg['Electricity Production']

if save_interim_files == True:
    elec_gen_em_agg.to_csv(interim_path_prefix + '\\' + 'interim_electric_agg_CI.csv')

# Separate non-electric, non-electric NEU, and electric activities --> merge to ef data frames and calculate total emissions

activity_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] == 'Electricity',:]

activity_non_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] != 'Electricity',:]

activity_non_elec_neu = activity_non_elec.loc[activity_non_elec['Energy carrier'].isin(['Hydrocarbon Gas Liquid Feedstocks',
                                                                                        'Petrochemical Feedstocks',
                                                                                        'Lubricants',
                                                                                        'Asphalt and Road Oil']), : ]
activity_non_elec = activity_non_elec.loc[~activity_non_elec['Energy carrier'].isin(['Hydrocarbon Gas Liquid Feedstocks',
                                                                                        'Petrochemical Feedstocks',
                                                                                        'Lubricants',
                                                                                        'Asphalt and Road Oil']), : ]

# Map direct combustion wrt energy carrier for non-electric. For electric, map aggregrate CIs that we calculated and then calculate the net emissions and GWPs
activity_elec = pd.merge(activity_elec, elec_gen_em_agg[['Year', 'Energy carrier', 'Energy Unit', 'Flow Name', 'Formula', 'Emissions Unit', 'CI']], 
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

activity_elec = activity_elec[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                               'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                               'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                               'Unit', 'Value', 'CI', 'Total Emissions']]

activity_non_elec = activity_non_elec[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                               'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                               'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                               'Unit', 'Value', 'CI', 'Total Emissions']]

activity_non_elec_neu = activity_non_elec_neu[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                               'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                               'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                               'Unit', 'Value', 'CI', 'Total Emissions']]

# Arranging non-combustion emissions from EPA GHGI
print("Status: Constructing EPA GHGI emissions data frame as activity data frame ..")
# Filter latest year data from EPA GHGI
activity_non_combust = ob_EPA_GHGI.df_ghgi.loc[ob_EPA_GHGI.df_ghgi['Year'] == EPA_GHGI_maxyear, :].copy()

# preserve Category and Subcategory information in one column
activity_non_combust ['Category, Subcategory'] = activity_non_combust ['Category'].copy() + ', ' + activity_non_combust ['Subcategory'].copy()

# Select the needed columns
activity_non_combust = activity_non_combust[[
    'Economic Sector',
    'Source',
    'Segment',
    'Category, Subcategory',
    'Emissions Type',
    'Year',
    'Unit',
    'GHG Emissions'
    ]]

# Rename columns to match with activity df
activity_non_combust.rename(columns = {
    'Economic Sector' : 'Sector',
    'Source' : 'Subsector',
    'Segment' : 'Basis',
    'Category, Subcategory' : 'End Use Application',
    'Emissions Type' : 'Formula',
    'GHG Emissions' : 'Total Emissions'    ,
    'Unit' : 'Emissions Unit'
    }, inplace=True)

# Adding additional empty columns, to match with other activity df
activity_non_combust[['AEO Case', 
                      'Energy carrier',
                      'Energy carrier type',
                      'Fuel Pool',
                      'Flow Name',                      
                      'Unit',                      
                      'Value' ,
                      'CI'                              
                      ]] = '-'

# Defining values to specific columns
activity_non_combust['Case'] = 'Reference case'
activity_non_combust['Scope'] = 'Direct, Non-Combustion'
activity_non_combust['Data Source'] = 'EPA GHGI'

# Rearranging columns
activity_non_combust = activity_non_combust[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                                             'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                                             'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                                             'Unit', 'Value', 'CI', 'Total Emissions']]
# Expand data set for all the years under study
EERE_yr_min = np.min(electric_gen_ef['Year']).astype(int)
EERE_yr_max = np.max(electric_gen_ef['Year']).astype(int)

activity_non_combust['Year'] = EERE_yr_min
activity_non_combust_exp = activity_non_combust.copy()
for yr in range(EERE_yr_min+1, EERE_yr_max+1): # [a,)
    activity_non_combust['Year'] = yr
    activity_non_combust_exp = pd.concat ([activity_non_combust_exp, activity_non_combust], axis=0).copy().reset_index(drop=True)
   
activity_non_combust_exp[['Emissions Unit', 'Total Emissions']] = ob_units.unit_convert_df(activity_non_combust_exp[['Emissions Unit', 'Total Emissions']],
                                                                       Unit = 'Emissions Unit', Value = 'Total Emissions',          
                                                                       if_given_unit=True, given_unit = elec_gen_em_agg['Emissions Unit'].unique()[0])

#activity_non_combust_exp['Total Emissions'] = activity_non_combust_exp['Total Emissions'] * 1e12
#activity_non_combust_exp['Emissions Unit'] = 'g' 

# Generate the Environmental Matrix
activity_BAU = pd.concat ([activity_non_combust_exp, activity_elec, activity_non_elec, activity_non_elec_neu], axis=0).reset_index(drop=True)

# Calculate LCIA metric
activity_BAU = pd.merge(activity_BAU, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_BAU['LCIA_estimate'] = activity_BAU['Total Emissions'] * activity_BAU['GWP']

activity_BAU.loc[~activity_BAU['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_BAU.loc[~activity_BAU['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

#activity_BAU['LCIA_estimate'] = activity_BAU['LCIA_estimate'] * 1e-12 # converting grams to million metric ton
#activity_BAU['Unit'] = 'MMmt'

print("Status: Saving activity_reference case table to file ..")
if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + 'interim_activity_reference_case.csv')

activity_BAU_agg = activity_BAU.copy()
activity_BAU_agg['EIA type'] = ["Electric use activities" if x == 'Electricity, Combustion' else "Non-electric use activities" for x in activity_BAU_agg['Scope']]
activity_BAU_agg = activity_BAU_agg.groupby(['Year', 'Sector', 'EIA type', 'Formula', 'Emissions Unit']).agg({
                                            'LCIA_estimate' : 'sum'}).reset_index()

if save_interim_files == True:
    activity_BAU_agg.to_csv(interim_path_prefix + '\\' + 'interim_activity_reference_case_agg.csv')


print( 'Elapsed time: ' + str(datetime.now() - init_time))



#%%

"""
Generating Electric power mitigation scenarios
"""

print("Status: Constructing Electric generation Mitigation scenario ..")

elec_gen_mtg = ob_elec.NREL_elec['generation'].\
    groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 'Energy carrier', 'Energy Unit'], as_index=False). \
    agg({'Electricity Production' : 'sum'}).reset_index()

# Merge and calculate based on T&D loss
elec_gen_mtg = pd.merge(elec_gen_mtg, ob_eia.TandD[['Year', 'loss_frac']], how='left', on='Year')
elec_gen_mtg['Electricity Production'] = elec_gen_mtg['Electricity Production'] * (1 - elec_gen_mtg['loss_frac'])

if save_interim_files == True:
    elec_gen_mtg.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen_mtg.xlsx')

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
elec_gen_ef_mtg[['AEO Case',
                 'Basis',
                 'Fuel Pool']] = '-'

elec_gen_ef_mtg = elec_gen_ef_mtg[['AEO Case', 'Case', 'Mitigation Case', 'GREET Pathway', 'Sector', 'Subsector', 'End Use Application', 
                          'Energy carrier', 'Energy carrier type', 'Basis', 'Fuel Pool', 'Generation Type',
                          'Year', 'Energy Unit', 'Electricity Production', 'Scope', 'Flow Name', 'Formula', 
                          'EF_Unit (Numerator)', 'EF_Unit (Denominator)', 
                          'EF_withElec', 'Total Emissions']]

if save_interim_files == True:
    elec_gen_ef_mtg.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen_emissions_mtg.xlsx')

# Aggregrate emissions
electric_gen_ef_mtg_agg = elec_gen_ef_mtg.groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 'Energy carrier', 
                                                   'Flow Name', 'Formula', 'Energy Unit', 'EF_Unit (Numerator)']).\
                                                agg({'Total Emissions' : 'sum'}).reset_index()   
                                                
if save_interim_files == True:
    electric_gen_ef_mtg_agg.to_excel(interim_path_prefix + '\\' + 'interim_electric_gen_emissions_mtg_agg.xlsx')
 
# merging the electricity production data with the total emissions data    
elec_gen_em_mtg_agg = pd.merge(elec_gen_mtg, electric_gen_ef_mtg_agg, how='left', on=['Sector', 'Subsector', 'Case', 
                        'Mitigation Case', 'Year', 'Energy carrier', 'Energy Unit']).reset_index(drop=True).drop(columns=['loss_frac']) 

elec_gen_em_mtg_agg.rename(columns={
    'Formula' : 'Emissions Type',
    'Unit' : 'Energy Unit', 
    'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)

elec_gen_em_mtg_agg['CI'] = elec_gen_em_mtg_agg['Total Emissions'] / elec_gen_em_mtg_agg['Electricity Production']

if save_interim_files == True:
    elec_gen_em_mtg_agg.to_csv(interim_path_prefix + '\\' + 'interim_electric_mtg_agg_CI.csv')

#%%

elec_gen_em_mtg_agg_m = pd.merge(elec_gen_em_agg, elec_gen_em_mtg_agg, 
         how='outer', on = ['Year', 'Sector', 'Energy carrier', 'Flow Name', 'Emissions Type',
                'Energy Unit', 'Emissions Unit'] ).reset_index(drop=True)

elec_gen_em_mtg_agg_m.rename(columns={'CI_x' : 'CI_ref_case_elec', 
                                      'CI_y' : 'CI_elec_mtg',
                                      'Total Emissions_x' : 'Total Emissions_ref_case',
                                      'Total Emissions_y' : 'Total Emissions_mtg_elec',
                                      'Electricity Production_x' : 'Electricity Production_ref_case',
                                      'Electricity Production_y' : 'Electricity Production_mtg_elec'}, inplace=True)
elec_gen_em_mtg_agg_m ['CI_diff_elec_mtg_ref_case'] = elec_gen_em_mtg_agg_m  ['CI_elec_mtg'] - elec_gen_em_mtg_agg_m ['CI_ref_case_elec']

activity_mtg_elec = ob_eia.EIA_data['energy_demand'].loc[ob_eia.EIA_data['energy_demand']['Energy carrier'] == 'Electricity',:]

activity_mtg_elec = pd.merge(activity_mtg_elec, elec_gen_em_mtg_agg_m[['Case', 'Mitigation Case', 'Year', 
                                                   'Flow Name', 'Emissions Type', 
                                                   'Emissions Unit', 'Energy Unit', 
                                                   'CI_diff_elec_mtg_ref_case']], 
         how='left', on=['Year']).reset_index(drop=True)

activity_mtg_elec['Total Emissions'] = activity_mtg_elec['Value'] * activity_mtg_elec['CI_diff_elec_mtg_ref_case']

activity_mtg_elec.rename(columns={'Case_y' : 'Case',
                                  'CI_diff_elec_mtg_ref_case' : 'CI',
                                  'Emissions Type' : 'Formula'}, inplace=True)
activity_mtg_elec['Scope'] = 'Electricity, Combustion'

activity_mtg_elec = activity_mtg_elec[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                                       'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                                       'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                                       'Unit', 'Value', 'CI', 'Total Emissions']]

# Calculate LCIA metric
activity_mtg_elec = pd.merge(activity_mtg_elec, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_mtg_elec['LCIA_estimate'] = activity_mtg_elec['Total Emissions'] * activity_mtg_elec['GWP']

activity_mtg_elec.loc[~activity_mtg_elec['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']] = \
  ob_units.unit_convert_df(activity_mtg_elec.loc[~activity_mtg_elec['Emissions Unit'].isnull(), ['Emissions Unit', 'LCIA_estimate']],
   Unit = 'Emissions Unit', Value = 'LCIA_estimate',          
   if_given_category=True, unit_category = 'Emissions')

activity_BAU = pd.concat([activity_BAU, activity_mtg_elec], axis=0).reset_index(drop=True)

if save_interim_files == True:
    activity_BAU.to_csv(interim_path_prefix + '\\' + 'interim_activity_reference_mtg_case.csv')


print( 'Elapsed time: ' + str(datetime.now() - init_time))



#%%