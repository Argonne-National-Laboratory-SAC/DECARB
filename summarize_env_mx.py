# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Created on Tue Aug  9 08:47:33 2022

@author: skar
"""

import pandas as pd

d = pd.read_excel('C:/Users/skar/Box/EERE SA Decarbonization/1. Tool/EERE Tool/Dashboard/US Decarbonization Tool - test.xlsx', 'Env Matrix', header = 3)

d1 = d.groupby(['Year', 'Sector', 'Subsector', 'Emissions Unit']).agg({'LCIA_estimate' : 'sum'}).reset_index()

d1.to_csv('C:/Users/skar/Box/saura_self/Proj - EERE Decarbonization/Net Emissions.csv', index=False)
d