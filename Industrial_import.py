# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 09:12:20 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 01/19/2022

Summary: This python script loads Industrial activity based emissions data (2020 - 2050)
to a class and pre-processes it. Data sourced by Hoyoung Kwon

"""

#%%
#Import Python Libraries

import pandas as pd
import numpy as np
import os


#%%

class Industrial:
    
    """
    """
    
    def __init__ (self, ob_units, data_path_prefix):
              
        self.data_path_prefix = data_path_prefix
        self.f_name = 'Industrial.xlsx'
        
        # data loading
        self.industrial = pd.read_excel(self.data_path_prefix + '\\' + self.f_name, header = 3)
               
        # unit conversion
        self.industrial['unit_to'] = [ob_units.select_units(x) for x in self.industrial['Unit'] ]
        self.industrial['unit_conv'] = self.industrial['unit_to'] + '_per_' + self.industrial['Unit'] 
        self.industrial['Value'] = np.where(
             [x in ob_units.dict_units for x in self.industrial['unit_conv'] ],
             self.industrial['Value'] * self.industrial['unit_conv'].map(ob_units.dict_units),
             self.industrial['Value'] )
        self.industrial.drop(['unit_conv', 'Unit'], axis = 1, inplace = True)
        self.industrial.rename(columns = {'unit_to' : 'Unit'}, inplace = True)
        
        # scaling values using adoption curve
        self.industrial['Value_scaled'] = self.industrial['Value'] * \
        [ self.adoption_curve(0, 100, 0.5, 2020, 2050, x, 1) for x in self.industrial['Year']]
        
        # add a separate column in mitigation, activity matrix 
            
    def adoption_curve (self,
                        min_val,
                        max_val,
                        k,
                        start_yr,
                        end_yr,
                        curr_yr,
                        a):
        x = curr_yr
        x_0 = int ( (start_yr + end_yr) /2 )
        val = min_val + (max_val - min_val) * pow ((1 / (1 + np.exp( -k * (x - x_0)))), a) 
        return val

# Notes for improvement:
# A variable option that can change the adaption curve parameters as input.
# The mitigation option should have different choices for the adoption curve parameters

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model'
    
    # Import the unit conversion module
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    
    os.chdir (code_path_prefix)

    from  unit_conversions import model_units    
    ob_units = model_units(data_path_prefix)
    
    ob1 = Industrial(ob_units, data_path_prefix)
    
    print(ob1.industrial)