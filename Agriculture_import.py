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
    
    def __init__ (self):
        
        # data loading
        self.path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
        self.f_name = 'Agriculture.xlsx'
        self.agg = pd.read_excel(self.path_data + '\\' + self.f_name, header = 3)
        
        # unit conversion
        

if __name__ == '__main__':
    ob1 = Agriculture()
    print(ob1.agg)