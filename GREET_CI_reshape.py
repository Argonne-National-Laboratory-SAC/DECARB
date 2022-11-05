# -*- coding: utf-8 -*-
"""
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

d1['Metric'].drop_duplicates()
d1_sub1 = d1.loc[d1['Metric'].isin(['CO2', 'CO2 (w/ C in VOC & CO)', 'CH4', 'N2O']), : ].copy()

# For Aviation and Marine, only select "CO2" and not "CO2 (w/ C in VOC & CO)" as both metrices data are available
d1_sub1 = d1_sub1.loc[(d1_sub1['source_str'].isin(['Aviation', 'Marine'])) & (d1_sub1['Metric'].isin(['CO2', 'CH4', 'N2O'])), : ].copy()


d1_sub2 = pd.melt(d1_sub1, id_vars = [              'source_str',
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
d1_sub2.rename(columns={'variable' : 'Year',
                        'value' : 'Emissions'}, inplace=True)
d1_sub2 = pd.melt(d1_sub2, id_vars = [ 'source_str',
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
                                       'Year',
                                       'Emissions'
                                       ])
d1_sub2.drop(['variable'], axis=1, inplace=True)
d1_sub2.rename(columns={'value' : 'Metric'}, inplace=True)

d1_sub2['LCIA Method'] = param_gwp

d1_sub2 = pd.merge(d1_sub2, gwp, how='left', left_on=['Metric', 'LCIA Method'], 
                   right_on=['Emissions Type', 'LCIA Method']).reset_index(drop=True)

# conversion of GHGs to CO2e
d1_sub2['Emissions'].astype(float)
d1_sub2['Emissions_CO2e'] = d1_sub2['Emissions'] * d1_sub2['GWP']
d1_sub2.drop(columns=['LCIA Method', 'GWP', 'timeframe_years', 'Emissions'], inplace=True)

# calculate summed GHGs as CO2e
d1_sub2 = d1_sub2.groupby(['source_str',
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

d1_sub2['Metric'] = 'GHGs'

# Reshape table to match origin
d1_sub3 = d1_sub2.pivot(index=['source_str', 'Scenario ID', 'Fuel Category', 'Vehicle Class',
         'Vehicle / Vessel', 'AGE Named Range', 'GREET Named Range',
         'Ethanol: Feedstock', 'Ethanol: Blend Level in Low Level Gasoline',
         'Ethanol: Blend Level in Dedicated Fuel Vehicle',
         'Biodiesel: Feedstock', 'Biodiesel: Blend Level in CIDI Fuel',
         'Renewable Diesel 2: Feedstock', 'Pyrolysis: Feedstock', 'PHEV Type',
         'EV Type', 'Jet Fuel: JetA Type', 'Jet Fuel: JetA Feedstock',
         'Jet Fuel: SPK Type', 'Jet Fuel: FT Feedstock', 'Jet Fuel: FT Biomass',
         'Jet Fuel: HRJ Feedstock', 'Jet Fuel: ETJ Plant Type',
         'Jet Fuel: ETJ Cellulosic Biomass (Standalone Facility)',
         'Jet Fuel: ETJ Biomass (Distributed Facility w/ Ethanol)',
         'Jet Fuel: STJ Feedstock', 'Jet Fuel: STJ Plant Type',
         'Marine Sector: Vessel Type', 'Marine Sector: Fuels', 'Vehicle',
         'Metric Unit', 'Functional Unit', 'LC Phase', 'Unique GREET scenarios',
         'Metric'],
                        columns='Year',
                        values='Emissions_CO2e').reset_index().copy()

#d1_sub3.columns = d1_sub3.columns.to_flat_index()
#d1_sub3.columns = d1_sub3.columns.get_level_values(0) + '_' +  str(d1_sub3.columns.get_level_values(1))

d1_sub3 = d1_sub3.T.reset_index().T.copy()
d1_sub3.columns = d1_sub3.iloc[0, : ].copy()
d1_sub3 = d1_sub3.iloc[1:, : ].copy()


# remove rows with GHG metric from original table
d2 = d1.loc[~ d1['Metric'].isin(['GHGs']), : ].reset_index(drop=True).copy()

# concat rows with the calculated GHG metric to the original table
d2 = pd.concat([d2, d1_sub3], axis=0).reset_index(drop=True)

if save_interim_files == True:
    d2.to_csv(fpath + '/' + fout_GREET_CIs, index=False)