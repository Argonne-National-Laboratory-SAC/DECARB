# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 11:40:22 2021

@author: skar
"""

""" 
This script contains two class definitions. One class definition defines
variables and functions for unit conversion, and the other class definition
declares the unit conventions used in calculations in the model. Pre-defining
the unit conventions facilitates to change needed units at one place and be consistent
across all calculations of the models.

"""
    
"""
sources:
1. https://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/nrcs142p2_022760.pdf
2. https://www.eia.gov/energyexplained/units-and-calculators/
3. Excel version of EERE Tool

"""

import pandas as pd 
import numpy as np


#%%

class model_units:
    
    def __init__(self, input_path_units, input_path_GREET, input_path_corr, verbose = False, class_object_for = 'EERE_Tool'):               
        
        self.input_path_units = input_path_units
        self.input_path_GREET = input_path_GREET
        self.input_path_corr = input_path_corr
        
        self.f_unit_convert = 'Unit Conversion.xlsx'
        self.f_tool_units = 'EERE_tool_unit_conventions.xlsx'
        self.f_GREET_HV = 'GREETheatingValues.xlsx'
        self.f_corr_EF_GREET_EIA = 'corr_EF_GREET_EIA.csv'
        
        self.return_to_unit = 'return_to_unit'
        self.verbose = verbose
        
        sheet_physical = 'physical'
        sheet_feedstock = 'feedstock'
        
        sheet_unit_conventions = 'unit_conventions'
              
        physical = pd.read_excel(self.input_path_units + '\\' + self.f_unit_convert, sheet_name = sheet_physical)
        feedstock = pd.read_excel(self.input_path_units + '\\' + self.f_unit_convert, sheet_name = sheet_feedstock)
        eere_tool_units = pd.read_excel(self.input_path_units + '\\' + self.f_tool_units, sheet_name = sheet_unit_conventions)
        
        hv = pd.read_excel(self.input_path_GREET + '\\' + self.f_GREET_HV)
               
        corr_EF_GREET_EIA = pd.read_csv(self.input_path_corr + '\\' + self.f_corr_EF_GREET_EIA)
        
        self.df_units = pd.concat([physical, feedstock])
        
        self.df_units['unit_conv'] = self.df_units['Convert_To'] + '_per_' + self.df_units['Convert_From']  
        
        # Data frames to dictionaries        
        self.dict_units = self.df_units.set_index('unit_conv').to_dict()['Multiply_By']
        self.eere_tool_units = eere_tool_units.set_index('Category').to_dict()['Unit']
        
        # Setting up heating value calculations
        self.hv_EIA = pd.merge(corr_EF_GREET_EIA, hv, how='left', on=['GREET_Fuel', 'GREET_Fuel type'])
        self.hv_EIA['LHV_by_HHV'] = self.hv_EIA['LHV']  / self.hv_EIA['HHV'] 
        
        # Model specific logic
        if class_object_for == 'EERE_Tool':
            # considering 1 for derived energy and average of 0.9 for unspecified or GREET-unclassified feedstocks
            self.hv_EIA.loc[self.hv_EIA['Energy carrier'].isin(['Electricity', '-', 'Renewables']), 'LHV_by_HHV'] = 1
            self.hv_EIA.loc[self.hv_EIA['Energy carrier'].isin(['Lubricants', 'Hydrocarbon Gas Liquid Feedstocks', 'Petrochemical Feedstocks']), 'LHV_by_HHV'] = 0.9
                    
    def select_units(self, ut):
        try:            
            unit_category = self.df_units.loc[self.df_units['Convert_From'] == ut, 'Category'].iloc[0]
            return self.eere_tool_units[unit_category]
        
        except (Exception) as e:            
            message1 = 'The unit key: ' + ut + ' not found.'
            if self.verbose:
                print(message1)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message2 = template.format(type(e).__name__, e.args)
            if self.verbose:
                print (message2)
            return self.return_to_unit
        
    def unit_convert (self, convert):
        if convert in self.dict_units:
            return self.dict_units[convert]
        else:
            print('Note: the requested unit conversion value is not found, now returning 1 as multiplier. \
                  Please check the Unit Conversion table to revise and maintain consistency.')
            return 1
    
    # The caller function to convert unit for a data frame. The column names should be 'Unit' and 'Value'
    def unit_convert_df (self, df, if_given_unit = False, given_unit = ''):
        
        if if_given_unit:
            df['unit_to'] = given_unit
        else:
            df['unit_to'] = [self.select_units(x) for x in df['Unit'] ]
        
        mask = (df['unit_to'].str.contains(self.return_to_unit, case=False, na=False))
        
        df['unit_conv'] = df['unit_to'] + '_per_' + df['Unit'] 
        df['Value'] = np.where(
             [x in self.dict_units for x in df['unit_conv'] ],
             df['Value'] * df['unit_conv'].map(self.dict_units),
             df['Value'] )
        df.loc[mask, 'unit_to'] = df.loc[mask, 'Unit'].copy()
        df.drop(['unit_conv', 'Unit'], axis = 1, inplace = True)
        df.rename(columns = {'unit_to' : 'Unit'}, inplace = True)
        
        return df[['Unit', 'Value']].copy()
    
    def setup_hv_convert(self):
        self.hv_EIA['LHV_by_HHV'] = self.hv_EIA['LHV'] / self.hv_EIA['HVV']
        
    
#%%

if __name__ == '__main__':
    
    # Please change the path to data per your computer
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_units = input_path_prefix + '\\Units'    
    input_path_GREET = input_path_prefix + '\\GREET'    
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    