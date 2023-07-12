# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:15:04 2023

@author: spatange
"""
#importing stuff
import requests
import pandas as pd

#table names will in this data set and both are compared
table_names_2023 = pd.DataFrame()
table_names_2021 = pd.DataFrame()

## getting table names

# for tableNumber in range(1,150):
#     url = "https://api.eia.gov/v2/aeo/2023/data/?frequency=annual&data[0]=value&facets[tableId][]=" + str(tableNumber) + "&facets[history][]=PROJECTION&facets[scenario][]=ref2023&start=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=3&api_key=1735fae01847596363c6500ff42de276"
#     r = requests.get(url)
#     json_data = r.json()
#     cnt = 0
#     while 'error' in json_data:                 
#         r_processor = requests.get(url)
#         json_data_processor = r_processor.json()
#         json_data = json_data_processor
#         cnt+=1
#         if cnt > 1000:
#             break   
#     df_temp = pd.DataFrame(json_data.get('response').get('data'),columns = ['tableName']).drop_duplicates()
#     table_names_2023 = pd.concat([table_names_2023, df_temp])

# for tableNumber in range(1,150):
#     url = "https://api.eia.gov/v2/aeo/2021/data/?frequency=annual&data[0]=value&facets[tableId][]=" + str(tableNumber) + "&facets[history][]=PROJECTION&facets[scenario][]=ref2021&start=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=3&api_key=1735fae01847596363c6500ff42de276"
#     r = requests.get(url)
#     json_data = r.json()
#     cnt = 0
#     while 'error' in json_data:                 
#         r_processor = requests.get(url)
#         json_data_processor = r_processor.json()
#         json_data = json_data_processor
#         cnt+=1
#         if cnt > 1000:
#             break    
#     df_temp = pd.DataFrame(json_data.get('response').get('data'),columns = ['tableName']).drop_duplicates()
#     table_names_2021 = pd.concat([table_names_2021, df_temp])
# for tableNumber in range(1,150):
    
########################################################################################

table_series_2023 = pd.DataFrame()
table_series_2021 = pd.DataFrame()
for tableNumber in range(1,150):
    url = "https://api.eia.gov/v2/aeo/2023/data/?frequency=annual&data[0]=value&facets[tableId][]=" + str(tableNumber) + "&facets[history][]=PROJECTION&facets[scenario][]=ref2023&start=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key=1735fae01847596363c6500ff42de276"
    r = requests.get(url)
    json_data = r.json()
    cnt = 0
    while 'error' in json_data:                 
        r_processor = requests.get(url)
        json_data_processor = r_processor.json()
        json_data = json_data_processor
        cnt+=1
        if cnt > 1000:
            break   
    df_temp = pd.DataFrame(json_data.get('response').get('data'),columns = ['seriesId']).drop_duplicates()
    table_series_2023 = pd.concat([table_series_2023, df_temp])

for tableNumber in range(1,150):
    url = "https://api.eia.gov/v2/aeo/2021/data/?frequency=annual&data[0]=value&facets[tableId][]=" + str(tableNumber) + "&facets[history][]=PROJECTION&facets[scenario][]=ref2021&start=2050&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key=1735fae01847596363c6500ff42de276"
    r = requests.get(url)
    json_data = r.json()
    cnt = 0
    while 'error' in json_data:                 
        r_processor = requests.get(url)
        json_data_processor = r_processor.json()
        json_data = json_data_processor
        cnt+=1
        if cnt > 1000:
            break   
    df_temp = pd.DataFrame(json_data.get('response').get('data'),columns = ['seriesId']).drop_duplicates()
    table_series_2021 = pd.concat([table_series_2021, df_temp])
table_series_2023.drop_duplicates()
table_series_2021.drop_duplicates()

