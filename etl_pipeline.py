import pandas as pd

# Standardized Mapping
MAPPING = {
    '2018': {'match_date': 'match_date', 'home_team_name': 'home_team', 'away_team_name': 'away_team', 'home_team_score': 'home_goals', 'away_team_score': 'away_goals'},
    '2022': {'date': 'match_date', 'home_team_id': 'home_team', 'away_team_id': 'away_team', 'home_score': 'home_goals', 'away_score': 'away_goals'},
    '2026': {'date': 'match_date', 'home_team_id': 'home_team', 'away_team_id': 'away_team', 'home_score': 'home_goals', 'away_score': 'away_goals'}
}

def clean_attendance(file_path):
    df = pd.read_csv(file_path)
    df['Home'] = df['Home'].str.strip()
    df['Away'] = df['Away'].str.strip()
    df['Attendance'] = df['Attendance'].replace(',', '', regex=True).astype(int)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def run_etl(year, match_file, attendance_file):
    df = pd.read_csv(match_file)
    df = df.rename(columns=MAPPING.get(year, {}))
    
    # Filter only completed matches
    if 'status' in df.columns:
        df = df[df['status'] == 'Completed']
    
    att_df = clean_attendance(attendance_file)
    
    # Create Composite Keys
    df['merge_key'] = pd.to_datetime(df['match_date']).dt.strftime('%Y-%m-%d') + '_' + df['home_team'].astype(str) + '_' + df['away_team'].astype(str)
    att_df['merge_key'] = att_df['Date'].dt.strftime('%Y-%m-%d') + '_' + att_df['Home'] + '_' + att_df['Away']
    
    # Merge Attendance
    df = df.merge(att_df[['merge_key', 'Attendance']], on='merge_key', how='left')
    df = df.rename(columns={'Attendance': 'official_attendance'})
    
    # ID Lookups for 2022/2026
    if year in ['2022', '2026']:
        teams = pd.read_csv('archive (8)/teams.csv')
        venues = pd.read_csv('archive (8)/venues.csv')
        df = df.merge(teams[['team_id', 'team_name']], left_on='home_team', right_on='team_id', how='left').drop(columns=['home_team', 'team_id']).rename(columns={'team_name': 'home_team'})
        df = df.merge(teams[['team_id', 'team_name']], left_on='away_team', right_on='team_id', how='left').drop(columns=['away_team', 'team_id']).rename(columns={'team_name': 'away_team'})
        df = df.merge(venues[['venue_id', 'stadium_name']], on='venue_id', how='left')
        
    return df.drop(columns=['merge_key'], errors='ignore')

if __name__ == "__main__":
    # Process 2022 example
    master_df = run_etl('2022', 'archive (8)/matches.csv', 'archive (6)/Attendance Sheet.csv')
    master_df.to_csv('cleaned_master_data.csv', index=False)
    print("Pipeline Complete: File saved as 'cleaned_master_data.csv'")