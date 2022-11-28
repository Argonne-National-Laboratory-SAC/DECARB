# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Created on Wed Jan 20 09:12:20 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 01/19/2022

Summary: This python script loads Transportation fuel use estiamtion over years (2020 - 2050)
from VISION model.

"""

#%%
#Import Python Libraries

import pandas as pd
import numpy as np
import os
import unit_conversions as ut

#%%

class Transport_Vision:
    
    """
    """
    
    def __init__ (self, input_path_transport):
        
        self.input_path_transport = input_path_transport
                
        self.f_name = 'MDHD_TEMPO Sales Share_VISION Results.xlsx'
        
        # data loading
        self.agg = pd.read_excel(self.input_path_transport + '\\' + self.f_name, header = 3)
                
        # unit conversion
        

if __name__ == '__main__':
    
    # Import user defined modules
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    os.chdir(code_path_prefix)
    
    # Please change the path to data folder per your computer
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_transport = input_path_prefix + '\\Transportation'
    
    ob1 = Transport_Vision(input_path_transport)
    
    print(ob1.agg)