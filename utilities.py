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