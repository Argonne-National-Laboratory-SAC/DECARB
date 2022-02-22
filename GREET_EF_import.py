# -*- coding: utf-8 -*-
"""
@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 02/10/2022

Summary: This python script loads pre-processed GREET emission factors data.

"""

#%%
#Import Python Libraries

import pandas as pd
import numpy as np


#%%

class GREET_EF:
    
    """
    
    """
    
    def __init__ (self, f_ef, data_path_prefix):
        
        # data loading
        self.data_path_prefix = data_path_prefix
        #self.f_name = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
        #self.f_hv = 'GREETheatingValues.xlsx'
        self.f_ef = f_ef
        
        #self.sheet_hv = 'mappings'
        
        #self.ef = pd.read_excel(self.data_path_prefix + '\\' + self.f_name)
        #self.hv = pd.read_excel(self.data_path_prefix + '\\' + self.f_hv, sheet_name = self.sheet_hv)
        self.ef = pd.read_csv(self.data_path_prefix + '\\' + self.f_ef, header = 3)
        
        # Emission factor approximate conversion from LHV to HHV (multiply by 0.9)
        self.ef['BAU'] = [0 if np.isnan(x) else x for x in self.ef['BAU'] * 0.9 ]
        self.ef['Elec0'] = [0 if np.isnan(x) else x for x in self.ef['Elec0'] * 0.9 ]

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model'
    
    # Change the input GREET Time Series Emission Factor data file as per scenario
    #f_option = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
    f_ef = 'GREET_EF_EERE.csv'
    
    ob = GREET_EF(f_ef, data_path_prefix)
    
    print(ob.ef)