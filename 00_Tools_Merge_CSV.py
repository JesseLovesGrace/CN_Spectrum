import os
import glob
import pandas as pd

#####################################################################
# The CSV file of merged data would be stored under project directory
# And please use "utf-8-sig" instead of "utf-8"
#####################################################################

# Set the directory containing the CSV files
directory = r'C:\Users\jesse\Desktop\Master Thesis\02_Experiments_with_Answers\Have_Babies'

# List all CSV files in the directory
all_files = glob.glob(os.path.join(directory, '*.csv'))

# Initialize an empty list to store dataframes
dfs = []

# Iterate over each CSV file and load it into a dataframe
for filename in all_files:
    df = pd.read_csv(filename, encoding='utf-8-sig')  # Make sure to specify the correct encoding for Chinese text
    dfs.append(df)

# Concatenate all dataframes into one
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('Merged_Have_Babies.csv', index=False, encoding='utf-8-sig')
# Specify the correct encoding for Chinese text with 'utf-8-sig'
