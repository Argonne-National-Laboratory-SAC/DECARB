# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
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
        self.f_name = 'Industrial.csv'
        
        # data loading
        self.industrial = pd.read_csv(self.data_path_prefix + '\\' + self.f_name, header = 3)
               
        # unit conversion
        self.industrial [['Unit', 'Value']] = ob_units.unit_convert_df (self.industrial [['Unit', 'Value']].copy())
        
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
    
    def mtg_init (self, EIA_data) :
        
        self.EIA_industry_demand = EIA_data['energy_demand'][EIA_data['energy_demand']['Sector'] == 'Industrial']
        
        self.mtg_paper_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Paper Industry']
        self.mtg_food_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Food Industry']
        self.mtg_blkchem_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Bulk Chemical Industry']
        
        #self.mtg_blkchem_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Iron and Steel Industry']
        #self.mtg_blkchem_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Cement and Lime Industry']
        #self.mtg_blkchem_extract_EIA = self.EIA_industry_demand.loc[self.EIA_industry_demand['Subsector'] == 'Other Manufacturing Industry']

# Notes for improvement:
# A variable option that can change the adaption curve parameters as input.
# The mitigation option should have different choices for the adoption curve parameters

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
      
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    
    #input_path_EPA = input_path_prefix + '\\EPA_GHGI'  
    input_path_industrial = input_path_prefix + '\\Industrial'
    input_path_units = input_path_prefix + '\\Units'
    input_path_GREET = input_path_prefix + '\\GREET'    
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    # Import the unit conversion module    
    os.chdir (code_path_prefix)
    from  unit_conversions import model_units
    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    ob1 = Industrial(ob_units, input_path_industrial)
    
    print(ob1.industrial)