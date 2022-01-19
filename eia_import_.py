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

# Python Packages
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
    def __init__(self, save_to_file):
        
        # data and file paths
        self.path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
        self.file_key = 'EIA_datakey.csv'
        self.file_series = 'eia_aeo_demand.xlsx'
        self.file_out = 'EIA Dataset.csv'
        self.save_to_file = save_to_file
        
        # Create a dictionary of AEO cases, and their corresponding API ID
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
        self.api_key = pd.read_csv(self.path_data + '\\' + self.file_key, index_col=0, squeeze=True).to_dict()[self.curr_user]
        
    # Function to fetch sector-wide energy consumption and CO2 emissions    
    def eia_sector_import (self, aeo_case, df_aeo_key): 
        """
        Parameters
        ----------
        sectors : List
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
        
        filepath : str
             Set the filepath to the EIA file which contains the EIA series IDs 
        
        Returns
        -------
        eia_df : Pandas DataFrame
            Output is a pandas DataFrame that contains detailed estimates of energy consumption
            for the selected U.S. sector and AEO case over the 2020 to 2050 time-horizon.

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
            url = 'http://api.eia.gov/series/?api_key=' + self.api_key +'&series_id=' + series_id
            r = requests.get(url)
            json_data = r.json()
            print('Currently fetching: ' + url)
            df_temp = pd.DataFrame(json_data.get('series')[0].get('data'),
                                   columns = ['Year', 'Value'])
            #df_temp['Case'] = row['Case']
            df_temp['Sector'] = row['Sector']
            df_temp['Subsector'] = row['Subsector']
            df_temp['End Use'] = row['End Use']  
            df_temp['Activity'] = row['Activity']  
            df_temp['Activity Type'] = row['Activity Type']  
            df_temp['Activity Basis'] = row['Activity Basis']  
            df_temp['Metric'] = row['Metric']  
            df_temp['Unit'] = row['Unit']  
            df_temp['Data Source'] = row['Data Source']
            df_temp['AEO Case'] = aeo_case
            df_temp['Series Id'] = series_id
            temp_list.append(df_temp)
        eia_sector_df = pd.concat(temp_list, axis=0)
        eia_sector_df = eia_sector_df.reset_index(drop=True)
        return eia_sector_df
    
    # Use the function to create datasets for sector-specific and AEO cases: 
    #eia_sector_df = eia_sector_import(sector = 'Residential', aeo_case = 'Reference case')
    
    # Function to store results across multiple combinations of AEO-cases and sectors    
    def eia_multi_sector_import (self, sectors, aeo_cases): 
        
        # Create an temporary list to store results
        temp_list = [] 
        
        #Loop through every combination of AEO Case and Sector 
        for aeo_case in aeo_cases:
            for sector in sectors:
                # Load in EIA's AEO Series IDs / AEO Keys
                df_aeo_key = pd.read_excel(self.path_data + '\\' + self.file_series, sheet_name = sector)
                eia_df_temp = self.eia_sector_import(aeo_case = aeo_case, df_aeo_key = df_aeo_key)
                temp_list.append(eia_df_temp)
        
        # Concatenate results into one large dataframe, containing all combinations of sectors and cases
        eia_economy_wide_df = pd.concat(temp_list, axis=0)
        eia_economy_wide_df = eia_economy_wide_df.reset_index(drop=True)
        
        if self.save_to_file == True:
            eia_economy_wide_df.to_csv(self.path_data + '\\' + self.file_out, index = False)
        else:
            return eia_economy_wide_df

# Create object and call function if script is ran directly

if __name__ == "__main__":
    init_time = datetime.now()
    ob = EIA_AEO(save_to_file = True)
    eia_multi_sector_df = ob.eia_multi_sector_import(sectors = ['Residential',
                                                                'Commercial',
                                                                'Electric Power'
                                                             ],
                                                  
                                                  aeo_cases = ['Reference case',
                                                               'High economic growth',
                                                               'Low economic growth',
                                                               'High oil price',
                                                               'Low oil price',
                                                               'High oil and gas supply',
                                                               'Low oil and gas supply',
                                                               'High renewable cost',
                                                               'Low renewable cost'
                                                               ]                                                  
                                                  )
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))