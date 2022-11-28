# -*- coding: utf-8 -*-
"""
Copyright © 2022, UChicago Argonne, LLC
The full description is available in the LICENSE.md file at location:
    https://github.com/Argonne-National-Laboratory-SAC/DECARB 
    
Created on Tue Nov 22 09:43:33 2022

@author: skar
"""

path_data = 'C:\\Users\\skar\\Box\\EERE SA Decarbonization\\1. Tool\\EERE Tool\\Data\\Script_data_model\\3_output_files'
path_plots = 'C:/Users/skar/Box/saura_self/Proj - EERE Decarbonization/manuscript/plots'

f_data = 'CI_sectoral_ref_mtg.csv'

import pandas as pd
import seaborn as sns
#import matplotlib.pyplot as plt

d = pd.read_csv(path_data + '\\' + f_data)

d1 = d[['Sector', 'Year', 'CI_Reference_perc', 'CI_Mitigation_perc']]

d1 = pd.melt(d1, id_vars=['Sector',
                          'Year'],
             var_name='Case',
             value_name='CI Percentage')

d1.loc[d1['Case'] == 'CI_Reference_perc', 'Case'] = 'Reference'
d1.loc[d1['Case'] == 'CI_Mitigation_perc', 'Case'] = 'Mitigation'
d1['category'] = d1['Sector'] + ', ' + d1['Case'] 

sns.set_theme(style="white", font_scale=1.5)

g = sns.relplot(
    data=d1, kind="line",
    x='Year', y='CI Percentage', hue='Sector', col='Case',
    palette='dark', alpha=.6, height=6,
    facet_kws=dict(margin_titles=True))
g.set(xlabel='Year', ylabel='Percentage CI change')


g.savefig(path_plots + '/' + 'CI_perc_line_plot.png', dpi=400)

d1 = d1.loc[d1['Year'].isin([2025, 2030, 2035, 2040, 2045, 2050]), :]

g = sns.catplot(
    data=d1, kind="bar",
    x='Year', y='CI Percentage', hue='Sector', col='Case',
    palette='dark', alpha=.6, height=6,
    facet_kws=dict(margin_titles=True))

