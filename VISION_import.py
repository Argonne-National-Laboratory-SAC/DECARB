# -*- coding: utf-8 -*-
"""
Project:EERE Decarbonization
Author: George G. Zaimes, Saurajyoti Kar
Affiliation: Argonne National Laboratory
Date: 04/13/2022
"""
#%%
# Python Packages
import pandas as pd

#%%

class VISION:
    
    def __init__ (self, input_path_VISION, input_path_corr):
        
        # Set Filepaths and Load input files
        
        # Set path and filenames for input files
        self.input_path_VISION = input_path_VISION
        self.input_path_corr = input_path_corr
        
        self.f_name_VISION = 'EERE_VISION Output_Fuel Use_0411.csv'        
        self.f_corr_VISION_EIA = 'corr_vision_ldv.csv'
        
        # Load VISION and correspondence excel workborks
        self.vision = pd.read_csv(self.input_path_VISION + '\\' + self.f_name_VISION, header = 3)        
        self.corr_vision = pd.read_csv(self.input_path_corr + '\\' + self.f_corr_VISION_EIA)
        
        # Foward fill NaN/missing entries 
        self.vision = self.vision.ffill(axis = 0)
        
        # Standardize VISION Results

        # Map to correspondence file (to adjust naming conventions)
        self.vision = pd.merge(self.vision, self.corr_vision, 
                               how='left', 
                               on = ['Sector',
                                     'EIA Subsector',
                                     'VISION Category',
                                     'End-Use Application',
                                     'Powertrain',
                                     'Energy Carrier Type'])

        # Drop un-necessary columns
        self.vision.drop(columns = ['Sector',
                                    'EIA Subsector',
                                    'VISION Category',
                                    'End-Use Application',
                                    'Powertrain',
                                    'Energy Carrier Type',                                    
                                    'Value (quad)',
                                    'Value (Trillion BTU)'], inplace=True)

        # Rename columns
        self.vision.rename(columns = {'Sector: USDT': 'Sector', 
                                      'Subsector: USDT': 'Subsector',
                                      'End Use Application: USDT': 'End Use Application',
                                      'Energy carrier: USDT': 'Energy carrier',
                                      'Energy carrier type: USDT': 'Energy carrier type',
                                      'Value (mmBTU)': 'Value'}, inplace=True)

        # Add new column for units and other additional columns
        self.vision['Data Source'] = 'VISION'
        self.vision['Case'] = 'Mitigation'
        self.vision['Unit'] = 'MMBtu'

        # aggregate values if any
        self.vision = self.vision.groupby(by=['Data Source', 'Case', 'Sector', 'Subsector', 'End Use Application',
                                              'Energy carrier', 'Energy carrier type', 'Year', 'Unit']). \
                                  agg({'Value' : 'sum'}).reset_index()

if __name__ == "__main__":
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
        
    input_path_VISION = input_path_prefix + '\\Transportation'
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    ob_VISION = VISION(input_path_VISION, input_path_corr)