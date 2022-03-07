# -*- coding: utf-8 -*-

"""
Project:EERE Decarbonization
Authors: George G. Zaimes and Saurajyoti Kar
Affiliation: Argonne National Laboratory
Date: 07/14/2021
Version: V1

Summary: This python script pulls time-series (2020-2050) data from EIA's AEO.
This data is combined with EPA's GHGI (2019), and used to project the GHG emissions
of the U.S. economy out until 2050.

Key Data Sources:
EIA AEO: https://www.eia.gov/outlooks/aeo/
EPA GHGI: https://cfpub.epa.gov/ghgdata/inventoryexplorer/chartindex.html
"""
#%%
#Import Python Libraries

import pandas as pd
import requests
import getpass
from datetime import datetime

#%%
# Set the EIA API Key (used to pull EIA data). EIA API Keys can be obtained via https://www.eia.gov/opendata/
# Create a Dictionary which maps EIA AEO cases to their API ID. AEO Cases represent different projections of the 
# U.S. Energy System. 'Looping' over the AEO dictionary, provides an easy way to extract EIA data across AEO cases.

# Obtain API Key from EIA, see URL: https://www.eia.gov/opendata/

class EIA_AEO:
    
    # class initialization function
    def __init__(self, data_path_prefix):
        
        # data and file paths
        self.data_path_prefix = data_path_prefix
        
        self.file_key = 'EIA_AEO_user_access_key.csv'
        self.file_series = 'EIA_AEO_data_series_IDs.xlsx'
        self.file_out_prefix = 'EIA Dataset-'
        self.file_out_postfix = '-.csv'
        
        # Initialize a dictionary to save EIA AEO data sets
        self.EIA_data = {'energy_demand' : '',
                         'energy_supply' : '',
                         'energy_price' : '',
                         'emissions_end_use' : '',
                         'emissions_energy_type' : ''
            }
        
        # Create a dictionary of AEO cases, and their corresponding API Ids
        self.aeo_case_dict = {'Reference case':'AEO.2021.REF2021.',
                         'High economic growth':'AEO.2021.HIGHMACRO.',
                         'Low economic growth':'AEO.2021.LOWMACRO.',
                         'High oil price':'AEO.2021.HIGHPRICE.',
                         'Low oil price':'AEO.2021.LOWPRICE.',
                         'High oil and gas supply':'AEO.2021.HIGHOGS.',
                         'Low oil and gas supply':'AEO.2021.LOWOGS.',
                         'High renewable cost':'AEO.2021.HIRENCST.',
                         'Low renewable cost':'AEO.2021.LORENCST.',
                         }
        
        self.curr_user = getpass.getuser()
        self.api_key = pd.read_csv(self.data_path_prefix + '\\' + self.file_key, index_col=0, squeeze=True).to_dict()[self.curr_user]
        
    # Function to fetch sector-wide energy consumption and CO2 emissions    
    def eia_sector_import (self, aeo_case, df_aeo_key, tab): 
        """
        Parameters
        ----------
        sectors : 
            Import EIA data for the selected U.S. sector(s). Choose one of the following options:
                'Residential',
                'Transportation',
                'Commercial',
                'Industrial',
                'Electric Power',
                'All Sectors Average',
                'Production prices'

        aeo_cases : List
            Import EIA data for the selected AEO case(s). Choose one of the following options:
                'Reference case',
                'High economic growth',
                'Low economic growth',
                'High oil price',
                'Low oil price',
                'High oil and gas supply',
                'Low oil and gas supply',
                'High renewable cost',
                'Low renewable cost',
                
        api_key : str
             Set the EIA API key. EIA API Keys can be obtained via https://www.eia.gov/opendata/
        """
               
        # Create an temporary list to store time-series results from EIA
        temp_list = []     
        
        # Each sector has multiple data series that document the end-use applications, materials, and energy consumption. 
        # Based on the user-selected sector, loop through each data series, pulling EIA data based on the series ID / API Key
        # For each series store relevant metadata and results across the 2020 to 2050 timeframe. Append the results to the
        # temporary list. After looping through all series, concatenate results into one large dataframe. This dataframe
        # contains sector-wide energy consumption        
        for idx, row in df_aeo_key.iterrows():
            series_id = self.aeo_case_dict[aeo_case] + row['Series Id']
            url = 'https://api.eia.gov/series/?api_key=' + self.api_key +'&series_id=' + series_id
            r = requests.get(url)
            json_data = r.json()
            print('Currently fetching: ' + url)
            df_temp = pd.DataFrame(json_data.get('series')[0].get('data'),
                                   columns = ['Year', 'Value'])
           
            if tab in ['energy_demand', 'energy_supply']:                
                df_temp['Sector'] = row['Sector']
                df_temp['Subsector'] = row['Subsector']
                df_temp['End Use'] = row['End Use']
                df_temp['Energy carrier'] = row['Energy carrier']
                df_temp['Energy carrier type'] = row['Energy carrier type']
                df_temp['Classification'] = row['Classification']
                df_temp['Basis'] = row['Basis']
                df_temp['Unit'] = row['Unit']
                df_temp['Data Source'] = row['Data Source']
                df_temp['AEO Case'] = aeo_case
                df_temp['Series Id'] = series_id
                df_temp['Table'] = row['Table']
                                
            elif tab == 'energy_price':
                df_temp['Energy carrier'] = row['Energy carrier']
                df_temp['Cost basis'] = row['Cost basis']
                df_temp['Unit'] = row['Unit']
                df_temp['Basis'] = row['Basis']
                df_temp['Data Source'] = row['Data Source']
                df_temp['Series Id'] = row['Series Id']
                df_temp['Table'] = row['Table']
            
            elif tab == 'emissions_end_use':
                df_temp['Sector'] = row['Sector']
                df_temp['Subsector'] = row['Subsector']
                df_temp['End Use'] = row['End Use']
                df_temp['Basis'] = row['Basis']
                df_temp['Unit'] = row['Unit']
                df_temp['Emissions Type'] = row['Emissions Type']
                df_temp['Data Source'] = row['Data Source']
                df_temp['AEO Case'] = aeo_case
                df_temp['Series Id'] = series_id
                df_temp['Table'] = row['Table']
            
            elif tab == 'emissions_energy_type':
                df_temp['Sector'] = row['Sector']
                df_temp['Energy Type'] = row['Energy Type']
                df_temp['Basis'] = row['Basis']
                df_temp['Unit'] = row['Unit']
                df_temp['Emissions Type'] = row['Emissions Type']
                df_temp['Data Source'] = row['Data Source']
                df_temp['AEO Case'] = aeo_case
                df_temp['Series Id'] = series_id
                df_temp['Table'] = row['Table']
            
            temp_list.append(df_temp)
        
        if isinstance(self.EIA_data[tab], pd.DataFrame):
            self.EIA_data[tab] = pd.concat ((self.EIA_data[tab], pd.concat(temp_list, axis=0).reset_index(drop=True).copy()), axis=0 )
        else:
            self.EIA_data[tab] = pd.concat(temp_list, axis=0).reset_index(drop=True).copy()       
    
    # Use the function to create datasets for sector-specific and AEO cases: 
    #eia_sector_df = eia_sector_import(sector = 'Residential', aeo_case = 'Reference case')
    
    # Function to store results across multiple combinations of AEO-cases and sectors    
    def eia_multi_sector_import_web (self, aeo_cases):                     
        #Loop through every combination of AEO Case and Sector 
        for tab in self.EIA_data.keys():
            for aeo_case in aeo_cases:
                # Load in EIA's AEO Series IDs / AEO Keys
                df_aeo_key = pd.read_excel(self.data_path_prefix + '\\' + self.file_series, sheet_name = tab)
                self.eia_sector_import(aeo_case, df_aeo_key, tab)      
    
    # Function to load EIA AEO data set from disk files
    def eia_multi_sector_import_disk (self, aeo_cases):                     
        #Loop through data tables and load 
        for key in self.EIA_data.keys():
            fname = self.file_out_prefix + key + self.file_out_postfix
            self.EIA_data[key] = pd.read_csv(self.data_path_prefix + '\\' + fname)
            self.EIA_data[key] = self.EIA_data[key].loc[self.EIA_data[key]['AEO Case'] in aeo_cases].copy()
        
    # Save data to file, one data table per data set
    def save_data_to_file (self):
        for key in self.EIA_data.keys():
            self.EIA_data[key].to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + key + self.file_out_postfix, index = False)
    
    def standardize_units (self, ob_units):
        #Loop through data tables and unit convert 
        for key in self.EIA_data.keys():
            self.EIA_Data[key][['Unit', 'Value']] = ob_units.unit_convert_df (self.EIA_Data[key][['Unit', 'Value']].copy())
    
    # T&D loss
    def calc_TandD_loss (self, aeo_cases, load_from_disk):
        if load_from_disk:
            self.eia_multi_sector_import_disk (aeo_cases)
        net_gen = self.EIA_data['energy_supply'].groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).reset_index()
        elec_purchased = self.EIA_data['energy_demand'].groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).reset_index()
        #elec_imported
        self.TandD = pd.merge(net_gen, elec_purchased, how='left', by='Year').rename({
            'Value_x' : 'net_generated',
            'Value_y' : 'net_purchased'})
        self.TandD['loss_frac'] = 1 - ( self.TandD['net_generated'] / self.TandD['net_purchased'] ) # should we take absolute value of this number as it will be negative?

# Create object and call function if script is ran directly
if __name__ == "__main__":    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model\\1_input_files\\EIA'
    save_to_file = True
    
    from  unit_conversions import model_units    
    ob_units = model_units(data_path_prefix)
    
    init_time = datetime.now()
    ob = EIA_AEO(data_path_prefix, save_to_file = True)   
    
    eia_multi_sector_df = ob.eia_multi_sector_import_web(aeo_cases = ob.aeo_case_dict.keys() )
    ob.standardize_units(ob_units)
    
    if save_to_file:
        ob.save_data_to_file()
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))