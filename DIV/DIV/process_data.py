"""
The below code processes the OECD dataset for corporate income tax statutory and targeted small business rates 
for all OECD countries between 2000-2024.
Data is presented in the format of:

[country] [year] [tax rate]

The key for the tax rates in column include:

CITPITCIT_S13_ST: Corporate income tax as a share of total tax paid for the general government sector (S13) at the statutory rate (ST).

CIT_DP_S13_ST: Corporate income tax rate on distributed profit for the general government sector at the statutory rate.

CPITCIT_S13_ST: Combined personal and corporate income tax rates for the general government sector at the statutory rate.

DP_S13_ST: Distributed profit rate for the general government sector at the statutory rate.

FWHT_S13_ST: Final withholding tax rate for the general government sector at the statutory rate.

GUD_S13_ST: Grossed up dividend for the general government sector at the statutory rate.

IDTC_S13_ST: Imputation or dividend tax credit for the general government sector at the statutory rate.

IR_S13_ST: Imputation rate for the general government sector at the statutory rate.

NPT_S13_ST: Net personal tax for the general government sector at the statutory rate.

PITGUD_S13_ST: Personal income tax rate on grossed-up dividend for the general government sector at the statutory rate.

PITPITCIT_S13_ST: Personal income tax as a share of total tax paid for the general government sector at the statutory rate.

PTDP_S13_ST: Pre-tax distributed profit rate for the general government sector at the statutory rate.
"""

import json
import pandas as pd

# Load the JSON data
with open('oecd_div.json', 'r') as file:
    data = json.load(file)

# Extract the series data
series_data = data['data']['dataSets'][0]['series']

# Extract the dimensions from the structure
dimensions = data['data']['structure']['dimensions']['series']

# Create a list to store the rows
rows = []

# Iterate through the series and observations
for series_key, series_info in series_data.items():
    # Split the series key to get dimension values
    dimension_values = series_key.split(':')
    
    # Create a dictionary for the row
    row = {}
    
    # Add dimension values to the row
    for i, dim in enumerate(dimensions):
        row[dim['id']] = dim['values'][int(dimension_values[i])]['id']
    
    # Add observations to the row
    for time_period, obs in series_info['observations'].items():
        year = data['data']['structure']['dimensions']['observation'][0]['values'][int(time_period)]['id']
        new_row = row.copy()
        new_row['Year'] = year
        new_row['Value'] = obs[0]
        
        # Append the row to the list
        rows.append(new_row)

# Create a DataFrame from the rows
df = pd.DataFrame(rows)

# Create a unique identifier for each type of tax rate
df['Tax_Type'] = df['MEASURE'] + '_' + df['SECTOR'] + '_' + df['TARGETING']

# Pivot the table to have tax types as columns
df_pivot = df.pivot_table(
    values='Value', 
    index=['REF_AREA', 'Year'], 
    columns='Tax_Type', 
    aggfunc='first'
)

# Reset the index to turn the pivot table into a regular DataFrame
df_pivot = df_pivot.reset_index()

# Rename the 'REF_AREA' column to 'Country'
df_pivot = df_pivot.rename(columns={'REF_AREA': 'Country'})

# Sort the DataFrame by Country and Year
df_pivot = df_pivot.sort_values(['Country', 'Year'])

# Print the first few rows and data info
print("\nFirst few rows of the reformatted DataFrame:")
print(df_pivot.head())
print("\nDataFrame info:")
print(df_pivot.info())

# Save the DataFrame to an Excel file
df_pivot.to_excel('oecd_div_tax.xlsx', index=False)

print("Data has been successfully parsed, reformatted, and saved to 'oecd_div_tax.xlsx'.")
