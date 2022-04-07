# -*- coding: utf-8 -*-
"""
Project:EERE Decarbonization
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 03/22/2022
"""
#%%
# Python Packages
import pandas as pd

#%%

# Import Scout Mitigation Results

df = pd.read_excel('C:\\Users\\gzaimes\\Desktop\\scenario_3-1_savings_SA_data_request_v3.xlsx', header = [0,1], index_col = [0,1,2])
df = df.stack()
df.reset_index(inplace=True)
df = pd.melt(df, id_vars = ['sector', 'end_use', 'fuel', 'meas_type',] , value_name = 'Value')
df = df.rename(columns = {'sector':'Sector',
                     'end_use': 'End Use Application',
                     'fuel': 'Energy carrier',
                     'meas_type': 'Mitigation measure',
                     'year': 'Year'
                     }
          )

# Add in additional columns
df['Units'] = 'Quadrillion Btu'
df['Subsector'] = '-'

# Modify naming convention for Migitation Measure
df.loc[(df['Mitigation measure'] == 'EE_DF') & (df['Sector'] == 'Residential'),'Mitigation measure'] = 'Residential: Energy efficiency'
df.loc[(df['Mitigation measure'] == 'EE_DF') & (df['Sector'] == 'Commercial'),'Mitigation measure'] = 'Commercial: Energy efficiency'
df.loc[(df['Mitigation measure'] == 'FS') & (df['Sector'] == 'Residential'), 'Mitigation measure'] = 'Residential: Fuel switching'
df.loc[(df['Mitigation measure'] == 'FS') & (df['Sector'] == 'Commercial'), 'Mitigation measure'] = 'Commercial: Fuel switching'

df['Energy carrier'] = df['Energy carrier'].replace({'Electric': 'Electricity',
                                                     'Distillate/Other': 'Distillate Oil'}) 
