import pandas as pd
import os
from datetime import datetime

def clean(path):
    # Reading the data
    df_new = pd.read_csv(path)
    df_check = pd.read_csv('data/test2.csv')

    # Ensure required columns exist
    required_columns = ['First Name', 'Email', 'Company Name']
    for df in [df_new, df_check]:
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in CSV file")

    # Select only the required columns
    df_new = df_new[required_columns]
    df_check = df_check[required_columns]

    # Perform cleaning on df_check
    df_check = df_check.drop_duplicates()
    df_check = df_check.dropna(subset=['Email', 'First Name'])
    string_columns = df_check.select_dtypes(include=['object']).columns
    df_check[string_columns] = df_check[string_columns].apply(lambda x: x.str.strip())

    # Merging on 'Email' to find unique entries in df_new
    merged_df = df_new.merge(df_check, on=['Email'], how='left', indicator='merge_email', suffixes=('', '_from_check'))
    merged_df = merged_df[merged_df['merge_email'] == 'left_only']

    # Merging on 'Company Name' to further filter unique entries
    merged_df = merged_df.merge(df_check, on=['Company Name'], how='left', indicator='merge_company', suffixes=('', '_from_check'))
    df_cleaned = merged_df[merged_df['merge_company'] == 'left_only']

    # Selecting the relevant columns and printing the cleaned data
    df_cleaned = df_cleaned[required_columns]
    print(df_cleaned)

    # Saving the cleaned data to batch.csv
    df_cleaned.to_csv('data/batch.csv', index=False)

    # Only add new, non-duplicate entries to test2.csv
    df_check_updated = pd.concat([df_check, df_cleaned]).drop_duplicates(subset=['Email', 'Company Name'], keep='first')

    # Update 'First Name' for existing entries
    df_check_updated = df_check_updated.set_index('Email')
    df_new_indexed = df_new.set_index('Email')
    df_check_updated.update(df_new_indexed)
    df_check_updated = df_check_updated.reset_index()

    print("\nUpdated check file:")
    print(df_check_updated)
    
    current_date = datetime.now()
    date_str = current_date.strftime("%Y-%m-%d-%H%M")
    
    # Calculate new rows
    new_rows = len(df_check_updated) - len(df_check)
    
    # Overwrite test2.csv with the updated data
    df_check_updated.to_csv('data/test2.csv', index=False)
    
    print(f"\nAdded {new_rows} new rows to test2.csv")
    print(f"Total rows in test2.csv: {len(df_check_updated)}")
    
    return 'data/test2.csv'

if __name__ == '__main__':
    clean('data/fake.csv')
