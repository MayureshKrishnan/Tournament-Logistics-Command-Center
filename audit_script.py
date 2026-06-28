import pandas as pd
import os

def audit_file(file_path, col_to_check=None):
    # Load the file
    df = pd.read_csv(file_path)
    print(f"\n--- Audit Report for: {os.path.basename(file_path)} ---")
    
    # 1. Column Availability
    columns = list(df.columns)
    print(f"Columns found: {columns}")
    
    # 2. Null Rate (Only if column is provided)
    if col_to_check:
        if col_to_check in df.columns:
            null_count = df[col_to_check].isnull().sum()
            null_rate = (null_count / len(df)) * 100
            print(f"Null Rate for '{col_to_check}': {null_rate:.2f}%")
            if null_rate > 15:
                print("!!! ALERT: Null rate > 15% !!!")
        else:
            print(f"!!! ALERT: Column '{col_to_check}' not found in this file !!!")
            
    # 3. Data Types
    print("Data types preview:")
    print(df.dtypes)

# Run audits based on your file structure
# Update 'archive (X)' to match the exact folder name from your screenshot
audit_file('archive (7)/matches.csv') 
# Update the attendance check to match the file's exact header: 'Attendance'
audit_file('archive (6)/Attendance Sheet.csv', col_to_check='Attendance')

# Verify the file path for venues.csv. 
# Check if it is in 'archive (6)' or 'archive (8)' and update accordingly.
# audit_file('archive (8)/venues.csv')audit_file('archive (7)/venues.csv')
# Audit Archive (8)
audit_file('archive (8)/matches.csv') # Compare this against archive (7)
audit_file('archive (8)/matches_detailed.csv') 
audit_file('archive (8)/match_team_stats.csv')