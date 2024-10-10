import pandas as pd
import os
from datetime import datetime
def clean(path):
    
    # Reading the data
    df_new = pd.read_csv(path)[['First Name', 'Email', 'Company Name']]
    df_check = pd.read_csv('data/check.csv')[['First Name', 'Email', 'Company Name']]

    # Merging on 'Email' and 'Company Name for Emails' to find unique entries in df_new
    merged_df = df_new.merge(df_check, on=['Email'], how='left', indicator=True, suffixes=('', '_from_check'))
    merged_df = merged_df[merged_df['_merge'] == 'left_only']
    merged_df = df_new.merge(df_check, on=['Company Name'], how='left', indicator=True, suffixes=('', '_from_check'))

    df_cleaned = merged_df[merged_df['_merge'] == 'left_only']

    # Selecting the relevant columns and printing the cleaned data
    print(df_cleaned)

    # Saving the cleaned data to a new batch file
    df_cleaned[['First Name', 'Email', 'Company Name']].to_csv('data/batch.csv', index=False)

    # Concatenating cleaned new entries with the old list and removing duplicates by Email and Company Name for Emails

    df_check_updated = pd.concat([df_check, df_cleaned[['First Name', 'Email', 'Company Name']]]).drop_duplicates(subset=['Email', 'Company Name'])

    # Writing the updated DataFrame to CSV
    print("\n")
    print(df_check_updated)
    current_date = datetime.now()
    date_str = current_date.strftime("%Y-%m-%d-%H%M")
    os.rename('data/check.csv', 'data/check_save'+date_str+".csv")
    df_check_updated.to_csv('data/check.csv', index=False)
    return 'data/check.csv'

if __name__ == '__main__':
    clean(os.path.join('data/rawtest_cc.csv'))
