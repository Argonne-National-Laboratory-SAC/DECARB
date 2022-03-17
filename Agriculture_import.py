# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 09:12:20 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 01/19/2022

Summary: This python script loads Agriculture activity based emissions data (2020 - 2050)
to a class and pre-processes it. Data sourced by Hoyoung Kwon

"""

#%%
#Import Python Libraries

import pandas as pd

#%%

class Agriculture:
    
    """
    """
    
    def __init__ (self, data_path_prefix):
        
        self.data_path_prefix = data_path_prefix
        self.f_name = 'Agriculture.xlsx'
        
        # data loading        
        self.agg = pd.read_excel(self.data_path_prefix + '\\' + self.f_name, header = 3)
        
        # unit conversion
        

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_aggriculture = input_path_prefix + '\\Agriculture'
    
    ob1 = Agriculture(input_path_aggriculture)
    
    print(ob1.agg)