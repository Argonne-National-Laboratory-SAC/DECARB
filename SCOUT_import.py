# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Project:EERE Decarbonization
Author: George G. Zaimes, Saurajyoti Kar
Affiliation: Argonne National Laboratory
Date: 03/22/2022
"""
#%%
# Python Packages
import pandas as pd
import os

#%%

# Import Scout Mitigation Results

class SCOUT:
    
    def __init__ (self, ob_units, input_path_SCOUT, input_path_corr):
        
        self.ob_units = ob_units
        self.input_path_SCOUT = input_path_SCOUT
        self.input_path_corr = input_path_corr
        
        #self.f_name = 'scenario_3-1_savings_SA_data_request_v3'
        self.f_name = 'scenario_3-1_savings_SA_data_request_061722'
        
        self.f_out_longform = self.f_name + '_longform.xlsx'
        
        self.f_name = self.f_name + '.xlsx'
        
        self.f_corr_EIA_SCOUT = 'corr_EERE_SCOUT.xlsx'
        self.sheet_corr_EIA_SCOUT = 'Mapping EIA_to_Scout'
        
        self.df_scout = pd.read_excel(self.input_path_SCOUT + '\\' + self.f_name, header = [0,1], index_col = [0,1,2])
        
        self.df_corr_EIA = pd.read_excel(self.input_path_corr + '\\' + self.f_corr_EIA_SCOUT, sheet_name = self.sheet_corr_EIA_SCOUT, header = 3, index_col=None)
        
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
        self.df_scout['Subsector'] = '-'
        
        # Invert the sign of values to represent the amount of energy reduced in the mitigation scenario compared to 'Reference case'
        self.df_scout['Value'] = -1 * self.df_scout['Value']
        
        # Modify naming convention for Migitation Measure
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_DF') & 
                          (self.df_scout['Sector'] == 'Residential'),'Mitigation Case'] = 'Residential: Energy efficiency'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_DF') & 
                          (self.df_scout['Sector'] == 'Commercial'),'Mitigation Case'] = 'Commercial: Energy efficiency'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'FS') & 
                          (self.df_scout['Sector'] == 'Residential'), 'Mitigation Case'] = 'Residential: Fuel switching'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'FS') & 
                          (self.df_scout['Sector'] == 'Commercial'), 'Mitigation Case'] = 'Commercial: Fuel switching'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_of_FS') & 
                          (self.df_scout['Sector'] == 'Residential'), 'Mitigation Case'] = 'Residential: Energy efficiency of Fuel switching'
        self.df_scout.loc[(self.df_scout['Mitigation Case'] == 'EE_of_FS') & 
                          (self.df_scout['Sector'] == 'Commercial'), 'Mitigation Case'] = 'Commercial: Energy efficiency of Fuel switching'
        self.df_scout_test = self.df_scout.copy()        
        # unit conversion
        self.df_scout[['Units', 'Value']] = self.ob_units.unit_convert_df ( self.df_scout[['Units', 'Value']],
                                                                           Unit = 'Units', Value = 'Value')

        # Mapping SCOUT columns for EERE standardization
        self.df_scout = pd.merge(self.df_scout, 
                                 self.df_corr_EIA[['SCOUT: Energy carrier', 'Energy carrier', 'Energy carrier type']].drop_duplicates(), 
                                 how='left', left_on=['Energy carrier'], 
                                 right_on=['SCOUT: Energy carrier']).reset_index(drop=True)
        
        # Rename columns
        self.df_scout.rename(columns={'Energy carrier_y' : 'Energy carrier',
                                      'Units' : 'Unit'}, inplace=True)
        
        # Adding additional columns with values to match existing Environmental Matrix
        self.df_scout['Case'] = 'Mitigation'
        self.df_scout['Data Source'] = 'SCOUT Model'
        self.df_scout.loc[self.df_scout['Energy carrier'] != 'Electricity', 'Scope'] = 'Direct, Combustion'
        self.df_scout.loc[self.df_scout['Energy carrier'] == 'Electricity', 'Scope'] = 'Electricity, Combustion'
        
        # Select and arrange columns
        self.df_scout = self.df_scout[['Data Source', 'Case', 'Mitigation Case', 'Sector', 'Subsector', 
                                       'Energy carrier', 'Energy carrier type', 
                                       'End Use Application', 'Scope', 'Year', 'Value', 'Unit']]
        
        # Data type conversion
        self.df_scout['Year'] = self.df_scout['Year'].astype('float64')
        
        # HHV to LHV conversion
        self.conv_HHV_to_LHV()
        
    def conv_HHV_to_LHV (self):
        self.df_scout = pd.merge(self.df_scout, self.ob_units.hv_EIA[['Energy carrier', 'Energy carrier type', 'LHV_by_HHV']].drop_duplicates(), 
                                    how='left', on=['Energy carrier', 'Energy carrier type'])        
        self.df_scout['Value'] = self.df_scout['Value'] * self.df_scout['LHV_by_HHV']
        self.df_scout.drop(columns=['LHV_by_HHV'], inplace=True)
        
if __name__ == "__main__":
    
    code_path_prefix = 'C:\\Users\\skar\\repos\\EERE_decarb'
    input_path_prefix = code_path_prefix + '\\Data\\1_input_files'
    
    input_path_units = input_path_prefix + '\\Units'  
    input_path_GREET = input_path_prefix + '\\GREET'        
    input_path_corr = input_path_prefix + '\\correspondence_files'
    input_path_SCOUT = input_path_prefix + '\\Buildings\\SCOUT'
         
    os.chdir(code_path_prefix)
    from  unit_conversions import model_units    
    ob_units = model_units(input_path_units, input_path_GREET, input_path_corr)
    
    ob_SCOUT = SCOUT(ob_units, input_path_SCOUT, input_path_corr)
    
    # save processed SCOUT data
    ob_SCOUT.df_scout.to_excel(input_path_SCOUT + '/' + ob_SCOUT.f_out_longform)