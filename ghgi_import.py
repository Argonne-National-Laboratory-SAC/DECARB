# -*- coding: utf-8 -*-

"""
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 01/25/2022

Summary: This python script pulls emissions data from EPA's 2019 GHGI.

"""
#%%
#Import Python Libraries

# Python Packages
import pandas as pd
import numpy as np
import seaborn as sns

#%%
#Load in GHGI Data

# Set filepath to GHGI Data
filepath = 'C:/Users/gzaimes/Desktop/EPA GHGI/Input Data/'

# Load in GHGI import sheet
df = pd.read_excel(filepath + 'ghgi_correspondence.xlsx')

#create list to append GHGI data
temp_list = [] 

# Loop through data tables in GHGI
for row in df.itertuples():
    print(row.filename)
    df_temp = pd.read_excel(filepath + "ghgi data tables/" + str(row.filename) + ".xlsx", sheet_name='Tidy')
    df_temp['Table'] = row.filename
    temp_list.append(df_temp)    

df_ghgi = pd.concat(temp_list, axis=0)
df_ghgi = df_ghgi.reset_index(drop=True)

#Remove unnecessary varibles
del temp_list, df_temp, row, df

#%%
#Load in 100-Yr GWP Factors

lcia = pd.read_excel(filepath + 'gwp factors.xlsx', sheet_name='Tidy')

#Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI. 
#NOTE - WE SHOULD ADD GWP TIME HORIZON AS SEPARATE COL**

lcia_ar4 = lcia[lcia['LCIA Method'] == 'AR4']

#%%
#Process GHGI Data

#Convert carbon flows (C) to Carbon Dioxide (CO2), e.g. C --> CO2
c_to_co2 = (16*2+12)/12

#Replace non-numeric values reported in GHGI
df_ghgi.loc[~df_ghgi["Value"].apply(np.isreal), 'Value'] = 0 

#Update GHGI C FLows --> CO2
df_ghgi.loc[df_ghgi['Emissions Type']=='C','Value'] = df_ghgi.loc[df_ghgi['Emissions Type']=='C','Value'] * c_to_co2
df_ghgi.loc[df_ghgi['Emissions Type']=='C', 'Emissions Type'] = 'CO2'

#Merge GWP factors to dataframe
df_ghgi = df_ghgi.merge(lcia_ar4, how='left', on=['Emissions Type'])

#Unit conversion (all values relative to MMmt)
unit_conv = {'kt': 10**-3,
             'mt': 10**-6,
             'MMmt': 1
             }

#Map unit conversions, and calculate GHG Emissions (MMmt CO2e)
df_ghgi['Unit Conv'] = df_ghgi['Unit'].map(unit_conv)
df_ghgi['GHG Emissions'] = df_ghgi['Value']  * df_ghgi['GWP'] * df_ghgi['Unit Conv']

#Aggregate Results by Sector and Source
df_ghgi_agg = df_ghgi.groupby(['Year', 'Inventory Sector', 'Economic Sector', 'Source'], as_index = False)['GHG Emissions'].sum()

#Remove unnecessary varibles
del lcia_ar4, unit_conv, c_to_co2

#%%
# QA/QC Check

