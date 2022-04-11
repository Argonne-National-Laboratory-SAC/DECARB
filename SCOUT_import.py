# -*- coding: utf-8 -*-
"""
Project:EERE Decarbonization
Author: George G. Zaimes
Affiliation: Argonne National Laboratory
Date: 03/22/2022
"""
#%%
# Python Packages
import pandas as pd

#%%

# Import Scout Mitigation Results

class SCOUT:
    
    def __init__ (self, ob_units, input_path_SCOUT, input_path_corr):
        
        self.ob_units = ob_units
        self.input_path_SCOUT = input_path_SCOUT
        self.input_path_corr = input_path_corr
        
        self.f_name = 'scenario_3-1_savings_SA_data_request_v3.xlsx'
        
        self.f_corr_EIA = 'corr_EERE_SCOUT.xlsx'
        self.sheet_corr_EIA = 'Mapping EIA_to_Scout'
        
        self.df_scout = pd.read_excel(self.input_path_SCOUT + '\\' + self.f_name, header = [0,1], index_col = [0,1,2])
        
        self.df_corr_EIA = pd.read_excel(self.input_path_corr + '\\' + self.f_corr_EIA, sheet_name = self.sheet_corr_EIA, header = 3, index_col=None)
        
        self.df_scout = self.df_scout.stack()
        
        self.df_scout.reset_index(inplace=True)
        
        self.df_scout = pd.melt(self.df_scout, id_vars = ['sector', 'end_use', 'fuel', 'meas_type',] , value_name = 'Value')
        
        self.df_scout = self.df_scout.rename(columns = {'sector':'Sector',
                             'end_use': 'End Use Application',
                             'fuel': 'Energy carrier',
                             'meas_type': 'Mitigation Case',
                             'year': 'Year'
                             }
                  )
        
        # Add in additional columns
        self.df_scout['Units'] = 'Quadrillion Btu'     
        
        # Invert the sign of values to represent the amount of energy reduced in the mitigation scenario compared to 'Reference case'
        self.df_scout['Value'] = -1 * self.df_scout['Value']
        
        # Modify naming convention for Migitation Measure
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_DF') & (self.df_scout['Sector'] == 'Residential'),'Mitigation Case'] = 'Residential: Energy efficiency'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_DF') & (self.df_scout['Sector'] == 'Commercial'),'Mitigation Case'] = 'Commercial: Energy efficiency'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'FS') & (self.df_scout['Sector'] == 'Residential'), 'Mitigation Case'] = 'Residential: Fuel switching'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'FS') & (self.df_scout['Sector'] == 'Commercial'), 'Mitigation Case'] = 'Commercial: Fuel switching'
        
        #self.df_scout['Energy carrier'] = self.df_scout['Energy carrier'].replace({'Electric': 'Electricity',
        #                                                                           'Distillate/Other': 'Distillate Oil'}) 
        
        # unit conversion
        self.df_scout[['Units', 'Value']] = self.ob_units.unit_convert_df ( self.df_scout[['Units', 'Value']],
                                                                           Unit = 'Units', Value = 'Value')

        # Mapping SCOUT columns for EERE standardization
        self.df_scout = pd.merge(self.df_scout, 
                                 self.df_corr_EIA[['Sector', 'Subsector', 'SCOUT: End Use Application', 
                                                   'SCOUT: Energy carrier', 'Energy carrier', 'EIA: Energy carrier type']], 
                                 how='left', left_on=['End Use Application', 'Energy carrier'], 
                                 right_on=['SCOUT: End Use Application', 'SCOUT: Energy carrier']).reset_index(drop=True)
        
        # Rename columns
        self.df_scout.rename(columns={'Sector_y' : 'Sector', 'Energy carrier_y' : 'Energy carrier',
                                      'EIA: Energy carrier type' : 'Energy carrier type',
                                      'Units' : 'Unit'}, inplace=True)
        
        # Select and arrange columns
        self.df_scout = self.df_scout[['Sector', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                                       'End Use Application', 'Year', 'Value', 'Unit']]
                
        
        # Adding additional columns with values to match existing Environmental Matrix
        self.df_scout['Case'] = 'Mitigation'
        self.df_scout['Data Source'] = 'SCOUT Model'
        
        # Data type conversion
        self.df_scout['Year'] = self.df_scout['Year'].astype('float64')
        
        
if __name__ == "__main__":
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    
    input_path_units = input_path_prefix + '\\Units'  
    input_path_GREET = input_path_prefix + '\\GREET'        
    input_path_corr = input_path_prefix + '\\correspondence_files'
    input_path_SCOUT = input_path_prefix + '\\Buildings\\SCOUT'
    
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    ob = SCOUT(ob_units, input_path_SCOUT, input_path_corr)