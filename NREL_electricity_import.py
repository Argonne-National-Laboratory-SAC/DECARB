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
        'nuclear-smr' : 'Nuclear, SMR', 
        'coal' : 'Coal', 
        'gas-cc' : 'Natural Gas, Combined Cycle', 
        'gas-ct' : 'Natural Gas, Combustion Turbine', 
        'o-g-s' : 'Petroleum',               
        'hydro' : 'Conventional Hydroelectric Power', 
        'pumped-hydro' : 'Pumped Storage and Other',
        'geothermal' : 'Geothermal', 
        'biopower' : 'Wood and Other Biomass', 
        'beccs' : 'Biopower, CCS', 
        'lfill-gas' : 'Landfill Gas', 
        'h2-ct' : 'Hydrogen, Combustion Turbine',
        'h2-ct-upgrade' : 'Hydrogen, Combustion Turbine', 
        'wind-ons' : 'Wind', 
        'wind-ofs' : 'Offshore Wind', 
        'csp' : 'Solar Thermal', 
        'upv' : 'Solar Photovoltaic', 
        'dupv' : 'Solar Photovoltaic',
        'distpv' : 'Solar Photovoltaic', 
        'battery_2' : 'Battery Storage', 
        'battery_4' : 'Battery Storage', 
        'battery_6' : 'Battery Storage', 
        'battery_8' : 'Battery Storage',
        'battery_10' : 'Battery Storage',
        'electrolyzer' : 'Electrolyzer',
        'Canada' : 'Electricity, Imports'   # US Average Grid Mix for BAU Case  
        }
    
    def __init__(self, ob_units, input_path_elec, input_path_corr, f_name_option = 'report - All Options EFS.xlsx'):
        
        # data loading
        
        self.ob_units = ob_units
        
        self.input_path_elec = input_path_elec + '\\' + 'NREL electricity_20220105'
        self.input_path_corr = input_path_corr
                
        self.sheet_gen = '1_Generation (TWh)'
        self.sheet_capa = '2_Capacity (GW)'
        
        self.file_corr_elec_gen = 'corr_elec_gen.csv'
        
        self.NREL_elec = {  'file_option' : f_name_option,
                            'generation' : '',
                            'capacity' : ''
                          }
        
        self.NREL_elec['generation'] = pd.read_excel(self.input_path_elec + '\\' + self.NREL_elec['file_option'], sheet_name = self.sheet_gen)
        self.NREL_elec['capacity'] = pd.read_excel(self.input_path_elec + '\\' + self.NREL_elec['file_option'], sheet_name = self.sheet_capa)
        
        self.corr_elec_gen = pd.read_csv(input_path_corr + '\\' + self.file_corr_elec_gen, header = 3)
        
        # Mapping technology to generation categories as per the EERE Tool
        
        self.NREL_elec['generation']['Energy carrier type'] = np.where(
             [x in self.nrel_to_eere_mappings for x in self.NREL_elec['generation']['tech'] ],
             self.NREL_elec['generation']['tech'].map(self.nrel_to_eere_mappings),
             self.NREL_elec['generation']['tech'] )
        
        self.NREL_elec['capacity']['Energy carrier type'] = np.where(
             [x in self.nrel_to_eere_mappings for x in self.NREL_elec['capacity']['tech'] ],
             self.NREL_elec['capacity']['tech'].map(self.nrel_to_eere_mappings),
             self.NREL_elec['capacity']['tech'] )
        
        self.process_EERE()
                
    def process_EERE (self, min_year = 2020, max_year = 2050):
        
        # rename columns and create a column for unit
        self.NREL_elec['generation'].rename(columns = {
            'year' : 'Year',
            'Generation (TWh)' : 'Electricity Production'}, inplace = True)
        
        self.NREL_elec['generation']['Energy Unit'] = 'TWh'
        #self.NREL_elec['capacity']['Energy Unit'] = 'GW'
        
        self.NREL_elec['generation']['Sector'] = 'Electric Power'
        self.NREL_elec['generation']['Subsector'] = 'Electric Power Sector'
        self.NREL_elec['generation']['Case'] = 'Mitigation'
        self.NREL_elec['generation']['Mitigation Case'] = 'NREL Electric Power Decarb'
        self.NREL_elec['generation']['Energy carrier'] = 'Electricity'
        self.NREL_elec['generation']['End Use Application'] = 'Electricity Generation'
        
        # Subset data for relevent years for EERE tool
        self.NREL_elec['generation'] = self.NREL_elec['generation'].loc[(self.NREL_elec['generation']['Year'] >= min_year) & 
                                                                        (self.NREL_elec['generation']['Year'] <= max_year) , : ]
               
        self.NREL_elec['generation'].drop(['tech'], axis=1, inplace=True)
        self.NREL_elec['generation'] = self.NREL_elec['generation'].\
            groupby(['Sector', 'Subsector', 'Case', 'Mitigation Case', 'Year', 'Energy carrier', 'Energy carrier type','Energy Unit'], as_index=False). \
            agg({'Electricity Production' : 'sum'}).reset_index()
                        
        # unit conversion
        self.NREL_elec['generation'][['Energy Unit', 'Electricity Production']] = \
          self.ob_units.unit_convert_df(self.NREL_elec['generation'][['Energy Unit', 'Electricity Production']],
                                   Unit = 'Energy Unit', Value = 'Electricity Production')
        
        # Merge electric generation
        self.NREL_elec['generation'] = pd.merge(self.NREL_elec['generation'], self.corr_elec_gen, how='left', on=['Sector', 'Energy carrier', 'Energy carrier type']).reset_index(drop=True)
       
    """
    def generation_grid_mix_yearly (self):
        
        tdf1 = self.NREL_elec['generation'].groupby (['scenario', 'year']).sum()
        
        tdf2 = pd.merge(self.NREL_elec['capacity'], tdf1, how = 'left', left_on=['scenario', 'year'], right_on=['scenario', 'year']).reset_index()
        
        tdf2['perc_mix_Generation (TWh)'] = tdf2['Generation (TWh)_x'] / tdf2['Generation (TWh)_y'] * 100
        
        return tdf2
      """  

if __name__ == '__main__':
    
    # Please change the path to data folder per your computer
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    
    input_path_elec = input_path_prefix + '\\Electricity'   
    input_path_units = input_path_prefix + '\\Units'  
    input_path_GREET = input_path_prefix + '\\GREET'        
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    init_time = datetime.now()
    
    ob1 = NREL_elec(ob_units, input_path_elec, input_path_corr)    
    
    print( 'Elapsed time: ' + str(datetime.now() - init_time))