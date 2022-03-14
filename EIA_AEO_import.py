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
import os

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
        
        self.url_errors = []
        
        # Initialize a dictionary to save EIA AEO data sets
        self.EIA_data = {'energy_demand' : '',
                         'energy_supply' : '',
                         'energy_price' : '',
                         'emissions_end_use' : '',
                         'emissions_energy_type' : '',
                         'supplemental' : ''}
        
        # Create a dictionary of AEO cases, and their corresponding API Ids
        self.aeo_case_dict = {'Reference case':'AEO.2021.REF2021.'
                         #'High economic growth':'AEO.2021.HIGHMACRO.',
                         #'Low economic growth':'AEO.2021.LOWMACRO.',
                         #'High oil price':'AEO.2021.HIGHPRICE.',
                         #'Low oil price':'AEO.2021.LOWPRICE.',
                         #'High oil and gas supply':'AEO.2021.HIGHOGS.',
                         #'Low oil and gas supply':'AEO.2021.LOWOGS.',
                         #'High renewable cost':'AEO.2021.HIRENCST.',
                         #'Low renewable cost':'AEO.2021.LORENCST.',
                         }
        
        self.curr_user = getpass.getuser()
        self.api_key = pd.read_csv(self.data_path_prefix + '\\' + self.file_key, index_col=0, squeeze=True).to_dict()[self.curr_user]
        
    # Function to fetch sector-wide energy consumption and CO2 emissions    
    def eia_sector_import (self, aeo_case, df_aeo_key, tab, verbose=False): 
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
            
            try:
                df_temp = pd.DataFrame(json_data.get('series')[0].get('data'),
                                   columns = ['Year', 'Value'])
            except (Exception) as e:              
                if verbose:
                    print("Warning: Could not fetch data from: " + url)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message2 = template.format(type(e).__name__, e.args)
                if verbose:
                    print (message2)                    
                self.url_errors.append(url)                
                continue
                      
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
            
            elif tab == 'supplemental':
                df_temp['Sector'] = row['Sector']
                df_temp['Subsector'] = row['Subsector']
                df_temp['Parameter'] = row['Parameter']
                df_temp['Parameter Levels'] = row['Parameter Levels']
                df_temp['Unit'] = row['Unit']
                df_temp['Basis'] = row['Basis']
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
    def eia_multi_sector_import_web (self, aeo_cases, verbose):                     
        #Loop through every combination of AEO Case and Sector 
        for tab in self.EIA_data.keys():
            for aeo_case in aeo_cases:
                # Load in EIA's AEO Series IDs / AEO Keys
                df_aeo_key = pd.read_excel(self.data_path_prefix + '\\' + self.file_series, sheet_name = tab)
                df_aeo_key.drop_duplicates(inplace = True)
                self.eia_sector_import(aeo_case, df_aeo_key, tab, verbose)      
    
    # Function to load EIA AEO data set from disk files
    def eia_multi_sector_import_disk (self, aeo_cases):                     
        #Loop through data tables and load 
        for key in self.EIA_data.keys():
            fname = self.file_out_prefix + key + self.file_out_postfix
            self.EIA_data[key] = pd.read_csv(self.data_path_prefix + '\\' + fname)
            #self.EIA_data[key] = self.EIA_data[key][self.EIA_data[key]['AEO Case'].isin(aeo_cases)].copy()
    
    def standardize_units (self, ob_units):
        #Loop through data tables and unit convert 
        for key in self.EIA_data.keys():
            self.EIA_data[key][['Unit', 'Value']] = ob_units.unit_convert_df (self.EIA_data[key][['Unit', 'Value']].copy())
    
    # T&D loss
    def calc_TandD_loss (self, aeo_cases, load_from_disk, verbose):
        if load_from_disk:
            self.eia_multi_sector_import_disk (aeo_cases)
        else:
            self.eia_multi_sector_import_web (aeo_cases, verbose)
        
        self.net_gen = self.EIA_data['supplemental'].\
          loc[(self.EIA_data['supplemental']['Parameter'] == 'Electricity Generation') & 
              (self.EIA_data['supplemental']['Parameter Levels'] == 'Net Generation to the Grid')][['Year', 'Value', 'Unit']].\
          groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).reset_index()
          
        self.elec_import = self.EIA_data['supplemental'].\
          loc[(self.EIA_data['supplemental']['Parameter'] == 'Electricity Generation') & 
              (self.EIA_data['supplemental']['Parameter Levels'] == 'Net Imports')][['Year', 'Value', 'Unit']].\
          groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).reset_index()
          
        self.elec_sales = self.EIA_data['supplemental'].\
          loc[(self.EIA_data['supplemental']['Parameter'] == 'Electricity Sales by Sector') & 
              (self.EIA_data['supplemental']['Parameter Levels'] == 'Total')][['Year', 'Value', 'Unit']].\
          groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).reset_index()
        
        self.TandD = pd.merge(self.net_gen, self.elec_import, how='left', on='Year') 
        self.TandD.rename(columns = {
            'Value_x' : 'net_generated',
            'Value_y' : 'net_import',
            'Unit_x' : 'Unit_net_generated',
            'Unit_y' : 'Unit_net_import'}, inplace=True)
        
        self.TandD = pd.merge(self.TandD, self.elec_sales, how='left', on='Year')
        self.TandD.rename(columns = {
            'Value' : 'net_sales',
            'Unit' : 'Unit_net_sales'}, inplace=True)
        
        self.TandD['loss_frac'] = \
            1 - ( (self.TandD['net_sales'] - self.TandD['net_import']) / self.TandD['net_generated'] ) 
           
    # Function to calculate ethanol fraction by source
    def calc_ethanol_by_source (self):
        self.E_sources = self.EIA_data['supplemental'].\
          loc[(self.EIA_data['supplemental']['Parameter'] == 'Sources of Ethanol') & 
              (self.EIA_data['supplemental']['Parameter Levels'].isin(['From Corn and Other Starch', 'From Cellulose']) ) ] \
              [['Year', 'Parameter Levels', 'Value', 'Unit']].drop_duplicates()
        E_sources_agg = self.E_sources.groupby(['Year']).agg({'Value' : 'sum'}) 
        self.E_sources = pd.merge(self.E_sources, E_sources_agg, how='left', on='Year').copy()
        self.E_sources.rename(columns = {
            'Value_x' : 'E_by_source',
            'Value_y' : 'E_total'}, inplace = True)
        self.E_sources['E_frac_by_source'] = self.E_sources['E_by_source'] / self.E_sources['E_total']
        
    # Function to calculate the fraction of Ethanol in E85 fuel blend over the years
    def classify_E85 (self, aeo_cases, load_from_disk):        
        if load_from_disk:
            self.eia_multi_sector_import_disk (aeo_cases)
        else:
            self.eia_multi_sector_import_web (aeo_cases, verbose)
            
        # sum over End Use==E85, for each year
        E85_use = self.EIA_data['energy_demand'].loc[(self.EIA_data['energy_demand']['Energy carrier'] == 'E85')]
        E85_use = E85_use.groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).copy()
        Eth_use_E85 = self.EIA_data['supplemental'].loc[(self.EIA_data['supplemental']['Parameter Levels'] == 'Ethanol used in E85')][['Year', 'Value', 'Unit']].drop_duplicates()
        self.Eth_frac_E85 = pd.merge(E85_use, Eth_use_E85, how='left', on = 'Year')
        self.Eth_frac_E85.rename(columns={
            'Value_x' : 'E85_use',
            'Unit_x' : 'Unit_E85_use',
            'Value_y' : 'Eth_in_E85',
            'Unit_y' : 'Unit_Eth_in_E85'}, inplace=True)
        self.Eth_frac_E85['Eth_frac_in_E85'] =  self.Eth_frac_E85['Eth_in_E85'] /  self.Eth_frac_E85['E85_use']
        
        self.calc_ethanol_by_source()        
        self.Eth_frac_E85 = pd.merge(self.Eth_frac_E85, self.E_sources[['Year', 'Parameter Levels', 'E_frac_by_source']], how='left', on='Year')
        
    
    # Function to calculate the fraction of Ethanol in Motor Gasoline fuel blend over the years
    def classify_Egasoline (self, aeo_case, load_from_disk):
        if load_from_disk:
            self.eia_multi_sector_import_disk (aeo_case)
        else:
            self.eia_multi_sector_import_web (aeo_case, verbose)
        
        # sum over End Use=='Motor Gasoline', for each year
        Egas_use = self.EIA_data['energy_demand'].loc[(self.EIA_data['energy_demand']['Energy carrier'] == 'Motor Gasoline')]
        Egas_use = Egas_use.groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).copy()
        Eth_use_Egas = self.EIA_data['supplemental'].loc[(self.EIA_data['supplemental']['Parameter Levels'] == 'Ethanol used in Gasoline Blending')][['Year', 'Value', 'Unit']].drop_duplicates()
        self.Eth_frac_Egas = pd.merge(Egas_use, Eth_use_Egas, how='left', on = 'Year')
        self.Eth_frac_Egas.rename(columns={
            'Value_x' : 'Egas_use',
            'Unit_x' : 'Unit_Egas_use',
            'Value_y' : 'Eth_in_Egas',
            'Unit_y' : 'Unit_Eth_in_Egas'}, inplace=True)
        self.Eth_frac_Egas['Eth_frac_in_Egas'] =  self.Eth_frac_Egas['Eth_in_Egas'] /  self.Eth_frac_Egas['Egas_use']
        
        self.calc_ethanol_by_source()        
        self.Eth_frac_Egas = pd.merge(self.Eth_frac_Egas, self.E_sources[['Year', 'Parameter Levels', 'E_frac_by_source']], how='left', on='Year')
        
    # Function to calculate the fraction of Biodiesel in Distillate Blending fuel blend over the years
    def classify_BioDieselDistlBlend (self, aeo_case, load_from_disk):
        if load_from_disk:
            self.eia_multi_sector_import_disk (aeo_case)
        else:
            self.eia_multi_sector_import_web (aeo_case, verbose)
        
        # sum over End Use=='Motor Gasoline', for each year
        #DB_use = self.EIA_data['energy_demand'].loc[(self.EIA_data['energy_demand']['Energy carrier'] == 'Distillate Fuel Oil')]
        DB_use = self.EIA_data['energy_demand'].loc[(self.EIA_data['energy_demand']['Energy carrier'].isin(['Diesel', 'Distillate Fuel Oil', 'Distillates and Diesel'])) & 
                                                    (self.EIA_data['energy_demand']['Sector'] == 'Transportation') & 
                                                    (self.EIA_data['energy_demand']['Subsector'] == 'On Road') ]
        
        DB_use = DB_use.groupby(['Year', 'Unit']).agg({'Value' : 'sum'}).copy()
        BD_use_DB = self.EIA_data['supplemental'].loc[(self.EIA_data['supplemental']['Parameter Levels'] == 'Biodiesel used in Distillate Blending')][['Year', 'Value', 'Unit']].drop_duplicates()
        self.BD_frac_DB = pd.merge(DB_use, BD_use_DB, how='left', on = 'Year')
        self.BD_frac_DB.rename(columns={
            'Value_x' : 'DB_use',
            'Unit_x' : 'Unit_DB_use',
            'Value_y' : 'BD_in_DB',
            'Unit_y' : 'Unit_BD_in_DB'}, inplace=True)
        self.BD_frac_DB['BD_frac_in_DB'] =  self.BD_frac_DB['BD_in_DB'] /  self.BD_frac_DB['DB_use']
    
    # Function to calculate the energy source dependancy for Ethanol, Petroleum Gasoline, Biodiesel and Distillate
    # This function should only be ran once the classify_E85, classify_Egasoline, classify_BioDieselDistlBlend functions are called.
    def calc_EIA_fuel_denand_by_source (self):
                       
        # subset the rows for E85
        mask = self.EIA_data['energy_demand']['Energy carrier'] == 'E85'
        subset = self.EIA_data['energy_demand'][mask]
        
        # pivot the frac table for column-vector based calculations
        frac_table=pd.pivot(self.Eth_frac_E85, index=['Year', 'Eth_frac_in_E85'], columns = 'Parameter Levels', values = 'E_frac_by_source')
        frac_table.reset_index(inplace=True)
        
        # merge frac with subset EIA data
        subset = pd.merge(subset, frac_table, how='left', on='Year')
        
        # perform calculations
        subset['Petroleum Gasoline'] =  subset['Value'] * ( 1 - subset['Eth_frac_in_E85'] )
        subset['Ethanol, Cellulose'] = subset['Value'] * subset['Eth_frac_in_E85'] * subset['From Cellulose']
        subset['Ethanol, Corn and Other Starch'] = subset['Value'] * subset['Eth_frac_in_E85'] * subset['From Corn and Other Starch']
        subset = subset.loc[ : , ~subset.columns.isin(['Energy carrier type', 'Value']) ]
        subset = pd.melt(subset, id_vars = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use', 
                                   'Energy carrier', 'Classification', 'Basis', 'Unit', 'Year', 'Series Id', 'Table'],
                        value_vars = ['Ethanol, Corn and Other Starch', 'Ethanol, Cellulose', 'Petroleum Gasoline'],
                        var_name = 'Energy carrier type', value_name = 'Value').reset_index(drop=True)
        
        # save the modified rows
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'] [~mask]
        self.EIA_data['energy_demand'] = pd.concat([subset, self.EIA_data['energy_demand']], axis=0).reset_index(drop=True)
                
        # subset the rows for Egasoline
        mask = self.EIA_data['energy_demand']['Energy carrier'] == 'Motor Gasoline'
        subset = self.EIA_data['energy_demand'][mask]
        
        # pivot the frac table for column-vector based calculations
        frac_table=pd.pivot(self.Eth_frac_Egas, index=['Year', 'Eth_frac_in_Egas'], columns = 'Parameter Levels', values = 'E_frac_by_source')
        frac_table.reset_index(inplace=True)
        
        # merge frac with subset EIA data
        subset = pd.merge(subset, frac_table, how='left', on='Year')
        
        # perform calculations
        subset['Petroleum Gasoline'] =  subset['Value'] * ( 1 - subset['Eth_frac_in_Egas'] )
        subset['Ethanol, Cellulose'] = subset['Value'] * subset['Eth_frac_in_Egas'] * subset['From Cellulose']
        subset['Ethanol, Corn and Other Starch'] = subset['Value'] * subset['Eth_frac_in_Egas'] * subset['From Corn and Other Starch']
        subset = subset.loc[ : , ~subset.columns.isin(['Energy carrier type', 'Value']) ]
        subset = pd.melt(subset, id_vars = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use', 
                                   'Energy carrier', 'Classification', 'Basis', 'Unit', 'Year', 'Series Id', 'Table'],
                        value_vars = ['Ethanol, Corn and Other Starch', 'Ethanol, Cellulose', 'Petroleum Gasoline'],
                        var_name = 'Energy carrier type', value_name = 'Value').reset_index(drop=True)
        
        # save the modified rows
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'] [~mask]
        self.EIA_data['energy_demand'] = pd.concat([subset, self.EIA_data['energy_demand']], axis=0).reset_index(drop=True)
              
        # subset the rows for Biodiesel-Distillate blend
        mask = (self.EIA_data['energy_demand']['Energy carrier'].isin(['Diesel', 'Distillate Fuel Oil', 'Distillates and Diesel'])) & \
               (self.EIA_data['energy_demand']['Sector'] == 'Transportation') & \
               (self.EIA_data['energy_demand']['Subsector'] == 'On Road')
        subset = self.EIA_data['energy_demand'][mask]
                
        # merge frac with subset EIA data
        subset = pd.merge(subset, self.BD_frac_DB[['Year', 'BD_frac_in_DB']], how='left', on='Year')
        
        # perform calculations
        subset['Biodiesel'] =  subset['Value'] * subset['BD_frac_in_DB'] 
        subset['Petroleum Distillate'] =  subset['Value'] * ( 1 - subset['BD_frac_in_DB'] )
        subset = subset.loc[ : , ~subset.columns.isin(['Energy carrier type', 'Value']) ]
        subset = pd.melt(subset, id_vars = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use', 
                                   'Energy carrier', 'Classification', 'Basis', 'Unit', 'Year', 'Series Id', 'Table'],
                        value_vars = ['Biodiesel', 'Petroleum Distillate'],
                        var_name = 'Energy carrier type', value_name = 'Value').reset_index(drop=True)
        
        # save the modified rows
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'] [~mask]
        self.EIA_data['energy_demand'] = pd.concat([subset, self.EIA_data['energy_demand']], axis=0).reset_index(drop=True)
        
    
    # Save data to file, one data table per data set
    def save_EIA_data_to_file (self):
        for key in self.EIA_data.keys():
            self.EIA_data[key].to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + key + self.file_out_postfix, index = False)
            
    def save_TandD_data_to_file (self, fname = 'TandD'):
        self.TandD.to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
    
    def save_E85_data_to_file (self, fname = 'E85_frac'):
        self.Eth_frac_E85.to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
        
    def save_Egas_data_to_file (self, fname = 'Egas_frac'):
        self.Eth_frac_Egas.to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
        
    def save_BDDB_data_to_file (self, fname = 'BioDieselDistlBlend_frac'):
        self.Eth_frac_Egas.to_csv(self.data_path_prefix + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
    
    def conv_HHV_to_LHV:
        
        
    
    def EERE_data_flow_EIA_AEO (self, ob_units, fetch_data, save_to_file, verbose):
        
        if fetch_data:
            self.eia_multi_sector_import_web(self.aeo_case_dict.keys(), load_from_disk, verbose = False )
        else:
            self.eia_multi_sector_import_disk(aeo_cases = self.EIA_AEO_case_option)   
        
        self.standardize_units(ob_units)
        
        self.calc_TandD_loss(self.aeo_case_dict.keys(), load_from_disk, verbose)
        
        self.classify_E85(self.aeo_case_dict.keys(), load_from_disk)
        
        self.classify_Egasoline(self.aeo_case_dict.keys(), load_from_disk)
        
        self.classify_BioDieselDistlBlend(self.aeo_case_dict.keys(), load_from_disk)
        
        self.calc_EIA_fuel_denand_by_source()
        
        if save_to_file:
            if fetch_data:
                self.save_EIA_data_to_file()
            self.save_TandD_data_to_file()
            self.save_E85_data_to_file()
            self.save_Egas_data_to_file()
            self.save_BDDB_data_to_file()
        
# Create object and call function if script is ran directly
if __name__ == "__main__":    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    
    input_path_EIA = input_path_prefix + '\\EIA'
    input_path_units = input_path_prefix + '\\Units'
    
    save_to_file = True
    verbose = True
    load_from_disk = True
    
    # Import the unit conversion module
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    
    os.chdir (code_path_prefix)
    
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units)
    
    init_time = datetime.now()
    ob = EIA_AEO(input_path_EIA)   
    
    eia_multi_sector_df = ob.eia_multi_sector_import_web(ob.aeo_case_dict.keys(), verbose )
    ob.standardize_units(ob_units)
    
    ob.calc_TandD_loss(ob.aeo_case_dict.keys(), load_from_disk, verbose)
    
    ob.classify_E85(ob.aeo_case_dict.keys(), load_from_disk)
    
    ob.classify_Egasoline(ob.aeo_case_dict.keys(), load_from_disk)
    
    ob.classify_BioDieselDistlBlend(ob.aeo_case_dict.keys(), load_from_disk)
    
    ob.calc_EIA_fuel_denand_by_source()
    
    if save_to_file:
        ob.save_EIA_data_to_file()
        ob.save_TandD_data_to_file()
        ob.save_E85_data_to_file()
        ob.save_Egas_data_to_file()
        ob.save_BDDB_data_to_file()
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))