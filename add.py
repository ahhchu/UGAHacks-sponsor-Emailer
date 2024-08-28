import pandas as pd

# Reading the data from recorded.csv and renaming the columns to match check.csv
df_new = pd.read_csv('data/recorded.csv')[['Contact Name','Email', 'Company Name']]
df_new = df_new.rename(columns={'Contact Name': 'First Name', 'Company Name': 'Company Name for Emails'})

# Reading the data from check.csv
df_check = pd.read_csv('data/check.csv')

# Merging on 'Email' and 'Company Name for Emails' to find unique entries in df_new
merged_df = df_new.merge(df_check, on=['Email', 'Company Name for Emails'], how='left', indicator=True, suffixes=('', '_from_check'))

# Filtering out entries already present in df_check
df_new_entries = merged_df[merged_df['_merge'] == 'left_only']

df_new_entries = df_new_entries[['First Name', 'Email', 'Company Name for Emails']]
print(df_new_entries)
# Concatenating cleaned new entries with the old list and removing duplicates by Email and Company Name for Emails
df_check_updated = pd.concat([df_check, df_new_entries]).drop_duplicates(subset=['Email', 'Company Name for Emails'])

# Writing the updated DataFrame to CSV
df_check_updated.to_csv('data/check.csv', index=False)

print("\nUpdated 'check.csv' with new entries:")
print(df_check_updated)
