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
    def __init__(self, input_path_EIA, input_path_corr):
        
        print("Status: Pre-processing EIA AEO emissions data frame ..")
        
        # data and file paths
        self.input_path_EIA = input_path_EIA
        self.input_path_corr = input_path_corr
        
        self.file_key = 'EIA_AEO_user_access_key.csv'
        self.file_series = 'EIA_AEO_data_series_IDs.xlsx'
        
        self.file_corr_eia = 'corr_EIA_EERE.csv'
        self.file_corr_eia_energy_carrier = 'corr_EIA_energy_carrier.csv'
        self.file_corr_eia_fuel_pool = 'corr_fuel_pool.csv'
        self.file_corr_elec_gen = 'corr_elec_gen.csv'
        
        self.file_out_prefix = 'EIA Dataset-'
        self.file_out_postfix = '-.csv'
        self.file_out_postfix_raw = '-raw.csv'
        
        # Define EIA AEO case correspondence to EERE Tool case 
        self.EIA_EERE_case = {
            'Reference case' : 'Reference case'
        }
        
        self.url_errors = []
        
        # Initialize a dictionary to save EIA AEO data sets
        self.EIA_data = {'energy_demand' : '',
                         'energy_supply' : '',
                         #'energy_price' : '',
                         #'emissions_end_use' : '',
                         #'emissions_energy_type' : '',
                         'supplemental' : '',
                         'chemical_industry_supp' : ''
                         }
        
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
        self.api_key = pd.read_csv(self.input_path_EIA + '\\' + self.file_key, index_col=0).squeeze("columns").to_dict()[self.curr_user]
        
        # Read correspondence files
        self.corr_EIA_EERE = pd.read_csv(self.input_path_corr + '\\' + self.file_corr_eia, header = 3)
        self.corr_EIA_energy_carrier = pd.read_csv(self.input_path_corr + '\\' + self.file_corr_eia_energy_carrier, header = 3)
        self.corr_EIA_fuel_pool = pd.read_csv(self.input_path_corr + '\\' + self.file_corr_eia_fuel_pool, header = 3)
        self.corr_elec_gen = pd.read_csv(input_path_corr + '\\' + self.file_corr_elec_gen, header = 3)
        
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
            
            elif tab in ['supplemental', 'chemical_industry_supp'] :
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
       
    # Function to store results across multiple combinations of AEO-cases and sectors    
    def eia_multi_sector_import_web (self, aeo_cases, verbose):                     
        #Loop through every combination of AEO Case and Sector 
        for tab in self.EIA_data.keys():
            for aeo_case in aeo_cases:
                # Load in EIA's AEO Series IDs / AEO Keys
                df_aeo_key = pd.read_excel(self.input_path_EIA + '\\' + self.file_series, sheet_name = tab)
                df_aeo_key.drop_duplicates(inplace = True)
                self.eia_sector_import(aeo_case, df_aeo_key, tab, verbose)      
    
    # Function to load EIA AEO data set from disk files
    def eia_multi_sector_import_disk (self, aeo_cases):                     
        #Loop through data tables and load 
        for key in self.EIA_data.keys():
            fname = self.file_out_prefix + key + self.file_out_postfix_raw
            self.EIA_data[key] = pd.read_csv(self.input_path_EIA + '\\' + fname)
            #self.EIA_data[key] = self.EIA_data[key][self.EIA_data[key]['AEO Case'].isin(aeo_cases)].copy()
    
    # EERE tool based data transformations
    def transform_EERE_tool (self, ob_units, base_year = 2020):
        
        # Filter out 'Net Coke Import' when in 'Energy carrier'
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'][
            self.EIA_data['energy_demand']['End Use'] != 'Net Coke Imports']
        
        """               
        # replacing industrial flows that use natural gas for hydrogen production to hydrogen as energy carrier
        # Convert energy efficiency from natural gas to hydrogen
        self.EIA_data['energy_demand'].loc[
            (self.EIA_data['energy_demand']['End Use'].isin(['Feedstock', 'Feedstocks']) ) & 
            (self.EIA_data['energy_demand']['Energy carrier'] == 'Natural Gas'), 'Value' ] = \
        self.EIA_data['energy_demand'].loc[
            (self.EIA_data['energy_demand']['End Use'].isin(['Feedstock', 'Feedstocks']) ) & 
            (self.EIA_data['energy_demand']['Energy carrier'] == 'Natural Gas'), 'Value' ] * ob_units.feedstock_convert['NG_to_H2']
        
        self.EIA_data['energy_demand'].loc[
            (self.EIA_data['energy_demand']['End Use'].isin(['Feedstock', 'Feedstocks']) ) & 
            (self.EIA_data['energy_demand']['Energy carrier'] == 'Natural Gas'), 'Energy carrier type' ] = 'Natural Gas'
        
        self.EIA_data['energy_demand'].loc[
            (self.EIA_data['energy_demand']['End Use'].isin(['Feedstock', 'Feedstocks']) ) & 
            (self.EIA_data['energy_demand']['Energy carrier'] == 'Natural Gas'), 'Energy carrier' ] = 'Hydrogen'
        """
        # Calculate ratio for the chemical industry supp data set        
        self.EIA_data['chemical_industry_supp']['Year'] = self.EIA_data['chemical_industry_supp']['Year'].astype('int')
        self.EIA_data['chemical_industry_supp']['Value'] = self.EIA_data['chemical_industry_supp']['Value'].astype('float32')
        self.test_data = self.EIA_data['chemical_industry_supp']
        self.EIA_data['chemical_industry_supp'] = \
        pd.merge( self.EIA_data['chemical_industry_supp'],
                  self.EIA_data['chemical_industry_supp'].loc[self.EIA_data['chemical_industry_supp']['Year'] == base_year, ['Sector', 'Subsector', 'Parameter', 'Parameter Levels', 'Value']],
                  how='left',
                  on=['Sector', 'Subsector', 'Parameter', 'Parameter Levels']).reset_index(drop=True)        
       
        self.EIA_data['chemical_industry_supp']['frac_increase'] = self.EIA_data['chemical_industry_supp']['Value_x'] / self.EIA_data['chemical_industry_supp']['Value_y']
        self.EIA_data['chemical_industry_supp'].drop(columns=['Value_y'], inplace=True)
        self.EIA_data['chemical_industry_supp'].rename(columns={'Value_x' : 'Value'}, inplace=True)
       
    def standardize_units (self, ob_units):
        #Loop through data tables and unit convert 
        # ['energy_demand', 'energy_supply', 'energy_price', 'emissions_end_use', 'emissions_energy_type', 'supplemental']
        for key in ['energy_demand', 'energy_supply']:
            self.EIA_data[key][['Unit', 'Value']] = ob_units.unit_convert_df (self.EIA_data[key][['Unit', 'Value']].copy())
            
   
    def conv_HHV_to_LHV (self, aeo_cases, ob_units, verbose):
             
        self.EIA_data ['energy_demand'] = pd.merge(self.EIA_data['energy_demand'], ob_units.hv_EIA[['Energy carrier', 'Energy carrier type', 'LHV_by_HHV']], 
                                    how='left', on=['Energy carrier', 'Energy carrier type'])        
        self.EIA_data['energy_demand']['Value'] = self.EIA_data['energy_demand']['Value'] * self.EIA_data['energy_demand']['LHV_by_HHV']
        self.EIA_data['energy_demand'].drop(columns=['LHV_by_HHV'], inplace=True)
        self.EIA_data_QA = self.EIA_data.copy()
           
    # T&D loss
    def calc_TandD_loss (self, aeo_cases, verbose):
        
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
    def classify_E85 (self, aeo_cases, verbose):        
            
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
    def classify_Egasoline (self, aeo_case, verbose):
        
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
    def classify_BioDieselDistlBlend (self, aeo_case, verbose):
        
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
    def calc_EIA_fuel_demand_by_source (self):
                       
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
        subset['Ethanol, Cellulosic'] = subset['Value'] * subset['Eth_frac_in_E85'] * subset['From Cellulose']
        subset['Ethanol, Conventional'] = subset['Value'] * subset['Eth_frac_in_E85'] * subset['From Corn and Other Starch']
        subset = subset.loc[ : , ~subset.columns.isin(['Energy carrier type', 'Value']) ]
        subset = pd.melt(subset, id_vars = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use', 
                                   'Energy carrier', 'Classification', 'Basis', 'Unit', 'Year', 'Series Id', 'Table'],
                        value_vars = ['Ethanol, Conventional', 'Ethanol, Cellulosic', 'Petroleum Gasoline'],
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
        subset['Ethanol, Cellulosic'] = subset['Value'] * subset['Eth_frac_in_Egas'] * subset['From Cellulose']
        subset['Ethanol, Conventional'] = subset['Value'] * subset['Eth_frac_in_Egas'] * subset['From Corn and Other Starch']
        subset = subset.loc[ : , ~subset.columns.isin(['Energy carrier type', 'Value']) ]
        subset = pd.melt(subset, id_vars = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use', 
                                   'Energy carrier', 'Classification', 'Basis', 'Unit', 'Year', 'Series Id', 'Table'],
                        value_vars = ['Ethanol, Conventional', 'Ethanol, Cellulosic', 'Petroleum Gasoline'],
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
                              
    # Map correspondence files
    def map_corr_tables (self):      
        
        # merge EERE conventions on Sector, Subsector, and End Use Applications
        
        self.EIA_data['energy_demand'] = pd.merge(self.EIA_data['energy_demand'], self.corr_EIA_EERE,
                               how='left',
                               left_on=['Sector', 'Subsector', 'End Use'],
                               right_on=['EIA: Sector', 'EIA: Subsector', 'EIA: End Use Application']).reset_index(drop=True)
        
        # Remove duplicate columns before renaming columns
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'].loc [:, ~self.EIA_data['energy_demand'].columns.isin(['EIA: End Use Application', 'End Use'])].copy()

        # Standardize column names
        self.EIA_data['energy_demand'].rename(columns = {'Sector_y' : 'Sector',
                                                         'Subsector_y' : 'Subsector', 
                                                         'Energy Carrier' : 'Activity', 
                                                         'Date' : 'Year',                            
                                                         'Series Id' : 'EIA Series ID'}, inplace = True)
        # Rearrange columns
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'] [['Data Source', 'AEO Case', 'Sector', 'Subsector', 
                                                                          'End Use Application', 'Energy carrier', 'Energy carrier type', 'Basis', 
                                                                          'Year', 'Unit', 'Value']]
        
        # merge EERE 'energy carrier' conventions to EIA tool
        
        self.EIA_data['energy_demand'] = pd.merge(self.EIA_data['energy_demand'], self.corr_EIA_energy_carrier,
                               how='left',
                               left_on=['Sector', 'Subsector', 'End Use Application', 'Energy carrier', 'Energy carrier type'],
                               right_on=['Sector', 'Subsector', 'End Use Application', 'EIA: Energy carrier', 'EIA: Energy carrier type']).reset_index(drop=True)
                
        self.EIA_data['energy_demand'].rename(columns = {'Sector_x' : 'Sector',
                                                         'Subsector_x' : 'Subsector', 
                                                         'End Use Application_x' : 'End Use Application',
                                                         'Energy carrier_y' : 'Energy carrier', 
                                                         'Energy carrier type_y' : 'Energy carrier type'}, inplace = True)
        self.EIA_data['energy_demand'] = self.EIA_data['energy_demand'] [['Data Source', 'AEO Case', 'Sector', 'Subsector', 
                                                                          'End Use Application', 'Energy carrier', 'Energy carrier type', 'Basis', 
                                                                          'Year', 'Unit', 'Value']]
        
        # Map EERE study case with EIA AEO case
        self.EIA_data['energy_demand']['Case'] =  self.EIA_data['energy_demand']['AEO Case'].map(self.EIA_EERE_case).copy()
        self.EIA_data['energy_supply']['Case'] =  self.EIA_data['energy_supply']['AEO Case'].map(self.EIA_EERE_case)
        
        # Merge Electricity generation data with 'Electricity generation types' tags
        self.EIA_data['energy_demand'] = pd.merge(self.EIA_data['energy_demand'], self.corr_elec_gen, how='left', on=['Sector', 'Energy carrier', 'Energy carrier type']).reset_index(drop=True) 
        self.EIA_data['energy_supply'] = pd.merge(self.EIA_data['energy_supply'], self.corr_elec_gen, how='left', on=['Sector', 'Energy carrier', 'Energy carrier type']).reset_index(drop=True)
                
        # Merge fuel pool
        self.EIA_data['energy_demand'] = pd.merge(self.EIA_data['energy_demand'], self.corr_EIA_fuel_pool, how='left', on=['Energy carrier']).reset_index(drop=True)
        self.EIA_data['energy_supply'] = pd.merge(self.EIA_data['energy_supply'], self.corr_EIA_fuel_pool, how='left', on=['Energy carrier']).reset_index(drop=True)
    
    # Save data to file, one data table per data set
    def save_EIA_data_to_file (self, raw_file_save=False):
        
        for key in self.EIA_data.keys():
            if raw_file_save == True:
                self.EIA_data[key].to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + key + self.file_out_postfix_raw, index = False)
            else:
                self.EIA_data[key].to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + key + self.file_out_postfix, index = False)
            
    def save_TandD_data_to_file (self, fname = 'TandD'):
        self.TandD.to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
    
    def save_E85_data_to_file (self, fname = 'E85_frac'):
        self.Eth_frac_E85.to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
        
    def save_Egas_data_to_file (self, fname = 'Egas_frac'):
        self.Eth_frac_Egas.to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
        
    def save_BDDB_data_to_file (self, fname = 'BioDieselDistlBlend_frac'):
        self.Eth_frac_Egas.to_csv(self.input_path_EIA + '\\' + self.file_out_prefix + fname + self.file_out_postfix, index = False)
       
    def EERE_data_flow_EIA_AEO (self, ob_units, fetch_data, save_to_file, verbose):            
        
        if fetch_data:
            self.eia_multi_sector_import_web(self.aeo_case_dict.keys(), verbose = False )
            self.save_EIA_data_to_file(raw_file_save=True)
        else:
            self.eia_multi_sector_import_disk(self.aeo_case_dict.keys())   
        
        self.transform_EERE_tool(ob_units)
        
        self.standardize_units(ob_units)        
        
        self.calc_TandD_loss(self.aeo_case_dict.keys(), verbose) 
        
        self.classify_E85(self.aeo_case_dict.keys(), verbose)
        
        self.classify_Egasoline(self.aeo_case_dict.keys(), verbose)
        
        self.classify_BioDieselDistlBlend(self.aeo_case_dict.keys(), verbose)     
        
        self.calc_EIA_fuel_demand_by_source()
        
        self.map_corr_tables()
        
        self.conv_HHV_to_LHV (self.aeo_case_dict.keys(), ob_units, verbose)
        
        if save_to_file:
            self.save_EIA_data_to_file(raw_file_save=False)
            self.save_TandD_data_to_file()
            self.save_E85_data_to_file()
            self.save_Egas_data_to_file()
            self.save_BDDB_data_to_file()
        
# Create object and call function if script is ran directly
if __name__ == "__main__":    
    
    # Please change the path to data folder per your computer
    
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    
    input_path_EIA = input_path_prefix + '\\EIA'
    input_path_units = input_path_prefix + '\\Units'      
    input_path_GREET = input_path_prefix + '\\GREET'    
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    EIA_AEO_fetch_data = True
    save_to_file = True
    verbose = True
    load_from_disk = True
        
    os.chdir (code_path_prefix)
    
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    init_time = datetime.now()
    ob = EIA_AEO(input_path_EIA, input_path_corr)   
    
    if EIA_AEO_fetch_data:
        eia_multi_sector_df = ob.eia_multi_sector_import_web(ob.aeo_case_dict.keys(), verbose )
        ob.save_EIA_data_to_file(raw_file_save=True)
    else:
        ob.eia_multi_sector_import_disk(ob.aeo_case_dict.keys())   
    
    ob.transform_EERE_tool(ob_units)
    
    ob.standardize_units(ob_units)
    
    ob.calc_TandD_loss(ob.aeo_case_dict.keys(), verbose)
    
    ob.classify_E85(ob.aeo_case_dict.keys(), verbose)
    
    ob.classify_Egasoline(ob.aeo_case_dict.keys(), verbose)
    
    ob.classify_BioDieselDistlBlend(ob.aeo_case_dict.keys(), verbose)
    
    ob.calc_EIA_fuel_demand_by_source()
    
    ob.map_corr_tables()
    
    ob.conv_HHV_to_LHV (ob.aeo_case_dict.keys(), ob_units, verbose)
    
    if save_to_file:
        ob.save_EIA_data_to_file(raw_file_save=False)
        ob.save_TandD_data_to_file()
        ob.save_E85_data_to_file()
        ob.save_Egas_data_to_file()
        ob.save_BDDB_data_to_file()
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))