# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:06:43 2023

@author: spatange
"""

## importing libraries
import plotly.graph_objects as go
import urllib, json
import pandas as pd
import random
from itertools import chain
import os

if not os.path.exists('images'):
    os.mkdir('images')
## Set Values:::
# Note: the capitalization conventions have to be the same as the column names in Energy Demand

YearOfInterest = 2050
Facet_1 = 'Fuel Pool'
Facet_2 = 'Sector'
Facet_3 = 'Subsector'
Facet_4 = 'End Use Application'
Case = 'Reference case' # 'Reference case' or 'Mitigation'

### Reading Energy Demand data file, choosing year and case
def change_index (floatt):
    return int(floatt)
def add_space (strang):
    return str(strang) + " "
def remove_space(string):
    return "".join([char for char in string if char != " "])
def count_space(string1):
    count = 0
    for c in string1:
        if c == " ":
            count += 1
    return count
def value_facet_classifacation(string, facets):
    for i in range(len(facets)):
        if string in [x for x in list(df[facets[i]].unique()) if str(x) != 'nan']:
            return i
        elif "".join([char for char in string if char != " "]) == '-':
            return count_space(string)

df_original = pd.read_excel('C:\\Users\\spatange\\Documents\\Repos\\DECARB\\Data\\4_dashboard\\US Decarbonization Tool - test.xlsx', sheet_name='Energy Demand')
df_original = df_original.iloc[3:]
df_original.columns = ['index', 'Case', 'Mitigation Case', 'Sector', 'Subsector', 'End Use Application', 'Energy carrier', "Energy carrier type", 'Basis','Fuel Pool','Year','Unit', 'Value']
df_original['index'] = df_original['index'].apply(change_index)
df_original = df_original.set_index('index')
df_original.drop(df_original[(df_original['Year'] != YearOfInterest)].index, inplace=True)
#df_original.drop(df_original[(df_original['Case'] != Case)].index, inplace=True)
#df.drop(df[(df['End Use Application'] == '-')].index, inplace=True)
df_original = df_original.reset_index(drop = True)
df = df_original.copy()

def create_sankey(Facets, YearOfInterest, remove_null):
    
    ## droping rows that have '-' in the first or second facet
    if remove_null == True:
        df.drop(df[(df[Facets[0]] == '-')].index, inplace=True)
        df.drop(df[(df[Facets[1]] == '-')].index, inplace=True)

    
    ## initializing source, target, value dataframe
    df_temps = []
    df_labels = pd.DataFrame()
    total_values = [0.0] * len(Facets)
        
    ## generating sankey plot dataframe
    for index_fac in range(len(Facets)-1):
        
        ## Initializing "source" and "target" dataframe using two facets at a time
        df_temp = df.groupby([Facets[index_fac],Facets[index_fac+1]])['Value'].count().reset_index()
        
        if remove_null == True:
            df_temp.drop(df_temp[(df_temp[Facets[index_fac]] == '-')].index, inplace=True)
            df_temp.drop(df_temp[(df_temp[Facets[index_fac+1]] == '-')].index, inplace=True)
        else:
            for index, row in df_temp.iterrows():
                if df_temp.at[index, Facets[index_fac]] == '-':
                    df_temp.at[index, Facets[index_fac]] += ' ' * index_fac
                if df_temp.at[index, Facets[index_fac+1]] == '-':
                    df_temp.at[index, Facets[index_fac+1]] += ' ' * (index_fac+1)
        
        
        df_temp.columns = ['source','target','value']
        
        ## Generating "value" data 
        for index, row in df_temp.iterrows():
            df_temp1 = df.drop(df[(df[Facets[index_fac]] != row['source'].rstrip())].index)
            df_temp1.drop(df_temp1[(df_temp1[Facets[index_fac+1]] != row['target'].rstrip())].index, inplace = True)
            df_temp.at[index, 'value'] = df_temp1['Value'].sum() 
            total_values[index_fac+1] = df_temp['value'].sum()    
            
        df_temps.append(df_temp)

    total_values[0] = total_values[1]

        ## detour
    if remove_null == True:

        if len(Facets) == 4:
            df_temp_edit = df.groupby([Facets[1],Facets[2],Facets[3]])['Value'].count().reset_index()
            df_temp_edit.drop(df_temp_edit[(df_temp_edit[Facets[2]] != '-')].index, inplace=True)
            df_temp_edit.drop(df_temp_edit[(df_temp_edit[Facets[3]] == '-')].index, inplace=True)
            df_temp_edit.drop(Facets[2], axis=1, inplace=True)
            df_temp_edit.columns = ['source','target','value']
            for index, row in df_temp_edit.iterrows():
                df_temp1 = pd.DataFrame()
                df_temp1 = df.drop(df[(df[Facets[1]] != row['source'])].index)
                df_temp1.drop(df_temp1[(df_temp1[Facets[3]] != row['target'])].index, inplace = True)
                df_temp_edit.at[index, 'value'] = df_temp1['Value'].sum()
            total_values[3] += df_temp_edit['value'].sum()
            df_temps.append(df_temp_edit)

    df_labels = pd.concat([df_labels, df_temps[0].groupby('source')['value'].sum().reset_index()], axis=0)
    for i in range(len(df_temps)):
        df_label = df_temps[i].groupby('target')['value'].sum().reset_index()
        df_labels = pd.concat([df_labels, df_label], axis=0)
    
    links = pd.concat(df_temps, axis=0)
    unique_source_target = list(pd.unique(links[['source','target']].values.ravel("K")))
    ust_copy = unique_source_target.copy()
                                
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    links['source'] = links["source"].map(mapping_dict)
    links['target'] = links["target"].map(mapping_dict)
    links_dict = links.to_dict(orient='list')
    
    ### adding percents to the labels 
    for index, row in df_labels.iterrows():
        if index == 0:
            if row['source'] in unique_source_target:
                index = unique_source_target.index(row['source'])
                if index < len(unique_source_target) :
                    unique_source_target[index] += " " + str(round((row['value'] / total_values[value_facet_classifacation(row['source'],Facets)])*100,1)) + "%"
        if row['target'] in unique_source_target:
            index = unique_source_target.index(row['target'])
            if index < len(unique_source_target) :
                unique_source_target[index] += " " + str(round((row['value'] / total_values[value_facet_classifacation(row['target'],Facets)])*100,1)) + "%"

    # generating color data
    random_color_node = []
    random_col = []
    for _ in range(len(unique_source_target)):
        random_color_node.append("rgba("+str(random.randint(1,255))+","+str(random.randint(1,255))+","+str(random.randint(1,255))+",0.35)")
    mapping_color_node_dict = {k: v for v, k in enumerate(random_color_node)}
    random_col.append(pd.concat([links['source'], links['target']]).tolist())
    random_col = list(chain.from_iterable(random_col))
    flipped_dict = {value: key for key, value in mapping_color_node_dict.items()}
    random_color_target = [flipped_dict.get(item) for item in random_col]
    
    #generating x-positional data
    xlist = []
    ylist = []
    temp = []
    for element in ust_copy:
        xlist.append(float(value_facet_classifacation(element, Facets)) / float((len(Facets) - 1)))
    for value in sorted(list(set(xlist)), key=float):
        temp.append(xlist.count(value))
    for value in temp:
        for i in range(0,value):
            ylist.append(float(i / value))
    ### creating Sankey diagram data
    fig = go.Figure(data=[go.Sankey(
        arrangement = 'snap',
        domain = dict( x = [0,1], y = [0,1]),
        node = dict(
            pad = 15, 
            thickness = 20, 
            line = dict(color = 'black',width = 0.5), 
            label = unique_source_target,
            x = xlist,
            y = [0.01]*len(xlist),
            color = random_color_node
        ), 
        link = dict(
        source = links_dict['source'],
        target = links_dict['target'],
        value = links_dict['value'],
        color = random_color_target
        ) 
    )])
    
    ## showing sankey diagram
    title = str(YearOfInterest) + " :"
    for i in range(len(Facets)):
        if i != (len(Facets) - 1):
            title = title + ' ' + Facets[i] + ' | '
        else:
            title = title + ' ' + Facets[i] 
        
    fig.update_layout(title_text = title , font_size = 16, width = 1118, height = 1000)
    fig.show()
    fig.write_image("C:\Sagar\SankeyPlotPictures\Sankey.png")
    
    
Facet_1 = 'Fuel Pool'
Facet_2 = 'Sector'
Facet_3 = 'Subsector'
Facet_4 = 'End Use Application'

facets = [Facet_2, Facet_4]
create_sankey(facets, 2050, True)