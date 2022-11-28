# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 02/10/2022

Summary: This python script loads pre-processed GREET emission factors data.

"""

#%%
#Import Python Libraries

import pandas as pd

#%%

class GREET_EF:
    
    """
    
    """
    
    def __init__ (self, data_path_prefix):
        
        # data loading
        self.data_path_prefix = data_path_prefix
        #self.f_name = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
        #self.f_hv = 'GREETheatingValues.xlsx'
        self.f_ef = 'GREET_EF_EERE.csv'
        
        #self.sheet_hv = 'mappings'
        
        #self.ef = pd.read_excel(self.data_path_prefix + '\\' + self.f_name)
        #self.hv = pd.read_excel(self.data_path_prefix + '\\' + self.f_hv, sheet_name = self.sheet_hv)
        self.ef = pd.read_csv(self.data_path_prefix + '\\' + self.f_ef, header = 3).drop_duplicates()
        
        # Emission factor approximate conversion from LHV to HHV (multiply by 0.9)
        #self.ef['BAU'] = [0 if np.isnan(x) else x for x in self.ef['BAU'] * 0.9 ]
        #self.ef['Elec0'] = [0 if np.isnan(x) else x for x in self.ef['Elec0'] * 0.9 ]
        
        # Remove rows with nan in any columns
        #self.ef = self.ef[~ (self.ef.isna().any(axis=1)) ].copy()

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_GREET = input_path_prefix + '\\GREET'
    
    # Change the input GREET Time Series Emission Factor data file as per scenario
    #f_option = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
    f_ef = 'GREET_EF_EERE.csv'
    
    ob = GREET_EF(f_ef, input_path_GREET)
    
    print(ob.ef)