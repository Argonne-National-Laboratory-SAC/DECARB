# -*- coding: utf-8 -*-

"""
Author: George G. Zaimes and Saurajyoti Kar
Affiliation: Argonne National Laboratory
Date: 01/25/2022

Summary: This python script pulls emissions data from EPA's 2019 GHGI.

"""
#%%
#Import Python Libraries

# Python Packages
import pandas as pd
import numpy as np
import os

#%%

class EPA_GHGI_import:
    
    def __init__(self, ob_units, input_path_EPA, input_path_corr, save_to_file = True, verbose = False):
        
        print("Status: Pre-processing EPA GHGI emissions data frame ..")
        
        self.ob_units = ob_units
        self.input_path_EPA = input_path_EPA
        self.input_path_corr = input_path_corr
        self.save_to_file = save_to_file
        self.file_out = 'EPA_GHGI.csv'
        
        # Load in GHGI import sheet
        df = pd.read_csv(self.input_path_corr + '\\' + 'ghgi_correspondence.csv')
        
        # create list to append GHGI data
        temp_list = [] 
        
        # Loop through data tables in GHGI
        for row in df.itertuples():
            if verbose:
                print('Currently fetching: ' + row.filename)
            df_temp = pd.read_excel(self.input_path_EPA + '\\ghgi data tables\\' + str(row.filename) + '.xlsx', sheet_name='Tidy')
            df_temp['Table'] = row.filename
            temp_list.append(df_temp)    
        
        self.df_ghgi = pd.concat(temp_list, axis=0)
        self.df_ghgi = self.df_ghgi.reset_index(drop=True)
        
        # Convert carbon flows (C) to Carbon Dioxide (CO2), e.g. C --> CO2
        c_to_co2 = (16*2+12)/12
        
        # Replace non-numeric values reported in GHGI
        self.df_ghgi.loc[~ self.df_ghgi["Value"].apply(np.isreal), 'Value'] = 0 
        
        # Update GHGI C FLows --> CO2
        self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C','Value'] = self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C','Value'] * c_to_co2
        self.df_ghgi.loc[self.df_ghgi['Emissions Type']=='C', 'Emissions Type'] = 'CO2'
        
        # Unit conversion 
        self.df_ghgi[['Unit', 'Value']] = self.ob_units.unit_convert_df ( self.df_ghgi[['Unit', 'Value']],
                                                                    if_given_category = True, unit_category = 'Emissions')
              
        self.df_ghgi.rename(columns = {'Value' : 'GHG Emissions'}, inplace=True)
        
        # Aggregate results by Year, Sector, and Source
        self.df_ghgi_agg = self.df_ghgi.groupby(['Year', 'Inventory Sector', 'Economic Sector', 'Source', 'Unit'], as_index = False).agg(
            {'GHG Emissions' : 'sum'}).reset_index()
        
        self.df_ghgi_agg.rename(columns = {'EF_Unit (Numerator)' : 'Emissions Unit'}, inplace=True)
                       
     
    def remove_combustion_other_em (self):
        
        # Removing combustion based emissions
        mask = (self.df_ghgi['Source'].str.contains('combustion', case=False, na=False))
        self.df_ghgi = self.df_ghgi [~ mask]
        
        # Removing 'Others' which occur in the 'Substitution of Ozone Depleting Substances' category
        self.df_ghgi = self.df_ghgi.loc[~ (self.df_ghgi['Emissions Type'] == 'Others') ]
        
        # Remove 'Non-Energy Use of Fuels'
        self.df_ghgi = self.df_ghgi.loc[~ (self.df_ghgi['Source'] == 'Non-Energy Use of Fuels')]
    
    # QA/QC Check    
    def QA_with_table_2_10(self, yr_filter = [2019] ):
        
        # Load in 100-Yr GWP Factors
        lcia = pd.read_excel(self.input_path_EPA + '\\gwp factors.xlsx', sheet_name='Tidy')

        # Use AR4 100-Yr GWP Factors, so that results can be compared with EIA's GHGI.         
        lcia_ar4 = lcia[lcia['LCIA Method'] == 'AR4'].copy()
        #lcia_ar4['GWP_years'] = 100
        
        # Merge GWP factors to dataframe
        self.df_ghgi_QA = self.df_ghgi.merge(lcia_ar4, how='left', on=['Emissions Type'])
        
        # Calculate GWP
        self.df_ghgi_QA['GHG Emissions'] = self.df_ghgi_QA['GHG Emissions'] * self.df_ghgi_QA['GWP']
        
        self.data_2_10_agg = self.table_2_10()
        
        #self.data_oth_agg = self.df_ghgi[self.df_ghgi['Table'] != 'Table 2-10'].copy()
        self.data_oth_agg = self.df_ghgi_QA.groupby(['Year', 'Economic Sector'], as_index = False)['GHG Emissions'].sum()
        
        d1 = self.data_oth_agg.merge(self.data_2_10_agg, left_on=['Year', 'Economic Sector'], right_on=['Year', 'Economic Sector'], how = 'left')
        d1.rename(columns = {'GHG Emissions_x' : 'GHG Emissions_compiled', 'GHG Emissions_y' : 'GHG Emissions_2_10'}, inplace = True)
        
        d1['Difference by'] = d1['GHG Emissions_compiled'] - d1['GHG Emissions_2_10']
        d1['percent diff'] = ( d1['GHG Emissions_compiled'] - d1['GHG Emissions_2_10'] ) / d1['GHG Emissions_2_10'] * 100
        
        d1 = d1[d1['Year'].isin(yr_filter)]
        
        return (d1)
        
    
    def table_2_10(self):
                   
        # load data table
        df_temp = pd.read_excel(self.input_path_EPA + "/" + "ghgi data tables/" + "Table 2-10.xlsx", sheet_name='Table 2-10', header = 2, index_col = None)
        
        # convert from wide to long form data
        df_temp = pd.melt(df_temp, id_vars=['Sector/Source'])
        
        # remove null or not needed rows, and replace with 0
        df_temp = df_temp[ ~ df_temp['Sector/Source'].isnull() ]        
        df_temp = df_temp[ ~ df_temp['value'].isnull() ]        
        df_temp = df_temp[ ~ df_temp['variable'].isin(['Percent a']) ]        
        df_temp.loc[ ~ df_temp['value'].apply(np.isreal), 'value' ] = 0
        
        # filter by primary economic sector names only
        df_temp = df_temp[ df_temp['Sector/Source'].isin(['Transportation', \
                       'Electric Power Industry', 'Industry', 'Agriculture', 'Commercial', 'Residential', \
                       'LULUCF Sector Net Total b' ]) ]
        
        # rename for similarity to later data sets
        df_temp.rename(columns = {'Sector/Source' : 'Economic Sector', \
                                  'variable' : 'Year', 'value' : 'GHG Emissions'}, inplace = True)
        
        # rename categories for similarity with later data set
        df_temp.loc[df_temp['Economic Sector'] == 'LULUCF Sector Net Total b', 'Economic Sector'] = 'LULUCF'
        df_temp.loc[df_temp['Economic Sector'] == 'Electric Power Industry', 'Economic Sector'] = 'Electric Power'
        
        return (df_temp)
          
    
    def process_EERE (self, decarb_year_min, decarb_year_max):
        
        print("Status: Constructing EPA GHGI emissions data frame as activity data frame ..")
        
        self.EPA_GHGI_maxyear = np.max(self.df_ghgi['Year'])
        
        activity_non_combust = self.df_ghgi.loc[self.df_ghgi['Year'] == self.EPA_GHGI_maxyear, :].copy()

        # preserve Category and Subcategory information in one column
        activity_non_combust ['Category, Subcategory'] = activity_non_combust ['Category'].copy() + ', ' + activity_non_combust ['Subcategory'].copy()

        # Select the required columns
        activity_non_combust = activity_non_combust[[
            'Economic Sector',
            'Source',
            'Segment',
            'Category, Subcategory',
            'Emissions Type',
            'Year',
            'Unit',
            'GHG Emissions'
            ]]

        # Rename columns to match with EIA AEO's activity data frame
        activity_non_combust.rename(columns = {
            'Economic Sector' : 'Sector',
            'Source' : 'Subsector',
            'Segment' : 'Basis',
            'Category, Subcategory' : 'End Use Application',
            'Emissions Type' : 'Formula',
            'GHG Emissions' : 'Total Emissions',
            'Unit' : 'Emissions Unit'
            }, inplace=True)

        # Expand the data frame to all the assessment years
        activity_non_combust['Year'] = decarb_year_min
        self.activity_non_combust_exp = activity_non_combust.copy()
        for yr in range(decarb_year_min+1, decarb_year_max+1): # [a,)
            activity_non_combust['Year'] = yr
            self.activity_non_combust_exp = pd.concat ([self.activity_non_combust_exp, activity_non_combust], axis=0).copy().reset_index(drop=True)
        
        # unit conversion    
        self.activity_non_combust_exp[['Emissions Unit', 'Total Emissions']] = \
            self.ob_units.unit_convert_df(self.activity_non_combust_exp[['Emissions Unit', 'Total Emissions']],
                                          Unit = 'Emissions Unit', Value = 'Total Emissions',          
                                          if_given_category=True, unit_category='Emissions')
        
        # Adding additional empty columns, to match with other activity df
        self.activity_non_combust_exp[['AEO Case', 
                              'Energy carrier',
                              'Energy carrier type',
                              'Fuel Pool',
                              'Flow Name',                      
                              'Unit',                      
                              'Value',
                              'CI'                              
                              ]] = '-'

        # Defining values to specific columns
        self.activity_non_combust_exp['Case'] = 'Reference case'
        self.activity_non_combust_exp['Scope'] = 'Direct, Non-Combustion'
        self.activity_non_combust_exp['Data Source'] = 'EPA GHGI'

        # Rearranging columns
        self.activity_non_combust_exp = self.activity_non_combust_exp[['Data Source', 'AEO Case', 'Case', 'Sector', 'Subsector', 
                                                     'End Use Application', 'Scope', 'Energy carrier', 'Energy carrier type', 
                                                     'Basis', 'Fuel Pool', 'Year', 'Flow Name', 'Formula', 'Emissions Unit', 
                                                     'Unit', 'Value', 'CI', 'Total Emissions']]
        
        # Rename the industry to industrial for alligning with EIA data set
        self.activity_non_combust_exp.loc[self.activity_non_combust_exp['Sector'] == 'Industry', 'Sector'] = 'Industrial'
        
        # Seperate Electric Power economic sector data as those will be included within the reference case electric power calculations
        self.activity_elec_non_combust_exp = self.activity_non_combust_exp.loc[self.activity_non_combust_exp['Sector'] == 'Electric Power', : ]
        self.activity_non_combust_exp = self.activity_non_combust_exp.loc[~(self.activity_non_combust_exp['Sector'] == 'Electric Power'), : ]
        
        # Rename subsectors as per EERE Decarb Tool
        self.activity_non_combust_exp.loc[self.activity_non_combust_exp['Subsector'] == 'Cement Production', 'Subsector'] = 'Cement and Lime Industry'
        self.activity_non_combust_exp.loc[self.activity_non_combust_exp['Subsector'] == 'Lime Production', 'Subsector'] = 'Cement and Lime Industry'
        

if __name__ == "__main__":
    
    # Please change the path to data folder per your computer
      
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_EPA = input_path_prefix + '\\EPA_GHGI'
    input_path_GREET = input_path_prefix + '\\GREET' 
    input_path_units = input_path_prefix + '\\Units'
    input_path_corr = input_path_prefix + '\\correspondence_files'
       
    save_to_file = True
    verbose = False
    
    # Import the unit conversion module
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    os.chdir (code_path_prefix)

    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    ob1 = EPA_GHGI_import(ob_units, input_path_EPA, input_path_corr, save_to_file, verbose)
    
    df = ob1.QA_with_table_2_10()
    
    print("QA data frame: ")
    print(df)
    
    ob1.remove_combustion_other_em()
    
    ob1.process_EERE(decarb_year_min=2020, decarb_year_max=2050)
    
    if ob1.save_to_file == True:
        ob1.df_ghgi.to_csv(input_path_EPA + ob1.file_out, index = False)    

