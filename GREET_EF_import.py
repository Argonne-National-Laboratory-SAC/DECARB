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
    
    def __init__ (self):
        
        # data loading
        self.path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
        self.f_name = 'EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx'
        self.f_hv = 'GREETheatingValues.xlsx'
        
        self.sheet_hv = 'mappings'
        
        self.ef = pd.read_excel(self.path_data + '\\' + self.f_name)
        self.hv = pd.read_excel(self.path_data + '\\' + self.f_hv, sheet_name = self.sheet_hv)
        
        # Emission factor approximate conversion from LHV to HHV (multiply by 0.9)
        self.ef['BAU'] = self.ef['BAU'] * 0.9
        self.ef['Elec0'] = self.ef['Elec0'] * 0.9
        self.ef['Elec_BAU'] = self.ef['Elec_BAU'] * 0.9

if __name__ == '__main__':
    
    ob = GREET_EF()
    
    print(ob.ef)