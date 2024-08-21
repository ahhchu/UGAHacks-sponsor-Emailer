import pandas as pd

# Reading the data
df_new = pd.read_csv('data/new.csv')[['First Name', 'Email', 'Company Name for Emails']]
df_check = pd.read_csv('data/check.csv')[['First Name', 'Email', 'Company Name for Emails']]

# Merging on 'Email' and 'Company Name for Emails' to find unique entries in df_new
merged_df = df_new.merge(df_check, on=['Email'], how='left', indicator=True, suffixes=('', '_from_check'))
merged_df = merged_df[merged_df['_merge'] == 'left_only']
merged_df = df_new.merge(df_check, on=['Company Name for Emails'], how='left', indicator=True, suffixes=('', '_from_check'))

df_cleaned = merged_df[merged_df['_merge'] == 'left_only']

# Selecting the relevant columns and printing the cleaned data
print(df_cleaned)

# Saving the cleaned data to a new batch file
df_cleaned[['First Name', 'Email', 'Company Name for Emails']].to_csv('data/batch.csv', index=False)

# Concatenating cleaned new entries with the old list and removing duplicates by Email and Company Name for Emails

df_check_updated = pd.concat([df_check, df_cleaned[['First Name', 'Email', 'Company Name for Emails']]]).drop_duplicates(subset=['Email', 'Company Name for Emails'])

# Writing the updated DataFrame to CSV
print("\n")
print(df_check_updated)
#df_check_updated.to_csv('data/check.csv', index=False)
