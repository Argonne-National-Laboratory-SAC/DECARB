# -*- coding: utf-8 -*-
"""
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
    
    def __init__ (self, data_path_prefix):
        
        self.data_path_prefix = data_path_prefix
                
        self.f_name = 'Industrial.xlsx'
        
        # data loading
        self.agg = pd.read_excel(self.path_data + '\\' + self.f_name, header = 3)
                
        # unit conversion
        

if __name__ == '__main__':
    
    # Import user defined modules
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    os.chdir(code_path_prefix)
    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model'
    
    ob1 = Transport_Vision(data_path_prefix)
    
    print(ob1.agg)