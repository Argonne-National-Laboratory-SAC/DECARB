# -*- coding: utf-8 -*-

"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 01/06/2022

Summary: This python script pulls time-series (2020-2050) data from EIA's AEO.

"""
#%%
#Import Python Libraries

# Python Packages
import pandas as pd
import numpy as np
import seaborn as sns

#%%
# Create a function to store sector-wide energy consumption

def adoption_curve (minimum, maximum, init_year, final_year, k, a): 
    """
    

    Parameters
    ----------
    minimum : int or float
        Add
        
    maximum : int or float
        Add
            
    init_year : int
         Add
    
    final_year : int
         Add
         
    k : int or float
         Add

    a : int or float
         Add         

    
    Returns
    -------
    Add : Pandas DataFrame
        Output is a pandas DataFrame that Add

    """
    
    # A list of years, 
    years = [*range(init_year, final_year + 1, 1)]
    
    # Add
    df = pd.DataFrame(data = years, columns = ['Year'])
    
    # Add
    df['Adoption Curve'] = minimum + (maximum - minimum) * ((1) / ((1 + np.exp((-k*(df['Year']-(init_year + final_year)/2))))**a))
   
    return df

# Test function
test = adoption_curve(minimum = 0.1, maximum = 0.9, init_year = 2020, final_year = 2050, k = 0.5, a = 1)

#%%
# Visualize Adoption Curve

g = sns.lineplot(data=test, x='Year', y='Adoption Curve')
