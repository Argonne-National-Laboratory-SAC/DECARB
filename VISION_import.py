# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
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
    
    def __init__ (self, ob_units, input_path_VISION, input_path_corr):
        
        # Set Filepaths and Load input files
        self.ob_units = ob_units
        
        # Set path and filenames for input files
        self.input_path_VISION = input_path_VISION
        self.input_path_corr = input_path_corr
        
        self.f_name_VISION_LDV = 'EERE_VISION Output_LDV_Fuel Use_0411.csv'   
        self.f_name_VISION_MDV = 'EERE_VISION Output_MDV_Fuel Use_0419.csv'  
        self.f_name_VISION_HDV = 'EERE_VISION Output_HDV_Fuel Use_0419.csv'  
        
        self.f_corr_VISION_EIA = 'corr_vision.csv'
        
        # Load VISION and correspondence excel workborks
        vision_ldv = pd.read_csv(self.input_path_VISION + '\\' + self.f_name_VISION_LDV, header = 3)  
        vision_mdv = pd.read_csv(self.input_path_VISION + '\\' + self.f_name_VISION_MDV, header = 3)  
        vision_hdv = pd.read_csv(self.input_path_VISION + '\\' + self.f_name_VISION_HDV, header = 3)  
        
        self.corr_vision = pd.read_csv(self.input_path_corr + '\\' + self.f_corr_VISION_EIA)
        
        # Concatenate vision data
        vision_ldv['Energy Carrier'] = '-'
        vision_mdv['Powertrain'] = '-'
        vision_hdv[['Powertrain', 'Energy Carrier']] = '-'
        self.vision = pd.concat([vision_ldv, vision_mdv, vision_hdv], axis=0).reset_index()
        
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
                                     'Energy Carrier',
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
        # convert HHV to LHV
        self.conv_HHV_to_LHV()
    
    def conv_HHV_to_LHV (self):
        self.vision = pd.merge(self.vision, self.ob_units.hv_EIA[['Energy carrier', 'Energy carrier type', 'LHV_by_HHV']].drop_duplicates(), 
                                    how='left', on=['Energy carrier', 'Energy carrier type'])        
        self.vision['Value'] = self.vision['Value'] * self.vision['LHV_by_HHV']
        self.vision.drop(columns=['LHV_by_HHV'], inplace=True)

if __name__ == "__main__":
        
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    input_path_GREET = input_path_prefix + '\\GREET' 
    input_path_units = input_path_prefix + '\\Units'
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    input_path_VISION = input_path_prefix + '\\Transportation'
    input_path_corr = input_path_prefix + '\\correspondence_files'
    
    ob_VISION = VISION(ob_units, input_path_VISION, input_path_corr)