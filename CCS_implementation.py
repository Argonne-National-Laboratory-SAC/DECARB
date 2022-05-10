# -*- coding: utf-8 -*-
"""
Created on Wed May  4 14:36:37 2022

@author: skar
"""

import pandas as pd
import numpy as np

class CCS_implementation:

 def __init__ (self, input_path_prefix):
     
     # loading files and data
     self.input_path_prefix = input_path_prefix
     self.input_path_ccs = self.input_path_prefix + '\\' + 'CCS'
     
     self.f_ccs_adopt_rate = 'CCS_adopt_rate.csv'
     self.f_ccs_demand = 'CCS_demand.csv'
     self.f_ccs_to_implement = 'CCS_to_implement.csv'
     
     self.ccs_adopt_rate = pd.read_csv(self.input_path_ccs + '\\' + self.f_ccs_adopt_rate, header = 3, index_col=None)
     self.ccs_demand = pd.read_csv(self.input_path_ccs + '\\' + self.f_ccs_demand, header = 3, index_col=None)
     self.ccs_to_implement = pd.read_csv(self.input_path_ccs + '\\' + self.f_ccs_to_implement, header = 3, index_col=None)
     
     self.ccs_sequestration_potential = 0.9 # define the fraction of incoming CO2 getting sequestred by CCS facility
     

 def model_2d_ccs (self, x, y, deg = 2):
        p = np.polyfit(x, y, deg)
        
        return np.poly1d(p)
    
 def pred_2d_ccs (self, ccs_model, x_pred):
        value = ccs_model (x_pred)
        if value < 0: # Truncate predictions those are negative
            return 0
        else:
            return value
 
 # Calculating CCS implementation trend as per AMO report   
 def trend_2d_ccs (self, 
                 df, colname_time='Year', colname_value='Value'):
        """
        Provide CCS adoption data for a sector and subsector and obtain fraction trend over time

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        colname_time : TYPE
            DESCRIPTION.
        colname_value : TYPE
            DESCRIPTION.

        Returns
        -------
        df_trend : TYPE
            DESCRIPTION.

        """
        ccs_model = self.model_2d_ccs(df[colname_time], df[colname_value])
        
        df_trend = pd.DataFrame({'Year' : np.linspace(min(df[colname_time]), max(df[colname_time]), max(df[colname_time]) - min(df[colname_time]) + 1 ),
                                 'frac' : [ self.pred_2d_ccs(ccs_model, curr_yr)
                                            for curr_yr in range(min(df[colname_time]), (max(df[colname_time])+1)) ] })        
        return df_trend
  
 def calc_ccs_trend(self):
        
        self.ccs_trend =  self.ccs_adopt_rate.groupby(['Sector', 'Subsector', 'Scenario'])[['Year', 'Value']]. \
                                              apply(self.trend_2d_ccs, 'Year', 'Value').reset_index()
 
 def implement_ccs(self, env_df, 
                   sector, 
                   colname_sector = 'Sector', 
                   colname_subsector = 'Subsector',
                   colname_scope = 'Scope',
                   colanme_year = 'Year',                   
                   colname_formula = 'Formula',
                   colname_multiplier = 'Marker',
                   colname_emissions = 'Total Emissions',
                   colname_emissions_unit = 'Emissions Unit'):
        
     self.calc_ccs_trend()   
     
     self.env_df = env_df
         
     # Filter by the sector to implement CCS and GHG emission as CO2
     self.env_df = self.env_df.loc[(self.env_df[colname_sector] == sector) &
                         (self.env_df[colname_formula] == 'CO2'), : ] 
     
     # Identify the subsectors and scope to implement CCS as per input file
     self.env_df = pd.merge(self.env_df, self.ccs_to_implement,
                       how = 'left',
                       on = [colname_sector, colname_subsector, colname_scope]).reset_index(drop=True)
     
     # Filter by rows that are marked for CCS implementation
     self.env_df = self.env_df.loc[self.env_df['Marker'] == 1, : ]
     
     # Summarize total emissions by the needed columns
     self.env_df = self.env_df.groupby([colname_sector, colname_subsector, colanme_year,
                              colname_emissions_unit, colname_formula, colname_multiplier]).agg({colname_emissions : 'sum'}).reset_index()
     
     self.env_df_prev = self.env_df
     
     # Filter by rows those have positive emissions
     self.env_df = self.env_df.loc[self.env_df[colname_emissions] > 0, :]
     
     # Merge CCS implementation trend
     self.env_df = pd.merge(self.env_df, self.ccs_trend[[colname_sector, colname_subsector, colanme_year, 'frac']],
                       how='left',
                       on=[colname_sector, colname_subsector, colanme_year]).reset_index(drop=True)
        
     # Calculate CO2 sequestration through CCS
     self.env_df[colname_emissions] = -1 * self.env_df[colname_emissions] * self.env_df['frac'] * self.ccs_sequestration_potential     
   
 def calc_ccs_activity(self, ob_units,
                       colname_sector = 'Sector',
                       colname_subsector = 'Subsector',
                       colname_emissions = 'Total Emissions'):
       
       self.ccs_process = pd.merge(self.ccs_demand, self.env_df,
                                   how='left',
                                   on=['Sector', 'Subsector']).reset_index(drop=True)
       
       # unit conversion       
       self.ccs_process.loc[~self.ccs_process['Emissions Unit'].isnull(), ['Emissions Unit', 'Total Emissions']] = \
         ob_units.unit_convert_df(self.ccs_process.loc[~self.ccs_process['Emissions Unit'].isnull(), ['Emissions Unit', 'Total Emissions']],
          Unit = 'Emissions Unit', Value = 'Total Emissions',          
          if_given_unit=True, given_unit = self.ccs_process['unit_denominator'][0])
       
       # Calculate total energy demand for CCS activity by energy carrier 
       self.ccs_process['Value'] = self.ccs_process[colname_emissions] * self.ccs_process['Value']
       
       #self.ccs_process.drop(columns=['unit_denominator'], inplace=True)

# Create object and call function if script is ran directly
if __name__ == "__main__":    
    
    # Please change the path to data folder per your computer
    
    input_path_prefix = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\1_input_files'
    
    ob = CCS_implementation(input_path_prefix)
    
    ob.calc_ccs_trend()