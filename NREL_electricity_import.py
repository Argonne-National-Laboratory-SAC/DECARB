# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 09:12:20 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar and George G. Zaimes
@Affiliation: Argonne National Laboratory
@Date: 01/19/2022

Summary: This python script loads NREL's electricity generation data (2020 - 2050)
to a class and pre-processes it.

"""
#%%
#Import Python Libraries

import pandas as pd
import numpy as np
from datetime import datetime

#%%

class NREL_elec:
   
    """
    
    Data file options -
        All Options = all mitigation measures
        Constrained = less ability for long-distance transmission (higher transmission costs), and constraints on some generation technologies but mainly about transmission
        Infrastructure = more ability for long-distance transmission, more transmission infrastructure
        No CCS = no carbon capture for fossil generation, meaning more renewable scale up
    
    Data Abbreviations -
        o-g-s = oil, gas, steam
        cc = combined cycle
        smr = small modular reactor
        Canada = Canadian imports
        battery_XX = battery storage where XX = hrs of storage
        lfill = landfill
        ofs = offshore
        ons = onshore
        distpv = distributed PV
        dupv = [distributed utility PV (lower voltage connection)? Not sure about this one]
        upv = utility PV
        csp = concentrating solar power
        electrolyzer = below zero because it is a demand for producing H2 that is then used to store energy and generate electricity later
        h2-ct = hydrogen combustion turbine

    EERE Tool electricity source categories -
        Coal
        Petroleum
        Natural Gas
        Solar Photovoltaic
        Wind    
        Nuclear >> new category
        Other Renewable >> new category

    """
    
    nrel_to_eere_mappings = {
        'nuclear' : 'Nuclear', 
        'nuclear-smr' : 'Nuclear', 
        'coal' : 'Coal', 
        'gas-cc' : 'Natural Gas', 
        'gas-ct' : 'Natural Gas', 
        'o-g-s' : 'Petroleum',               
        'hydro' : 'Other Renewable', 
        'geothermal' : 'Other Renewable', 
        'biopower' : 'Other Renewable', 
        'beccs' : 'Other Renewable', 
        'lfill-gas' : 'Other Renewable', 
        'h2-ct' : 'Other Renewable',
        'h2-ct-upgrade' : 'Other Renewable', 
        'wind-ons' : 'Wind', 
        'wind-ofs' : 'Wind', 
        'csp' : 'Solar Photovoltaic', 
        'upv' : 'Solar Photovoltaic', 
        'dupv' : 'Solar Photovoltaic',
        'distpv' : 'Solar Photovoltaic', 
        'battery_2' : 'Other Renewable', 
        'battery_4' : 'Other Renewable', 
        'battery_6' : 'Other Renewable', 
        'battery_8' : 'Other Renewable'
                
        }
    
    def __init__(self, f_name, data_path_prefix):
        
        # data loading
        self.data_path_prefix = data_path_prefix
        self.f_name = f_name
        self.f_sheet = '1_Generation (TWh)'
        self.elec_gen = pd.read_excel(self.path_data + '\\' + self.f_name, sheet_name = self.f_sheet)
        
        # mappings
        self.elec_gen['EERE_Activity'] = np.where(
             [x in self.nrel_to_eere_mappings for x in self.elec_gen['tech'] ],
             self.elec_gen['tech'].map(self.nrel_to_eere_mappings),
             self.elec_gen['tech'] )
        
    def summarize_byEERE_categories (self):
        self.elec_gen.drop(['tech'], axis=1, inplace=True)
        self.elec_gen = self.elec_gen.groupby(['scenario', 'year', 'EERE_Activity'], as_index=False).sum()
        
    def grid_mix_yearly (self):
        tdf1 = self.elec_gen.groupby (['scenario', 'year']).sum()
        tdf2 = pd.merge(self.elec_gen, tdf1, how = 'left', left_on=['scenario', 'year'], right_on=['scenario', 'year']).reset_index()
        tdf2['perc_mix_Generation (TWh)'] = tdf2['Generation (TWh)_x'] / tdf2['Generation (TWh)_y'] * 100
        return tdf2
        

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    #data_path_prefix = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data\\NREL electricity_20220105'
    data_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\EERE Tool\\Data\\Script_data_model\\NREL electricity_20220105'
    f_option = 'report - All Options EFS.xlsx'
    
    init_time = datetime.now()
    
    ob1 = NREL_elec(f_option, data_path_prefix)
    ob1.summarize_byEERE_categories()
    r = ob1.elec_gen
    s = ob1.grid_mix_yearly()
    
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))