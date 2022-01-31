# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 11:40:22 2021

@author: skar
"""

""" A dictionary for unit conversions and a caller \
function to return 1 in case the unit conversation is not available """
    
"""
sources:
https://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/nrcs142p2_022760.pdf
https://www.eia.gov/energyexplained/units-and-calculators/
Excel version of EERE Tool
"""

import pandas as pd 

path_data = 'C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization\\data'
f_unit_conv = 'Unit Conversion.xlsx'
unit_conv = pd.read_excel(path_data + '\\' + f_unit_conv)

unit1_per_unit2 = {
 # feedstock or fuel based physical units:

 'Barley_lb_per_bu' : 48,
 'Corn_lb_per_bu' : 56,
 'Oats_lb_per_bu' : 32,
 'Sorghum_lb_per_bu' : 56,
 'Soybeans_lb_per_bu' : 60,
 'Wheat_lb_per_bu' : 60,
 'Barley_dry_per_wet' : 0.3, # fraction of dry matter
 'Corn_dry_per_wet' : 0.3,
 'Oats_dry_per_wet' : 0.3,
 'Sorghum_dry_per_wet' : 0.3,
 'Soybeans_dry_per_wet' : 0.3,
 'Wheat_dry_per_wet' : 0.3,
 
 'Crude Oil_barrel_per_MMBtu' : (1/ 5.691), 
 'Coal_st_per_MMBtu' : ( 1/ (20.6736101163927 * 0.907185) ), # GREET1_2021, Fuel_Specs, Coal Mix for Electricity Generation
 'Diesel_gal_per_MMBtu' : (1/ 0.138490), # GREET1_2021, Fuel_Specs, Low-sulfur diesel
 'Motor Gasoline_gal_per_MMBtu' : (1/ 0.12043862), # GREET1_2021, Fuel_Specs, Gasoline
 'Jet Fuel_gal_per_MMBtu' : (1/ 0.132948694386834), # GREET1_2021, Fuel_Specs, Conventional Jet Fuel
 'Residential distillate Fuel Oil/Heating Oil_gal_per_MMBtu' : (1/ 0.150110), # GREET1_2021, Fuel_Specs, Residual Oil HHV

 
 # physical only units
 
 'U.S.ton_per_lb' : 0.0005,
 'MMBtu_per_kWh' : 0.003412,
 'MMBtu_per_BkWh' : 3412,
 'MMBtu_per_GJ' : 0.947817
 } 

def unit_conv (conv):
    if conv in unit1_per_unit2:
        return unit1_per_unit2[conv]
    else:
        return 1