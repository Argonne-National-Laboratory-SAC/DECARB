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


#%%

class model_units:
    
    def __init__(self):
               
        self.path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
        self.f_unit_conv = 'Unit Conversion.xlsx'
        sheet_physical = 'physical'
        sheet_feedstock = 'feedstock'
        sheet_heatingvalues = 'HHV_to_LHV'
        
        physical = pd.read_excel(self.path_data + '\\' + self.f_unit_conv, sheet_name = sheet_physical)
        feedstock = pd.read_excel(self.path_data + '\\' + self.f_unit_conv, sheet_name = sheet_feedstock)
        heatingvalues = pd.read_excel(self.path_data + '\\' + self.f_unit_conv, sheet_name = sheet_heatingvalues)
        
        self.df_units = pd.concat([physical, feedstock, heatingvalues])
        
        self.df_units['unit_conv'] = self.df_units['Convert_To'] + '_per_' + self.df_units['Convert_From']
        
        # Data frames to dictionaries        
        self.dict_units = self.df_units.set_index('unit_conv').to_dict()['Multiply_By']
               
        # Unit conventions
        
        self.to_units = {
            'Energy' : 'MMBtu', # Million Metric British Thermal Unit
            'Electricity' : 'TWh', # Terawatt Hour
            'Biomass_Feedstock' : 'MT' # Metric Ton
            }
        
    def select_units(self, ut):
        try:            
            unit_category = self.df_units.loc[self.df_units['Convert_To'] == ut, 'Category'][0]
            return self.to_units[unit_category]
        
        except (Exception) as e:            
            message1 = 'Possibly a unit key: ' + ut + ' not found.'
            print(message1)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message2 = template.format(type(e).__name__, e.args)
            print (message2)
        
    def unit_convert (self, convert):
        if convert in self.dict_units:
            return self.dict_units[convert]
        else:
            print('Note: the requested unit conversion value is not found, returning 1. \
                  Please check the Unit Conversion table to check value and maintain consistency.')
            return 1

    
#%%

if __name__ == '__main__':
    ob_units = model_units()
    