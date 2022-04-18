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
import sys


#%%

class model_units:
    
    def __init__(self, input_path_units, input_path_GREET, input_path_corr, verbose = True, class_object_for = 'EERE_Tool'):               
        
        self.input_path_units = input_path_units
        self.input_path_GREET = input_path_GREET
        self.input_path_corr = input_path_corr
        
        self.f_unit_convert = 'Unit Conversion.xlsx'
        self.f_tool_units = 'EERE_tool_unit_conventions.csv'
        self.f_GREET_HV = 'GREETheatingValues.csv'
        self.f_corr_EF_GREET_EIA = 'corr_EF_GREET_EIA.csv'
        
        self.return_to_unit = 'return_to_unit'
        self.verbose = verbose
        
        sheet_physical = 'physical'
        sheet_feedstock = 'feedstock'
              
        physical = pd.read_excel(self.input_path_units + '\\' + self.f_unit_convert, sheet_name = sheet_physical)
        feedstock = pd.read_excel(self.input_path_units + '\\' + self.f_unit_convert, sheet_name = sheet_feedstock)
        eere_tool_units = pd.read_csv(self.input_path_units + '\\' + self.f_tool_units)
        
        hv = pd.read_csv(self.input_path_GREET + '\\' + self.f_GREET_HV)
               
        corr_EF_GREET_EIA = pd.read_csv(self.input_path_corr + '\\' + self.f_corr_EF_GREET_EIA)
        
        self.df_units = pd.concat([physical, feedstock])
        
        # convert all units to lower case to avoid missing keys due to string case
        self.df_units['Convert_To'] = self.conv_to_lower_list(self.df_units['Convert_To'])
        self.df_units['Convert_From'] = self.conv_to_lower_list(self.df_units['Convert_From'])
        eere_tool_units['Unit'] = self.conv_to_lower_list(eere_tool_units['Unit'])
        
        self.df_units['unit_conv'] = self.df_units['Convert_To'] + '_per_' + self.df_units['Convert_From']  
        
        all_units = pd.concat([self.df_units['Convert_To'], self.df_units['Convert_From'] ] ).unique()
        all_units = all_units + '_per_' + all_units
        all_units = pd.DataFrame({'unit_conv' : all_units,
                      'Multiply_By' : [1]*len(all_units)})
        
        self.df_units = pd.concat([self.df_units, all_units], axis = 0)
        
        # Data frames to dictionaries        
        self.dict_units_from = self.df_units.set_index('Convert_From').to_dict()['Category']
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
                    
    def conv_to_lower_list(self, lst):
        return [x.lower() for x in lst].copy()
        
    def select_units(self, ut, unit_category=''):
        try:            
            if unit_category == '':
                unit_category = self.dict_units_from [ut]
           
            return self.eere_tool_units[unit_category]
        
        except (Exception) as e:            
            message1 = 'The unit key: ' + ut + ' not found.'
            if self.verbose:
                print(message1)
            template = "An exception of type {0} occurred. Arguments: {1!r}"
            message2 = template.format(type(e).__name__, e.args)
            if self.verbose:
                print (message2)
            sys.exit(1)
        
    def unit_convert (self, convert):
        if convert in self.dict_units:
            return self.dict_units[convert]
        else:
            print('Note: the requested unit conversion value is not found, now returning 1 as multiplier. \
                  Please check the Unit Conversion table to revise and maintain consistency.')
            return 1
    
    # The caller function to convert unit for a data frame. The column names should be 'Unit' and 'Value'
    def unit_convert_df (self, df, 
                         Unit = 'Unit', Value = 'Value', 
                         if_given_unit = False, given_unit = '',  # convert to lower case
                         if_given_category = False, unit_category = 'None'):
        
        df = df.copy()
        df[Unit] = self.conv_to_lower_list(df[Unit])
        
        if if_given_unit:
            df['unit_to'] = given_unit
        elif if_given_category:
            df['unit_to'] = [self.select_units(x, unit_category) for x in df[Unit] ]
        else:
            df['unit_to'] = [self.select_units(x) for x in df[Unit] ]
                
        df['unit_conv'] = df['unit_to'] + '_per_' + df[Unit] 
        
        missing_keys = df.loc[~ (df['unit_conv'].isin(self.dict_units.keys()) ), 'unit_conv' ].unique()
        if len(missing_keys) > 0:            
            print('WARNING: missing unit conversion keys:')
            print(missing_keys)
            raise KeyError ('Please update the unit_conversions table before model execution .. ')
        
        df[Value] = np.where(
             [x in self.dict_units for x in df['unit_conv'] ],
             df[Value] * df['unit_conv'].map(self.dict_units),
             df[Value] )
        
        df.drop(['unit_conv', Unit], axis = 1, inplace = True)
        df.rename(columns = {'unit_to' : Unit}, inplace = True)
        
        return df[[Unit, Value]].copy()
    
    def setup_hv_convert(self):
        self.hv_EIA['LHV_by_HHV'] = self.hv_EIA['LHV'] / self.hv_EIA['HHV']
        
    
#%%

if __name__ == '__main__':
    
    # Please change the path to data per your computer
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_units = input_path_prefix + '\\Units'    
    input_path_GREET = input_path_prefix + '\\GREET'    
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    # Class testing
    df_test = pd.DataFrame({
        'Unit' : ['kt', 'MMmt'],
        'Value' : [2, 1],
        'Category' : ['mass', 'mass'],
        'expected_Unit' : ['MMmt', 'MMmt'],
        'expected_Value' : [1E-6, 1]})
    
    print( ob_units.select_units('kt') )
    print( ob_units.select_units('kto') )
    
    print( ob_units.unit_convert_df(df_test[['Unit', 'Value']]) )
