# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:29:46 2022

@Project: EERE Decarbonization
@Authors: Saurajyoti Kar
@Affiliation: Argonne National Laboratory
@Date: 04/20/2022

Summary: Class defining various utility functions for the EERE Decarbonization tool
@author: skar
"""

import pandas as pd
import numpy as np

class Utilities:    
    
    def calc_LCIA_with_EFs(self, df, corr_EF_GREET, ob_ef, elec_gen_em_mtg_agg_m):
        
        # Seperate electric and non-electric activities
        
        df_elec = df.loc[df['Energy carrier'] == 'Electricity', : ]
        df = df.loc[~(df['Energy carrier'] == 'Electricity'), : ]

        # Merge GREET correspondence table
        df = pd.merge(df, corr_EF_GREET, how='left', 
                      on=['Sector', 'Scope', 'Subsector', 'Energy carrier', 'Energy carrier type', 
                      'End Use Application']).reset_index(drop=True)

        # Merge GREET EF
        df = pd.merge(df, ob_ef.ef_raw, 
                      how='left', on=['Case', 'Scope', 'Year', 'GREET Pathway'])

        # Merge NREL mitigation scenario electricity CIs to VISION
        df_elec = pd.merge(df_elec, 
                           elec_gen_em_mtg_agg_m[['Formula', 'Emissions Unit', 'Energy Unit', 'Year', 'CI_elec_mtg']], 
                           how='left',
                           on=['Year'])
        df_elec.rename(columns={'CI_elec_mtg' : 'CI'}, inplace=True)

        df.rename(columns={'Unit (Numerator)' : 'Emissions Unit',
                                       'Unit (Denominator)' : 'Energy Unit',
                                       'Reference case' : 'CI'}, inplace=True)
        df.drop(columns=['GREET Version', 'GREET Tab', 'GREET Pathway', 'Elec0'], inplace=True)

        # Concatenate electric and non-electric activities
        df = pd.concat([df, df_elec], axis = 0).reset_index(drop=True)

        df['Total Emissions'] = df['Value'] * df['CI']
        
        return df
    
    
    def trend_linear(self, df, colname_time, start_frac, end_frac):
        """
        Function to create a linearly spaced multiplier dataframe for implementation
        of mitigation objectives, assuming they reach mitigation targets linearly.
    
        Parameters
        ----------
        df : pandas.DataFrame
            Must have a column with <colname_time> numeric values.
        colname_time : String
            String to specify the name of the column that has time in df.
        start_frac : Numeric
            Value to start linear interpolation.
        end_frac : Numeric
            Value to end linear interpolation.
    
        Returns
        -------
        df_mult : pandas.DataFrame
            Data frame containing a linearly spaced <colname_time> and fraction multiplier.
    
        """
        self.df = df.copy()
        self.df[colname_time] = self.df[colname_time].astype(int)
        df_mult = pd.DataFrame({'Year' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ), 
                                'mtg_frac' : np.linspace(start_frac, end_frac, max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ) } )
        return df_mult
    
    def model_2d_ammonia(self, 
                         x = [2020, 2030, 2040, 2050],
                         y = [0, 0.08, 0.25, 0.50],    # percentage replacement of conventional fossil based ammonia by green ammonia
                         deg = 2):
        p = np.polyfit(x, y, deg)
        
        self.m_2d_ammonia = np.poly1d(p)
    
    def trend_2d_ammonia(self, x_pred):                # Predict Green ammonia implementation over year
        value = self.m_2d_ammonia (x_pred)
        if value < 0: # Truncate predictions those are negative
            return 0
        else:
            return value
    
    def adoption_curve (self,
                        min_val,
                        max_val,
                        k,
                        start_yr,
                        end_yr,
                        curr_yr,
                        a):
        x = curr_yr
        x_0 = int ( (start_yr + end_yr) /2 )
        val = min_val + (max_val - min_val) * pow ((1 / (1 + np.exp( -k * (x - x_0)))), a) 
        return val
    
    def efficiency_improvement (self, 
                                df, colname_time, colname_value,
                                trend_start_val,
                                trend_end_val,
                                trend_type = 'adoption curve',
                                min_val = 0,
                                max_val = 1,
                                k = 0.5,
                                start_yr = 2020,
                                end_yr = 2050,
                                a = 1):
        self.trend_type = trend_type
        
        if self.trend_type == 'linear':
            self.df_trend_ef = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : self.trend_linear(df[[colname_time]], colname_time, trend_start_val , trend_end_val)})
            df = pd.merge(df, self.df_trend_ef, how='left', left_on=colname_time, right_on='time').reset_index(drop=True)            
            df[colname_value] = -1 * df[colname_value] * df['frac']
        
        elif self.trend_type == 'adoption curve':
            self.df_trend_ef = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : [ self.adoption_curve(min_val, max_val, k, start_yr, end_yr, curr_yr, a) 
                                                            for curr_yr in range(min(self.df[colname_time]), (max(self.df[colname_time])+1)) ] })
            df = pd.merge(df, self.df_trend_ef, how='left', left_on=colname_time, right_on='time').reset_index(drop=True)            
            df[colname_value] = -1 * df[colname_value] * df['frac'] * trend_end_val
        
        df.drop(columns=['time', 'frac'], inplace=True)
        
        return df
    
    def fuel_switching (self,
                        df, colname_time, colname_value, colname_energy_carrier, colname_energy_carrier_type,
                        to_energy_carrier, to_energy_carrier_type,
                        feedstock_convert_frac,
                        trend_start_val,
                        trend_end_val,                        
                        trend_type = 'adoption curve',
                        min_val = 0,
                        max_val = 1,
                        k = 0.5,
                        start_yr = 2020,
                        end_yr = 2050,
                        a = 1):
        
        self.trend_type = trend_type
        
        if self.trend_type == 'linear':
            self.df_trend_fs = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : self.trend_linear(df[[colname_time]], colname_time, trend_start_val , trend_end_val)})
        
        elif self.trend_type == 'adoption curve':
            self.df_trend_fs = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : [ self.adoption_curve(min_val, max_val, k, start_yr, end_yr, curr_yr, a) 
                                                            for curr_yr in range(min(self.df[colname_time]), (max(self.df[colname_time])+1)) ] })
        
        df = pd.merge(df, self.df_trend_fs, how='left', left_on=colname_time, right_on='time').reset_index(drop=True)
        
        # Rows for new fuels
        df_fs = df.copy()
        df_fs[colname_value] = df_fs[colname_value] * df_fs['frac'] * feedstock_convert_frac
        df_fs[colname_energy_carrier] = to_energy_carrier
        df_fs[colname_energy_carrier_type] = to_energy_carrier_type
                        
        # Rows to subtract existing fuels
        df_fs_sub = df.copy()
        df_fs_sub[colname_value] = -1 * df_fs_sub[colname_value] * df_fs_sub['frac'] * trend_end_val 
        
        df = pd.concat([df_fs, df_fs_sub], axis=0).reset_index(drop=True)
        
        df.drop(columns=['time', 'frac'], inplace=True)
        
        return df
    
    def calc_H2_by_energy_NG (self, vol_H2, LHV_NG = 983, LHV_H2 = 290):  # LHV values are from GREET 2021 in units of BTU/ft^3. NG and H2 are gaseous fuels.
        return  1 / (1 + ( (1 - vol_H2) * LHV_NG / (vol_H2 * LHV_H2) ) )
    
    def fuel_switching_H2NG (self,
                        df, colname_time, colname_value, colname_energy_carrier, colname_energy_carrier_type,
                        to_energy_carrier, to_energy_carrier_type,
                        trend_start_val,
                        trend_end_val,                        
                        trend_type = 'adoption curve',
                        min_val = 0,
                        max_val = 1,
                        k = 0.5,
                        start_yr = 2020,
                        end_yr = 2050,
                        a = 1):
        
        self.trend_type = trend_type
        
        if self.trend_type == 'linear':
            self.df_trend_fs = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : self.trend_linear(df[[colname_time]], colname_time, trend_start_val , trend_end_val)})
        
        elif self.trend_type == 'adoption curve':
            self.df_trend_fs = pd.DataFrame({'time' : np.linspace(min(self.df[colname_time]), max(self.df[colname_time]), max(self.df[colname_time]) - min(self.df[colname_time]) + 1 ),
                                          'frac' : [ self.adoption_curve(min_val, max_val, k, start_yr, end_yr, curr_yr, a) 
                                                            for curr_yr in range(min(self.df[colname_time]), (max(self.df[colname_time])+1)) ] })
        
        df = pd.merge(df, self.df_trend_fs, how='left', left_on=colname_time, right_on='time').reset_index(drop=True)
        
        # Rows for new fuels
        df_fs = df.copy()
        df_fs[colname_value] = df_fs[colname_value] * [self.calc_H2_by_energy_NG (x) for x in df_fs['frac']]
        df_fs[colname_energy_carrier] = to_energy_carrier
        df_fs[colname_energy_carrier_type] = to_energy_carrier_type
                        
        # Rows to subtract existing fuels
        df_fs_sub = df.copy()
        df_fs_sub[colname_value] = -1 * df_fs_sub[colname_value] * df_fs_sub['frac'] * trend_end_val       
        
        df = pd.concat([df_fs, df_fs_sub], axis=0).reset_index(drop=True)
        
        df.drop(columns=['time', 'frac'], inplace=True)
        
        return df 
    
    