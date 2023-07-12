# # -*- coding: utf-8 -*-
# """
# Created on Tue Jun 20 09:19:55 2023

# @author: spatange
# """

## importing libraries
import pandas as pd
import re 

def round_to_tenth(num):
    return round(num)
def API_fix(series):
    return re.sub(r"_na(?![a-zA-Z])", "_NA", series[:-2][17:].lower())
def conversion(num):
    return num / 1000000000.00
def conversion2(num):
    return (num * 293.071070000) / 1000000000.0000 
def get_number_after_table(string):
    pattern = r"Table (\d+)"     
    match = re.search(pattern, string)     
    if match:         
        number = match.group(1)         
        return int(number)
    
# ################################################################## 1

# # Emission End Use 

# emissions_end_use_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-emissions_end_use-.csv').drop_duplicates()
# emissions_end_use_original = pd.read_csv(r'C:\Sagar\EIA Dataset-emissions_end_use_original-.csv').drop_duplicates()
# emissions_end_use_new["Value"] = emissions_end_use_new["Value"].apply(round_to_tenth)
# emissions_end_use_original["Value"] = emissions_end_use_original["Value"].apply(round_to_tenth)
# e_new_value = emissions_end_use_new['Value']
# e_org_value = emissions_end_use_original['Value']
# #print('False' in comparison.unique())
# comparison = e_new_value.reset_index(drop=True).compare(e_org_value.reset_index(drop=True))
# print(comparison)

# ###################################################################

# Energy Demand 

energy_demand_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-energy_demand-.csv')#.drop_duplicates("Series Id")
energy_demand_original = pd.read_csv(r'C:\Sagar\EIA Dataset-energy_demand_original-.csv').drop_duplicates()
energy_demand_original.drop(energy_demand_original[(energy_demand_original['Year'] == 2021)].index, inplace=True)
energy_demand_original.drop(energy_demand_original[(energy_demand_original['Year'] == 2020)].index, inplace=True)
energy_demand_new.drop(energy_demand_new[(energy_demand_new['Year'] == 2021)].index, inplace=True)
energy_demand_new.drop(energy_demand_new[(energy_demand_new['Year'] == 2020)].index, inplace=True)
energy_demand_new = energy_demand_new.reset_index(drop = True)
energy_demand_original = energy_demand_original.reset_index(drop = True)

energy_demand_2023_2021 = pd.DataFrame()

energy_demand_2023_2021["2023"] = energy_demand_new["Value"]
energy_demand_2023_2021["2021"] = energy_demand_original["Value"]
energy_demand_2023_2021["percent difference"] = ((energy_demand_original["Value"] - energy_demand_new["Value"]) / energy_demand_original["Value"])*100

merge_check = pd.merge(energy_demand_original, energy_demand_new, how = 'left',
         on = ['Data Source', 'AEO Case', 'Sector', 'Subsector', 'End Use Application',
                'Energy carrier', 'Energy carrier type', 'Basis', 'Year', 'Unit', 'Case']).reset_index(drop = True)
merge_check.rename(columns = {'Value_x':'value_AEO_2021',
                              'Value_y':'value_AEO_2023'}, inplace = True)
merge_check.drop(columns = ['Generation Type_x', 'Fuel Pool_x', 'Generation Type_y', 'Fuel Pool_y'], inplace = True)
merge_check["percent difference"] = ((merge_check["value_AEO_2021"] - merge_check["value_AEO_2023"]) / merge_check["value_AEO_2021"])*100

print(energy_demand_new.isnull().sum())
merge_check.to_csv('C:\Sagar\merge_check.csv')
#energy_demand_new["Value"] = energy_demand_new["Value"].apply(round_to_tenth)
#energy_demand_original["Value"] = energy_demand_original["Value"].apply(round_to_tenth)
#ed_new = energy_demand_new['Value'].apply(conversion)
#ed_org = energy_demand_original['Value'].apply(conversion)

#comparison = ed_new.reset_index(drop=True).compare(ed_org.reset_index(drop=True))
#print(comparison)



# emissions_end_use_result = pd.concat([emissions_end_use_new, emissions_end_use_original]).drop_duplicates('Value')
energy_demand_result = pd.concat([energy_demand_new, energy_demand_original]).drop_duplicates()

# ######################################################################################################## 1

# # ## Suplemental

# supplimental_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-supplemental-.csv')#.drop_duplicates('Series Id')
# supplimental_org = pd.read_csv(r'C:\Sagar\EIA Dataset-supplemental-.csv')#.drop_duplicates('Series Id')
# supplimental_new["Value"] = supplimental_new["Value"].apply(round_to_tenth)
# supplimental_org["Value"] = supplimental_org["Value"].apply(round_to_tenth)
# supplimental_org['Series Id'] = supplimental_org['Series Id'].apply(API_fix)
# s_new_value = supplimental_new['Series Id']
# s_org_value = supplimental_org['Series Id']
# #s_new_value = supplimental_new['Value']
# #s_org_value = supplimental_org['Value']
# for i in s_org_value.values:
#     if i not in s_new_value.values:
#         print(i)
# comparison = s_new_value.reset_index(drop=True).compare(s_org_value.reset_index(drop=True))
# print(comparison)

# ############################################################################################################# 1

#  ## Chemical

# chemical_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-chemical_industry_supp-.csv')#.drop_duplicates("Series Id")
# chemical_original = pd.read_csv(r'C:\Sagar\EIA Dataset-chemical_industry_supp-.csv')#.drop_duplicates("Series Id")
# chemical_new["Value"] = chemical_new["Value"].apply(round_to_tenth)
# chemical_original["Value"] = chemical_original["Value"].apply(round_to_tenth)
# chem_new = chemical_new["Value"]
# chem_org = chemical_original['Value']
# for i in chem_new.values:
#     if i not in chem_org.values:
#         print(i)

# ########################################################################################################### 1

# Energy Supply

# energy_supply_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-energy_supply-.csv')#.drop_duplicates("Series Id")
# energy_supply_original = pd.read_csv(r'C:\Sagar\Data\1_input_files\EIA\EIA Dataset-energy_supply-.csv')#.drop_duplicates("Series Id")

# energy_supply_new["Value"] = conversion2(energy_supply_new["Value"])
# energy_supply_new["Value"] = round_to_tenth(energy_supply_new["Value"])
# #energy_supply_original["Value"] = round_to_tenth(energy_supply_original["Value"])

# energy_supply_original["Value"] = conversion2(energy_supply_original["Value"])
# energy_supply_original["Value"] = round_to_tenth(energy_supply_original["Value"])
# esup_new = energy_supply_new["Value"]
# esup_org = energy_supply_original['Value']#.apply(API_fix)

# for i in esup_new.values:
#     if i not in esup_org.values:
#           print(i)
        
# ################################################################################################################### 1

# # Energy Price

# energy_price_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-energy_price-.csv')#.drop_duplicates("Series Id")
# energy_price_original = pd.read_csv(r'C:\Sagar\Data\1_input_files\EIA\EIA Dataset-energy_price-.csv')#.drop_duplicates("Series Id")

# energy_price_new["Value"] = round_to_tenth(energy_price_new["Value"])
# energy_price_original["Value"] = round_to_tenth(energy_price_original["Value"])

# eprice_new = energy_price_new["Value"]
# eprice_org = energy_price_original['Value']#.apply(API_fix)

# for i in eprice_new.values:
#     if i not in eprice_org.values:
#           print(i)

#####################################################################################################################

# # Emission energy type

# emission_energy_type_new = pd.read_csv(r'C:\Users\spatange\Documents\Repos\DECARB\Data\1_input_files\EIA\EIA Dataset-emissions_energy_type-.csv')#.drop_duplicates("Series Id")
# emission_energy_type_original = pd.read_csv(r'C:\Sagar\Data\1_input_files\EIA\EIA Dataset-emissions_energy_type-.csv')#.drop_duplicates("Series Id")

# emission_energy_type_new["Value"] = round_to_tenth(emission_energy_type_new["Value"])
# emission_energy_type_original["Value"] = round_to_tenth(emission_energy_type_original["Value"])

# eet_new = emission_energy_type_new["Value"]
# eet_org = emission_energy_type_original['Value']#.apply(API_fix)

# for i in eet_new.values:
#     if i not in eet_org.values:
#            print(i)

#####################################################################################################################





