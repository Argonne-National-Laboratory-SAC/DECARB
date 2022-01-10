# -*- coding: utf-8 -*-
"""
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 01/08/2022

Main file

"""
#%%

# Import python packages
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date
import matplotlib.ticker as ticker
import os 

# Set working directory
wrk_dir = 'C:/Users/gzaimes/Desktop/B2B Project/Script'
os.chdir(wrk_dir)

# Import python modules
from eia_import import eia_data_import
from unit_conversion import unit_conversion

#%%

# Set the EIA API Key (used to pull EIA data). EIA API Keys can be obtained via https://www.eia.gov/opendata/
eia_api_key = '047f4916ce9b0b97f6e9a8d2fbee1c00'

# Create a dictionary, mapping EIA AEO cases to and their corresponding IDs
aeo_case_dict = {'Reference case':'AEO.2021.REF2021.',
                 'High economic growth':'AEO.2021.HIGHMACRO.',
                 'Low economic growth':'AEO.2021.LOWMACRO.',
                 'High oil price':'AEO.2021.HIGHPRICE.',
                 'Low oil price':'AEO.2021.LOWPRICE.',
                 'High oil and gas supply':'AEO.2021.HIGHOGS.',
                 'Low oil and gas supply':'AEO.2021.LOWOGS.',
                 'High renewable cost':'AEO.2021.HIRENCST.',
                 'Low renewable cost':'AEO.2021.LORENCST.',
                 }

#%%

# Set filepath to EIA demand data (e.g., EIA metadata, series ID, etc.) 
eia_path = 'C:/Users/gzaimes/Desktop/B2B Project/Input files/eia_aeo_demand.xlsx'

# Add
eia_demand = eia_data_import(sectors = ['Residential'], aeo_cases = ['Reference case'], api_key = eia_api_key, filepath = eia_path)




del eia_path

#%%

# Import Electricity LCI
elec_lci = pd.read_excel('C:/Users/gzaimes/Desktop/B2B Project/Input files/Electricity LCI.xlsx')
elec_lci_comb = elec_lci[elec_lci['Scope'] == 'Electricity, Combustion']

# Mapping
elec_mapping = pd.read_excel('C:/Users/gzaimes/Desktop/B2B Project/Input files/Electricity Mapping.xlsx')
elec_mapping.columns

# Add
eia_elec_gen = eia_data_import(sectors = ['Electric Power'], aeo_cases = ['Reference case'], api_key = eia_api_key, filepath = eia_path)

eia_elec_gen_agg = eia_elec_gen.groupby(['Year', 'Value', 'Case', 'Sector', 'End Use', 'Activity',
       'Activity Type', 'Activity Basis', 'Metric', 'Unit'], as_index = False)['Value'].sum()

eia_elec_gen_merged = eia_elec_gen_agg.merge(elec_mapping, how='left', on = ['Sector', 'End Use', 'Activity', 'Activity Type', 'Activity Basis'])
eia_elec_gen_merged[['Year']] = eia_elec_gen_merged[['Year']].astype(int)
eia_elec_gen_merged_lci = eia_elec_gen_merged.merge(elec_lci_comb, how='left', on = ['GREET Pathway', 'Year'])

eia_elec_gen_merged.dtypes
elec_lci_comb.dtypes

# Add-