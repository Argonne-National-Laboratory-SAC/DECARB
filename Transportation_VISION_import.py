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

# Import user defined modules
code_path = 'C:\\Users\\skar\\repos\\EERE_decarb'
os.chdir(code_path)

import unit_conversions as ut

#%%

class Transport_Vision:
    
    """
    """
    
    def __init__ (self):
        
        # data loading
        self.path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
        self.f_name = 'Industrial.xlsx'
        self.agg = pd.read_excel(self.path_data + '\\' + self.f_name, header = 3)
                
        # unit conversion
        

if __name__ == '__main__':
    ob1 = Transport_Vision()
    print(ob1.agg)