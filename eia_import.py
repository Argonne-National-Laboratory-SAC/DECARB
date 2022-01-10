# -*- coding: utf-8 -*-

"""
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 01/08/2022

Summary: This python script pulls time-series (2020-2050) data from EIA's AEO.

Data Sources:
EIA AEO: https://www.eia.gov/outlooks/aeo/

"""
#%%
#Import Python Libraries

# Python Packages
import pandas as pd
import requests

#%%
# Set the EIA API Key (used to pull EIA data). EIA API Keys can be obtained via https://www.eia.gov/opendata/
# Create a Dictionary which maps EIA AEO cases to their API ID. AEO Cases represent different projections of the 
# U.S. Energy System. 'Looping' over the AEO dictionary, provides an easy way to extract EIA data across AEO cases.

# Obtain API Key from EIA, see URL: https://www.eia.gov/opendata/
eia_api_key = '047f4916ce9b0b97f6e9a8d2fbee1c00'

# Create a dictionary of AEO cases, and their corresponding API ID
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

# Set the filepath to the file that contains the EIA AEO Series Id's
eia_path = 'C:/Users/gzaimes/Desktop/B2B Project/Input files/eia_aeo_demand.xlsx'

#%%
# Create a function to store sector-wide energy consumption

def eia_data_import (sectors, aeo_cases, filepath, api_key): 
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
    
    # Loop over sectors
    for sector in sectors:
        
        # Load in EIA data
        df_eia_import = pd.read_excel(eia_path, sheet_name = sector)
        df_eia_dict = df_eia_import.to_dict('records') # converts datafame to dictionary, to enable dictionary iteration
        
        # Loop over aeo cases
        for aeo_case in aeo_cases:
            
            # Loop over rows in dataframe
            for row in df_eia_dict:
                series_id = aeo_case_dict[aeo_case] + row['Series Id']
                url = 'http://api.eia.gov/series/?api_key=' + api_key +'&series_id=' + series_id
                r = requests.get(url)
                json_data = r.json()
                df_temp = pd.DataFrame(json_data.get('series')[0].get('data'),
                                       columns = ['Year', 'Value'])
                df_temp['Case'] = row['Case']
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
    df_eia_data = pd.concat(temp_list, axis=0)
    df_eia_data = df_eia_data.reset_index(drop=True)
    return df_eia_data

#%%
# Test function

df_eia = eia_data_import(sectors = ['Residential','Commercial'], aeo_cases = ['Reference case'], api_key = eia_api_key, filepath = eia_path)