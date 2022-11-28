# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Created on Mon Apr  4 13:42:07 2022

@author: skar
"""

import pandas as pd

input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
input_path_EPA = input_path_prefix + '\\EPA_GHGI'
input_path_EPA = input_path_EPA + '\\EPA GHGI Raw Data\\Chapter Text\\Ch 2 - Trends'

f_epa_ghgi_2_12 = 'Table 2-12.csv'

table_2_12 = pd.read_csv(input_path_EPA + '\\' + f_epa_ghgi_2_12, header = 2)

l1 = { 'Industry' : ['Direct Emissions', 'Electricity-Related'],
       'Commercial' : ['Direct Emissions', 'Electricity-Related'],
       'Residential' : ['Direct Emissions', 'Electricity-Related'],
       'Agriculture' : ['Direct Emissions', 'Electricity-Related'],
       'U.S. Territories' : [],
       'Total Emissions (Sources)' : [],
       'LULUCF Sector Net Total c' : [],
       'Net Emissions (Sources and Sinks)' : []}

l2 = { 'Direct Emissions': ['CO2', 'CH4', 'N2O', 'HFCs, PFCs, SF6, and NF3', 'HFCs b', 'HFCs'],
       'Electricity-Related' : ['CO2', 'CH4', 'N2O', 'HFCs, PFCs, SF6, and NF3', 'HFCs b', 'HFCs'] }

for key, values in l1.items():
    
    for v in values:
        
        for x in l2[v]:
            
            print (key + '  ' + v + '  ' + x)
            

table_2_12['Sector/Gas'][0]

        
