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


#%%

class GREET_EF:
    
    """
    
    """
    
    def __init__ (self, f_option, data_path_prefix):
        
        # data loading
        self.data_path_prefix = data_path_prefix
        self.f_name = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
        self.f_hv = 'GREETheatingValues.xlsx'
        
        self.sheet_hv = 'mappings'
        
        self.ef = pd.read_excel(self.data_path_prefix + '\\' + self.f_name)
        self.hv = pd.read_excel(self.data_path_prefix + '\\' + self.f_hv, sheet_name = self.sheet_hv)
        
        # Emission factor approximate conversion from LHV to HHV (multiply by 0.9)
        self.ef['BAU'] = self.ef['BAU'] * 0.9
        self.ef['Elec0'] = self.ef['Elec0'] * 0.9
        self.ef['Elec_BAU'] = self.ef['Elec_BAU'] * 0.9

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model'
    
    # Change the input GREET Time Series Emission Factor data file as per scenario
    f_option = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
    
    ob = GREET_EF(f_option, data_path_prefix)
    
    print(ob.ef)