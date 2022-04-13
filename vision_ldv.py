#%% Import Necessary Packages

# Python Packages
import pandas as pd

#%% Set Filepaths and Load input files

# Set path and filenames for input files
path = 'C:\\Users\\gzaimes\\Desktop\\'
fname_vision = 'EERE_VISION Output_Fuel Use_0411.xlsx'
fname_corr = 'corr_vision_ldv.xlsx'

# Load VISION excel workbork
vision = pd.read_excel(path + '\\' + fname_vision, header = 3)
corr_vision = pd.read_excel(path + '\\' + fname_corr)

#%% Standardize VISION Results

# Foward fill NaN/missing entries 
vision = vision.ffill(axis = 0)

# Map to correspondence file (to adjust naming conventions)
vision = pd.merge(vision, corr_vision, how='left', on = ['Sector', 
                                                         'EIA Subsector',
                                                         'VISION Category',
                                                         'End-Use Application',
                                                         'Powertrain',
                                                         'Energy Carrier Type']
                  )


# Drop un-necessary columns
vision = vision.drop(columns = ['Sector',
                                'EIA Subsector',
                                'VISION Category',
                                'End-Use Application',
                                'Powertrain',
                                'Energy Carrier Type',
                                'Year','Value (quad)',
                                'Value (Trillion BTU)']
                     )

# Rename columns
vision = vision.rename(columns = {'Sector: USDT': 'Sector', 
                                  'Subsector: USDT': 'Subsector',
                                  'End Use Application: USDT': 'End Use Application',
                                  'Energy carrier: USDT': 'Energy carrier',
                                  'Energy carrier type: USDT': 'Energy carrier type',
                                  'Value (mmBTU)': 'Value'}
                       )

# Add new column for units
vision['Units'] = 'MMBtu'

# Reorganize columns
vision = vision[['Sector', 'Subsector', 'End Use Application',
       'Energy carrier', 'Energy carrier type','Units','Value']]
