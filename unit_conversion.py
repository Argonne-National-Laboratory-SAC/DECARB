# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 13:45:21 2022

@author: gzaimes
"""

#%%
#Import Python Libraries

# Python Packages
import pandas as pd
import numpy as np
import seaborn as sns

#%%

# Create a function to store sector-wide energy consumption

def unit_conversion (from_unit, to_unit, value): 
    """
    

    Parameters
    ----------
    from_unit : string
        Add
        
    to_unit : string
        Add
            
    value : int or float
        Add         

    
    Returns
    -------
    Add : Pandas DataFrame
        Output is a pandas DataFrame that Add

    """

    # import unit conversions excel file 
    df_conv = pd.read_excel('C:/Users/gzaimes/Desktop/B2B Project/Input files/Unit Conversion.xlsx')
    conversion = df_conv[(df_conv['Convert_From'] == from_unit) & (df_conv['Convert_To'] == to_unit)]

    if (conversion.shape[0]==0):
        return print("unit conversion is not valid, please try again")
    else:
        ans = value * conversion['Multiply_By'].values[0]
        return ans

#%%

# Test function
unit_conversion('kWh','GWh',1)
