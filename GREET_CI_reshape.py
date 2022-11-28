# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Created on Mon Oct 31 17:16:19 2022

@author: skar
"""

#%%

import pandas as pd

# Decarb 2b Project code
# Format GREET extractor data for input to the BioeconomyAGE

fpath = "C:/Users/skar/Box/saura_self/Proj - EERE Decarbonization/Decarb 2b/GREET/GREET TS 2020 - BAU scenarios_final"
fpath_corr = 'C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Data/Script_data_model/1_input_files/correspondence_files'
fpath_gwp = 'C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Data/Script_data_model/1_input_files/EPA_GHGI'

f_greet1 = 'TS_GREET1_2020.xlsm'
s_scm = 'GREET1_Scenario_Matrix'
s_lds = 'LDS_Matrix'
s_hds = 'HDS_Matrix'
s_avi = 'Aviation_Matrix'
s_mar = 'Marine_Matrix'

fcorr_ranges = 'corr_EF_GREETnames.xlsx'
scorr_ranges = 'decarb_2b'

fout_GREET_CIs = 'GREET1_all_pathways.csv'

f_gwp = 'gwp factors.xlsx'
s_gwp = 'Tidy'

f_path_GREET_supplychain = 'C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Data/Script_data_model/1_input_files/GREET'
f_GREET_supplychain = 'GREET_EF_SUPPLY_CHAIN.csv'
f_corr_GREET_supplychain = 'corr_EF_GREET_SUPPLY_CHAIN.csv'

save_interim_files = True

#%%

d_scm = pd.read_excel(fpath + '/' + f_greet1, s_scm, header=7, index_col=False)

d_scm = d_scm[['Scenario ID', 'Fuel Category', 'Vehicle Class', 'Vehicle / Vessel',
               'AGE Named Range', 'GREET Named Range',
               'Ethanol: Feedstock',
               'Ethanol: Blend Level in Low Level Gasoline'	,
               'Ethanol: Blend Level in Dedicated Fuel Vehicle',
               'Biodiesel: Feedstock', 	'Biodiesel: Blend Level in CIDI Fuel',	'Renewable Diesel 2: Feedstock', 
               'Pyrolysis: Feedstock',	'PHEV Type',
               'EV Type',	'Jet Fuel: JetA Type', 'Jet Fuel: JetA Feedstock',
               'Jet Fuel: SPK Type',
               'Jet Fuel: FT Feedstock',
               'Jet Fuel: FT Biomass',
               'Jet Fuel: HRJ Feedstock',
               'Jet Fuel: ETJ Plant Type',
               'Jet Fuel: ETJ Cellulosic Biomass (Standalone Facility)',
               'Jet Fuel: ETJ Biomass (Distributed Facility w/ Ethanol)',
               'Jet Fuel: STJ Feedstock',
               'Jet Fuel: STJ Plant Type',
               'Marine Sector: Vessel Type',
               'Marine Sector: Fuels']]

# Concatenate all data structures to one data frame
t1 = pd.read_excel(fpath + '/' + f_greet1, s_lds, header=1, index_col=False, usecols='B:AN')
t1['source_str'] = 'LDS'
t2 = pd.read_excel(fpath + '/' + f_greet1, s_hds, header=1, index_col=False, usecols='B:AN')
t2['source_str'] = 'HDS'
t3 = pd.read_excel(fpath + '/' + f_greet1, s_avi, header=1, index_col=False, usecols='B:AN')
t3['source_str'] = 'Aviation'
t4 = pd.read_excel(fpath + '/' + f_greet1, s_mar, header=1, index_col=False, usecols='B:AM')		
t4['source_str'] = 'Marine'
d = pd.concat([t1, t2, t3, t4], axis=0).reset_index(drop=True)
del t1, t2, t3, t4

# merge the scenario index table to carbon intensity table
d1 = pd.merge(d_scm.iloc[ : , ~(d_scm.columns.isin(['Fuel Category', 'Vehicle Class'])) ], d, how='right', on='Scenario ID').reset_index(drop=True)

# merge GREET names to Named Ranges
corr_names = pd.read_excel(fpath_corr + '/' + fcorr_ranges, scorr_ranges, index_col=False)
d1 = pd.merge(d1, corr_names, how='left', on='AGE Named Range').reset_index(drop=True)

if save_interim_files == True:
    d1.to_csv(fpath + '/' + fout_GREET_CIs, index=False)

#%%

# Calculating CO2e for GHG metric from CO2, CH4, N2O based on AR4
param_gwp = 'AR4'
gwp = pd.read_excel(fpath_gwp + '/' + f_gwp, s_gwp, index_col=False)

# Aviation and Marine structures contain 'CO2 (w/ C in VOC & CO)' only, so selecting it to accommodate all structures
d1_sub1 = d1.loc[d1['Metric'].isin(['CO2 (w/ C in VOC & CO)', 'CH4', 'N2O']), : ].copy()

# Rename the 'CO2 (w/ C in VOC & CO)' to CO2 for mapping
d1_sub1.loc[d1_sub1['Metric'].isin(['CO2 (w/ C in VOC & CO)']), 'Metric'] = 'CO2'

# reshape table to long form
d1_sub1 = pd.melt(d1_sub1, id_vars = [              'source_str',
                                                   'Scenario ID',
                                                 'Fuel Category',
                                                 'Vehicle Class',
                                              'Vehicle / Vessel',
                                               'AGE Named Range',
                                             'GREET Named Range',
                                            'Ethanol: Feedstock',
                    'Ethanol: Blend Level in Low Level Gasoline',
                'Ethanol: Blend Level in Dedicated Fuel Vehicle',
                                          'Biodiesel: Feedstock',
                           'Biodiesel: Blend Level in CIDI Fuel',
                                 'Renewable Diesel 2: Feedstock',
                                          'Pyrolysis: Feedstock',
                                                     'PHEV Type',
                                                       'EV Type',
                                           'Jet Fuel: JetA Type',
                                      'Jet Fuel: JetA Feedstock',
                                            'Jet Fuel: SPK Type',
                                        'Jet Fuel: FT Feedstock',
                                          'Jet Fuel: FT Biomass',
                                       'Jet Fuel: HRJ Feedstock',
                                      'Jet Fuel: ETJ Plant Type',
        'Jet Fuel: ETJ Cellulosic Biomass (Standalone Facility)',
       'Jet Fuel: ETJ Biomass (Distributed Facility w/ Ethanol)',
                                       'Jet Fuel: STJ Feedstock',
                                      'Jet Fuel: STJ Plant Type',
                                    'Marine Sector: Vessel Type',
                                          'Marine Sector: Fuels',
                                                       'Vehicle',
                                                        'Metric',
                                                   'Metric Unit',
                                               'Functional Unit',
                                                      'LC Phase',
                                        'Unique GREET scenarios']).copy()
d1_sub1.rename(columns={'variable' : 'Year',
                        'value' : 'Emissions'}, inplace=True)

d1_sub1['LCIA Method'] = param_gwp

d1_sub1 = pd.merge(d1_sub1, gwp, how='left', left_on=['Metric', 'LCIA Method'], 
                   right_on=['Emissions Type', 'LCIA Method']).reset_index(drop=True)

# conversion of GHGs to CO2e
d1_sub1['Emissions_CO2e'] = d1_sub1['Emissions'] * d1_sub1['GWP']
d1_sub1.drop(columns=['LCIA Method', 'GWP', 'timeframe_years', 'Emissions'], inplace=True)

d1_sub1.fillna('-', inplace=True)

# calculate summed GHGs as CO2e
d1_sub1 = d1_sub1.groupby(['source_str',
                           'Scenario ID', 
                           'Fuel Category', 
                           'Vehicle Class', 
                           'Vehicle / Vessel',
                           'AGE Named Range', 
                           'GREET Named Range', 
                           'Ethanol: Feedstock',
                           'Ethanol: Blend Level in Low Level Gasoline',
                           'Ethanol: Blend Level in Dedicated Fuel Vehicle',
                           'Biodiesel: Feedstock', 'Biodiesel: Blend Level in CIDI Fuel',
                           'Renewable Diesel 2: Feedstock', 
                           'Pyrolysis: Feedstock', 'PHEV Type',
                           'EV Type', 'Jet Fuel: JetA Type', 
                           'Jet Fuel: JetA Feedstock',
                           'Jet Fuel: SPK Type', 
                           'Jet Fuel: FT Feedstock', 
                           'Jet Fuel: FT Biomass',
                           'Jet Fuel: HRJ Feedstock', 
                           'Jet Fuel: ETJ Plant Type',
                           'Jet Fuel: ETJ Cellulosic Biomass (Standalone Facility)',
                           'Jet Fuel: ETJ Biomass (Distributed Facility w/ Ethanol)',
                           'Jet Fuel: STJ Feedstock', 
                           'Jet Fuel: STJ Plant Type',
                           'Marine Sector: Vessel Type', 
                           'Marine Sector: Fuels', 
                           'Vehicle', 
                           'Metric Unit', 
                           'Functional Unit',
                           'LC Phase', 
                           'Unique GREET scenarios',
                           'Year'
       ]).agg({'Emissions_CO2e' : 'sum'}).reset_index()

d1_sub1['Metric'] = 'GHGs'

# Reshape table to match origin
d1_sub1 = d1_sub1.pivot(index=['source_str', 
                               'Scenario ID', 
                               'Fuel Category', 
                               'Vehicle Class',
                               'Vehicle / Vessel', 
                               'AGE Named Range', 
                               'GREET Named Range',
                               'Ethanol: Feedstock', 
                               'Ethanol: Blend Level in Low Level Gasoline',
                               'Ethanol: Blend Level in Dedicated Fuel Vehicle',
                               'Biodiesel: Feedstock', 
                               'Biodiesel: Blend Level in CIDI Fuel',
                               'Renewable Diesel 2: Feedstock', 
                               'Pyrolysis: Feedstock', 'PHEV Type',
                               'EV Type', 
                               'Jet Fuel: JetA Type', 
                               'Jet Fuel: JetA Feedstock',
                               'Jet Fuel: SPK Type', 
                               'Jet Fuel: FT Feedstock', 
                               'Jet Fuel: FT Biomass',
                               'Jet Fuel: HRJ Feedstock', 
                               'Jet Fuel: ETJ Plant Type',
                               'Jet Fuel: ETJ Cellulosic Biomass (Standalone Facility)',
                               'Jet Fuel: ETJ Biomass (Distributed Facility w/ Ethanol)',
                               'Jet Fuel: STJ Feedstock', 
                               'Jet Fuel: STJ Plant Type',
                               'Marine Sector: Vessel Type', 
                               'Marine Sector: Fuels', 
                               'Vehicle',
                               'Metric Unit', 
                               'Functional Unit', 
                               'LC Phase', 
                               'Unique GREET scenarios',
                               'Metric'],
                        columns='Year',
                        values='Emissions_CO2e').reset_index().copy()


# remove rows with GHG metric from original table
d1 = d1.loc[~ d1['Metric'].isin(['GHGs']), : ].reset_index(drop=True).copy()

# concat rows with the calculated GHG metric to the original table
d1 = pd.concat([d1, d1_sub1], axis=0).reset_index(drop=True)

if save_interim_files == True:
    d1.to_csv(fpath + '/' + fout_GREET_CIs, index=False)
    
del d1_sub1
    
#%%

# Adding supply chain emissions to GREET CIs
CI_supplychain = pd.read_csv(f_path_GREET_supplychain + '/' + f_GREET_supplychain)
corr_CI_supplychain = pd.read_csv(fpath_corr + '/' + f_corr_GREET_supplychain)