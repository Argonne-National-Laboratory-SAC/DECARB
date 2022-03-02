# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 20:08:36 2022

@author: skar
"""

#%%
# Analysis parameters

# Update the _prefix paths based on your local Box folder location

code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb' # into the Github local repository

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

# LCIA factors
f_lcia = 'gwp factors.xlsx'
f_lcia_sheet = 'Tidy'

# Declaring correlation filenames
f_eia = 'EIA Dataset.csv'
f_NREL_elec_option = 'report - All Options EFS.xlsx'
f_ef = 'GREET_EF_EERE.csv'
f_corr_eia = 'corr_EIA_EERE.csv'
f_corr_ef_greet = 'corr_EF_GREET.csv'
f_corr_fuel_pool = 'corr_fuel_pool.csv'
f_corr_elec_gen = 'corr_elec_gen.csv'

# Model data pull and intermediate file saving options
fetch_data = False # True for fetching data, False for loading pre-compiled data
save_interim_files = True

# GWP assumptions
# Note: Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI.
LCIA_Method = 'AR4'
lcia_timeframe = 100

# EIA AEO data case
EIA_AEO_case_option = ['Reference case']

# EIA AEO sectors
EIA_AEO_sectors = ['Residential',
                   'Transportation',
                   'Commercial',
                   'Industrial',
                   'Electric Power'
                   ]

# Define EIA AEO case correspondence to EERE Tool case 
EIA_EERE_case = {
    'Reference case' : 'BAU'
}

# T&D assumption, constant or calculated
T_and_D_loss_constant = True
T_and_D_loss = 0.06

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
ob_units = model_units(input_path_units)

# EIA data import
if fetch_data:
    eia_ob = EIA_AEO(save_interim_files, input_path_EIA )
    eia_data = eia_ob.eia_multi_sector_import(sectors = EIA_AEO_sectors,                                                  
                                              aeo_cases = EIA_AEO_case_option                                               
                                             )    
else:
    eia_data = pd.read_csv(input_path_EIA + '\\' + f_eia)
    eia_data = eia_data.loc[eia_data['AEO Case'].isin(EIA_AEO_case_option)]

# Industrial data import
ob_industry = Industrial(ob_units, input_path_industrial )

# Agricultural and LULUCF data import
ob_agriculture = Agriculture(input_path_aggriculture )

# Transportation (VISION) data import
ob_transport = Transport_Vision(input_path_transport )

# EPA GHGI data import << NB: EPA <-> EIA mapping can be a target at future >>`
ob_EPA_GHGI = EPA_GHGI_import(ob_units, input_path_EPA, input_path_corr )
ob_EPA_GHGI.remove_combustion_other_em() # removing 'combustion' and 'other' category emissions

if save_interim_files:
    ob_EPA_GHGI.df_ghgi.to_excel(interim_path_prefix + '//' + 'interim_ob_EPA_GHGI.xlsx')

# NREL Electricity generation data import
ob_elec = NREL_elec(f_NREL_elec_option, input_path_electricity )

# GREET emission factor load
ob_ef = GREET_EF(f_ef, input_path_GREET )

# Data tables for correspondence across data sets

corr_EIA_EERE = pd.read_csv(input_path_corr + '\\' + f_corr_eia, header = 3)
corr_EF_GREET = pd.read_csv(input_path_corr + '\\' + f_corr_ef_greet, header = 3)
corr_fuel_pool = pd.read_csv(input_path_corr + '\\' + f_corr_fuel_pool, header = 3)
corr_elec_gen = pd.read_csv(input_path_corr + '\\' + f_corr_elec_gen, header = 3)

lcia_data = pd.read_excel(input_path_EPA + '\\' + f_lcia, sheet_name = f_lcia_sheet)
         
lcia_select = lcia_data.loc[ (lcia_data['LCIA Method'] == LCIA_Method) & (lcia_data['timeframe_years'] == lcia_timeframe) ]

#%%

#%%

# Map EIA case to EERE Tool case
eia_data['Case'] = eia_data['AEO Case'].map(EIA_EERE_case)

# Merge EIA and EPA's correspondence matrix
activity = pd.merge(eia_data, corr_EIA_EERE, how='right', left_on=['Sector', 'Subsector'], 
                    right_on=['EIA: Sector', 'EIA: Subsector']).dropna().reset_index()
activity = activity.loc [:, ~activity.columns.isin(['EIA: End Use Application', 'End Use Application'])].copy()
activity.rename(columns = {'Sector_y' : 'Sector',
                           'Subsector_y' : 'Subsector', 
                           'End Use' : 'End Use Application',
                           'Energy Carrier' : 'Activity', 
                           'Date' : 'Year',                            
                           'Series Id' : 'EIA Series ID'}, inplace = True)
activity = activity [['AEO Case', 'Case', 'Sector', 'Subsector', 'End Use Application', 'Activity', 'Activity Type', 'Activity Basis', 
                      'Year', 'Unit', 'Value']]

# unit conversion
activity [['Unit', 'Value']] = ob_units.unit_convert_df (activity [['Unit', 'Value']].copy())

# Merge fuel pool
activity = pd.merge(activity, corr_fuel_pool, how='left', left_on=['Activity'],\
                    right_on=['Energy Carrier']).dropna().reset_index(drop=True)

print('Status: Constructing Electric generation activity and Emission Factors data frames ..')
    
# Extract electricity generation data from activity data frame
elec_gen = activity.loc[(activity['Sector'] == 'Electric Power') ].dropna().\
   reset_index(drop=True)

# Merge Electricity generation data with 'Electricity generation types' tags
elec_gen = pd.merge(elec_gen, corr_elec_gen, how='left', left_on=['Sector', 'Activity', 'Activity Type'],
                    right_on=['Sector', 'Activity', 'Activity Type']).\
    drop(['Index'], axis=1).reset_index(drop=True)
    

# Aggregrate electricity generation data by fuel type and by year
#elec_gen_agg =  elec_gen.groupby(['Year', 'Generation Type', 'Unit'])['Value'].sum().reset_index()

# Map with correlation matrix to GREET pathway names
temp_corr_EF_GREET = corr_EF_GREET[['Activity', 'Activity Type', 'GREET Pathway']].drop_duplicates()
ob_ef.ef = pd.merge(ob_ef.ef, temp_corr_EF_GREET, how='left',on='GREET Pathway')

# Filter combustion data for electricity generation 
ob_ef.ef_electric = ob_ef.ef.loc[ob_ef.ef['Activity Type'].isin(elec_gen['Activity Type'].unique())].drop_duplicates()
ob_ef.ef_electric = ob_ef.ef_electric.loc[ob_ef.ef['Scope'].isin(['Electricity, Combustion'])]

ob_ef.ef_electric.rename(columns = {'Unit (Numerator)' : 'EF_Unit (Numerator)',
                                    'Unit (Denominator)' : 'EF_Unit (Denominator)'}, inplace = True)

# Merge emission factors for fuel-feedstock combustion so used for electricity generation with net electricity generation
electric_ef_gen = pd.merge(ob_ef.ef_electric[['Flow Name', 'Formula', 'EF_Unit (Numerator)', 
                            'EF_Unit (Denominator)', 'Case', 'Scope', 'Year', 
                            'BAU', 'Elec0', 'Activity', 'Activity Type']], 
         elec_gen[['AEO Case', 'Case', 'End Use Application', 'Sector', 'Subsector', 'Activity', 
                   'Activity Type', 'Activity Basis', 'Year', 'Unit', 'Value', 
                   'Energy Carrier', 'Fuel Pool', 'Generation Type', 'Energy Type']],
             how='left',
             on=['Activity', 'Activity Type', 'Year', 'Case'])

# Calculate net emission by GHG species, from electricity generation    
electric_ef_gen['Total Emissions'] = electric_ef_gen['BAU'] * electric_ef_gen['Value'] 

if save_interim_files == True:
    electric_ef_gen.to_excel(interim_path_prefix + '\\' + 'interim_electric_ef_gen.xlsx')

# Add additional columns, rename columns, re-arrange columns
electric_ef_gen = electric_ef_gen.rename(columns={
                                                  'BAU' : 'EF_withElec',
                                                  'Elec0' : 'EF_Elec0',
                                                  'Value' : 'Electricity Production',
                                                  'Unit' : 'Energy Unit'
                                        })
electric_ef_gen = electric_ef_gen[['AEO Case', 'Case', 'Sector', 'Subsector', 'End Use Application', 
                          'Activity', 'Activity Type', 'Activity Basis', 'Fuel Pool', 'Case', 
                          'Year', 'Energy Unit', 'Electricity Production', 'Scope', 'Flow Name', 'Formula', 
                          'EF_Unit (Numerator)', 'EF_Unit (Denominator)', 
                          'EF_withElec', 'EF_Elec0', 'Total Emissions']]

# Aggrigration to calculate overall Electricity generation CI, combustion portion    
electric_ef_gen_agg = electric_ef_gen.groupby(['Year', 'Activity Type', 'Flow Name', \
                                               'Formula', 'Energy Unit', 'EF_Unit (Numerator)']).agg({
                                                   'Electricity Production' : 'sum', 
                                                   'Total Emissions' : 'sum'})\
                                    .reset_index()\
                                    .rename(columns = {'EF_Unit (Numerator)' : 'Emissions Unit'})
                                    
electric_ef_gen_agg['CI'] = electric_ef_gen_agg['Total Emissions'] / \
    ( electric_ef_gen_agg['Electricity Production'] * (1 - T_and_D_loss) )

if save_interim_files == True:
    electric_ef_gen_agg.to_csv(interim_path_prefix + '\\' + 'interim_electric_ef_gen_agg_1.csv')
    

# Aggregrating to calculate the net energy generation per year, and corresponding GHG emissions
electric_ef_gen_agg = electric_ef_gen_agg.groupby(['Year', 'Flow Name', 'Formula', \
                                                   'Energy Unit', 'Emissions Unit']).agg({
                                                       'Electricity Production' : 'sum',
                                                       'Total Emissions' : 'sum'}) \
                                                           .reset_index()

""" Adding GHG emissions from incineration of waste from EPA's GHGI, 
Electrical Transmission and Distribution, and Other Process Uses of Carbonates.
Values from 2019, as constant to all the years.
"""
EPA_GHGI_maxyear = np.max(ob_EPA_GHGI.df_ghgi['Year'])
EPA_GHGI_addn_em = ob_EPA_GHGI.df_ghgi.loc[(ob_EPA_GHGI.df_ghgi['Source'].isin(
    ['Incineration of Waste', 
     'Electrical Transmission and Distribution', 
     'Other Process Uses of Carbonates'])) & 
   (ob_EPA_GHGI.df_ghgi['Year'] == 2019) ]

EPA_GHGI_addn_em = EPA_GHGI_addn_em.groupby(['Year', 'Source', \
                                                                   'Emissions Type',
                                                                   'Unit'])\
                                                         .agg({
                                                             'Value' : 'sum'
                                                             }).reset_index()
# unit conversion
activity [['Unit', 'Value']] = ob_units.unit_convert_df (activity [['Unit', 'Value']].copy())

EPA_GHGI_addn_em['unit_to'] = electric_ef_gen_agg['Emissions Unit'].unique()[0]
EPA_GHGI_addn_em['unit_conv'] = EPA_GHGI_addn_em['unit_to'] + '_per_' + EPA_GHGI_addn_em['Unit'] 
EPA_GHGI_addn_em['Value'] = np.where(
     [x in ob_units.dict_units for x in EPA_GHGI_addn_em['unit_conv'] ],
     EPA_GHGI_addn_em['Value'] * EPA_GHGI_addn_em['unit_conv'].map(ob_units.dict_units),
     EPA_GHGI_addn_em['Value'] )
EPA_GHGI_addn_em.drop(['unit_conv', 'Unit'], axis = 1, inplace = True)
EPA_GHGI_addn_em.rename(columns = {'unit_to' : 'Unit'}, inplace = True)

# Merge and add to electricity emissions df 
electric_ef_gen_agg = pd.merge(electric_ef_gen_agg, EPA_GHGI_addn_em[['Emissions Type', 'Value']], 
                               how='left', left_on='Formula', right_on='Emissions Type')
electric_ef_gen_agg['Total Emissions'] = electric_ef_gen_agg['Total Emissions'] + electric_ef_gen_agg['Value']
electric_ef_gen_agg.drop(['Value'], axis=1, inplace=True) # at this stage, the total emissions represent emissions including incineration of waste.

# Recalculate the Electricity generation, combustion based CI
electric_ef_gen_agg['CI'] = electric_ef_gen_agg['Total Emissions'] / \
    ( electric_ef_gen_agg['Electricity Production'] * (1 - T_and_D_loss) )
    
if save_interim_files == True:
    electric_ef_gen_agg.to_csv(interim_path_prefix + '\\' + 'interim_electric_ef_gen_agg_2.csv')

print('Status: Constructing non-electric activity sectors as per EIA AEO data set ..')

# BAU scenario dev for non-electricity generation sectors and non-electric activities
activity_non_elec = activity.loc [~ (activity['Sector'] == 'Electric Power')]
activity_non_elec = activity_non_elec.loc [~ (activity_non_elec['Activity'] == 'Electricity')]

# Filter combustion data for electricity generation 
ob_ef.ef_non_electric = ob_ef.ef.loc[ob_ef.ef['Activity'].isin(activity_non_elec['Activity'].unique())].drop_duplicates()
ob_ef.ef_non_electric.rename(columns = {'Unit (Numerator)' : 'EF_Unit (Numerator)',
                                    'Unit (Denominator)' : 'EF_Unit (Denominator)'}, inplace = True)

# Merge emission factors for non-electric generation activites
non_electric_ef_activity = pd.merge(ob_ef.ef_non_electric[['Flow Name', 'Formula', 'EF_Unit (Numerator)', 
                            'EF_Unit (Denominator)', 'Case', 'Scope', 'Year', 
                                'BAU', 'Elec0', 'Activity']], 
         activity_non_elec[['AEO Case', 'Sector', 'Subsector', 'End Use Application',
                            'Activity', 'Activity Basis', 'Year', 'Unit', 
                            'Value', 'Energy Carrier', 'Fuel Pool']],
             how='left',
             on=['Activity', 'Year'])

# calculate total emissions
non_electric_ef_activity['Total Emissions'] = non_electric_ef_activity['BAU'] * non_electric_ef_activity['Value']
#non_electric_ef_activity.dropna(axis=1, how='all', inplace=True)

# Add additional columns, rename columns, re-arrange columns
non_electric_ef_activity[['Activity Type']] = '-'
non_electric_ef_activity = non_electric_ef_activity.rename(columns={
                                                            'BAU' : 'EF_withElec',
                                                            'Elec0' : 'EF_Elec0',
                                                            'Value' : 'Energy Estimate'
                                                          })
non_electric_ef_activity = non_electric_ef_activity[['AEO Case', 'Sector', 'Subsector', 'End Use Application', 
                          'Activity', 'Activity Type', 'Activity Basis', 'Fuel Pool', 'Case', 
                          'Year', 'Unit', 'Energy Estimate', 'Scope', 'Flow Name', 'Formula', 
                          'EF_Unit (Numerator)', 'EF_Unit (Denominator)', 
                          'EF_withElec', 'EF_Elec0', 'Total Emissions']]
 
if save_interim_files == True:
    non_electric_ef_activity.to_excel(interim_path_prefix + '\\' + 'interim_non_electric_ef_activity.xlsx')   
    

# Arranging non-combustion emissions from EPA GHGI
print("Status: Constructing EPA GHGI emissions data frame as activity data frame ..")
# Filter latest year data from EPA GHGI
activity_non_combust = ob_EPA_GHGI.df_ghgi.loc[ob_EPA_GHGI.df_ghgi['Year'] == EPA_GHGI_maxyear]

# Select the needed columns
activity_non_combust = activity_non_combust[[
    'Economic Sector',
    'Source',
    'Segment',
    'Category',
    'Subcategory',
    'Emissions Type',
    'Year',
    'Unit',
    'Value'
    ]]

# Rename columns to match with activity df
activity_non_combust = activity_non_combust.rename(columns = {
    'Economic Sector' : 'Sector',
    'Source' : 'Subsector',
    'Segment' : 'End Use Application',
    'Category' : 'Activity',
    'Subcategory' : 'Activity Basis',
    'Emissions Type' : 'Formula',
    'Value' : 'Total Emissions'    
    })

# Adding additional empty columns, to match with other activity df
activity_non_combust[['AEO Case',
                   'Activity Type',
                   'Fuel Pool',
                   'Case',
                   'Year',
                   'Energy Unit',
                   'Electricity Production',
                   'Scope',
                   'Flow Name',
                   'EF_Unit (Numerator)',
                   'EF_Unit (Denominator)',
                   'EF_withElec',
                   'EF_Elec0',
                   'Energy Estimate']] = '-'

# Defining values to specific columns
activity_non_combust['Case'] = 'BAU'
activity_non_combust['Scope'] = 'Direct, Non-Combustion'

# Rearranging columns
activity_non_combust = activity_non_combust[['AEO Case', 'Sector', 'Subsector', 'End Use Application', 
                          'Activity', 'Activity Type', 'Activity Basis', 'Fuel Pool', 'Case', 
                          'Year', 'Energy Unit', 'Electricity Production', 'Scope', 'Flow Name', 'Formula', 
                          'EF_Unit (Numerator)', 'EF_Unit (Denominator)', 
                          'EF_withElec', 'EF_Elec0', 'Total Emissions']]

# Expand data set for all the years under study
EERE_yr_min = np.min(electric_ef_gen['Year']).astype(int)
EERE_yr_max = np.max(electric_ef_gen['Year']).astype(int)

activity_non_combust['Year'] = EERE_yr_min
activity_non_combust_exp = activity_non_combust.copy()
for yr in range(EERE_yr_min+1, EERE_yr_max+1):
    activity_non_combust['Year'] = yr
    activity_non_combust_exp = pd.concat ([activity_non_combust_exp, activity_non_combust], axis=0).reset_index(drop=True)

# Generate the Environmental Matrix
activity_BAU = pd.concat ([activity_non_combust_exp, electric_ef_gen, non_electric_ef_activity], axis=0).reset_index(drop=True)

# Calculate LCIA metric
activity_BAU = pd.merge(activity_BAU, lcia_select, how='left', left_on=['Formula'], right_on=['Emissions Type'] ).reset_index(drop=True)
activity_BAU['LCIA_estimate'] = activity_BAU['Total Emissions'] * activity_BAU['GWP']

print("Status: Saving activity_BAU table to file ..")
if save_interim_files == True:
    activity_BAU.to_excel(interim_path_prefix + '\\' + 'interim_activity_BAU.xlsx')

print( 'Elapsed time: ' + str(datetime.now() - init_time))



#%%
