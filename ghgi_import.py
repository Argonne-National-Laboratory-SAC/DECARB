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

class EPA_GHGI_import:
    
    def __init__(self):
        
        # Load in GHGI Data

        # Set filepath to GHGI Data
        self.filepath = 'C:/Users/skar/Box/saura_self/Proj - EERE Decarbonization/data/EPA GHGI Input Data/'
        
        # Load in GHGI import sheet
        df = pd.read_excel(self.filepath + 'ghgi_correspondence.xlsx')
        
        # create list to append GHGI data
        temp_list = [] 
        
        # Loop through data tables in GHGI
        for row in df.itertuples():
            print('Currently fetching: ' + row.filename)
            df_temp = pd.read_excel(self.filepath + "ghgi data tables/" + str(row.filename) + ".xlsx", sheet_name='Tidy')
            df_temp['Table'] = row.filename
            temp_list.append(df_temp)    
        
        self.df_ghgi = pd.concat(temp_list, axis=0)
        self.df_ghgi = self.df_ghgi.reset_index(drop=True)
        
        # Load in 100-Yr GWP Factors
        self.lcia = pd.read_excel(self.filepath + 'gwp factors.xlsx', sheet_name='Tidy')

        # Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI.         
        lcia_ar4 = self.lcia[self.lcia['LCIA Method'] == 'AR4'].copy()
        lcia_ar4['GWP_years'] = 100
        

        # Process GHGI Data
        
        # Convert carbon flows (C) to Carbon Dioxide (CO2), e.g. C --> CO2
        c_to_co2 = (16*2+12)/12
        
        # Replace non-numeric values reported in GHGI
        self.df_ghgi.loc[~ self.df_ghgi["Value"].apply(np.isreal), 'Value'] = 0 
        
        # Update GHGI C FLows --> CO2
        self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C','Value'] = self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C','Value'] * c_to_co2
        self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C', 'Emissions Type'] = 'CO2'
        
        # Merge GWP factors to dataframe
        self.df_ghgi = self.df_ghgi.merge(lcia_ar4, how='left', on=['Emissions Type'])

        # Unit conversion (all values relative to MMmt)
        unit_conv = {'kt': 10**-3,
                     'mt': 10**-6,
                     'MMmt': 1
                     }
        
        # Map unit conversions, and calculate GHG Emissions (MMmt CO2e)
        self.df_ghgi['Unit Conv'] = self.df_ghgi['Unit'].map(unit_conv)
        self.df_ghgi['GHG Emissions'] = self.df_ghgi['Value']  * self.df_ghgi['GWP'] * self.df_ghgi['Unit Conv']
        
        #Aggregate results by Year, Sector, and Source
        self.df_ghgi_agg = self.df_ghgi.groupby(['Year', 'Inventory Sector', 'Economic Sector', 'Source'], as_index = False)['GHG Emissions'].sum()
                
     
    def remove_categories(self):
        
        # Removing combustion based emissions
        mask = (self.df_ghgi['Source'].str.contains('combustion', case=False, na=False))
        self.df_ghgi = self.df_ghgi [~ mask]
    
    # QA/QC Check
    
    def QA_with_table_2_10(self, yr_filter = [2019] ):
        
        self.data_2_10_agg = self.table_2_10()
        
        self.data_oth = self.df_ghgi[self.df_ghgi['Table'] != 'Table 2-10'].copy()
        self.data_oth_agg = self.data_oth.groupby(['Year', 'Economic Sector'], as_index = False)['GHG Emissions'].sum()
        
        d1 = self.data_oth_agg.merge(self.data_2_10_agg, left_on=['Year', 'Economic Sector'], right_on=['Year', 'Economic Sector'], how = 'left')
        d1.rename(columns = {'GHG Emissions_x' : 'GHG Emissions_compiled', 'GHG Emissions_y' : 'GHG Emissions_2_10'}, inplace = True)
        
        d1['Difference by'] = d1['GHG Emissions_compiled'] - d1['GHG Emissions_2_10']
        d1['perc diff'] = ( d1['GHG Emissions_compiled'] - d1['GHG Emissions_2_10'] ) / d1['GHG Emissions_2_10'] * 100
        
        d1 = d1[d1['Year'].isin(yr_filter)]
        
        return (d1)
        
    def table_2_10(self):
                
        df_temp = pd.read_excel(self.filepath + "ghgi data tables/" + "Table 2-10.xlsx", sheet_name='Table 2-10', header = 2, index_col = None)
        df_temp = pd.melt(df_temp, id_vars=['Sector/Source'])
        df_temp = df_temp[ ~ df_temp['Sector/Source'].isnull() ]
        df_temp = df_temp[ ~ df_temp['value'].isnull() ]
        df_temp = df_temp[ ~ df_temp['variable'].isin(['Percent a']) ]
        df_temp.loc[ ~ df_temp['value'].apply(np.isreal), 'value' ] = 0
        
        df_temp = df_temp[ df_temp['Sector/Source'].isin(['Transportation', \
                       'Electric Power Industry', 'Industry', 'Agriculture', 'Commercial', 'Residential', \
                       'LULUCF Sector Net Total b' ]) ]
        df_temp.rename(columns = {'Sector/Source' : 'Economic Sector', \
                                  'variable' : 'Year', 'value' : 'GHG Emissions'}, inplace = True)
        df_temp.loc[df_temp['Economic Sector'] == 'LULUCF Sector Net Total b', 'Economic Sector'] = 'LULUCF'
        df_temp.loc[df_temp['Economic Sector'] == 'Electric Power Industry', 'Economic Sector'] = 'Electric Power'
        
        #self.df_temp = df_temp
        return (df_temp)
        
        

if __name__ == "__main__":
    ob1 = EPA_GHGI_import()
    #ob1.table_2_10()
    df = ob1.QA_with_table_2_10()

