import pandas as pd

# 1. Load Data
df = pd.read_csv('cleaned_master_data.csv')
venues = pd.read_csv('archive (8)/venues.csv')
stages = pd.read_csv('archive (8)/tournament_stages.csv')

# 2. Merge & Clean
df = df.merge(stages[['stage_id', 'stage_name']], on='stage_id', how='left')
df = df.merge(venues[['venue_id', 'capacity']], on='venue_id', how='left')
df['capacity'] = df['capacity'].fillna(40000)

# 3. Model: Sensitivity Analysis (Scenario Modeling)
# We define three levels of "Average Spend" to show revenue uncertainty
scenarios = {'Conservative': 200, 'Base': 300, 'Aggressive': 450}
observed_fill_rate = 0.997
df['official_attendance'] = (df['capacity'] * observed_fill_rate).astype(int)
df['stage_weight'] = df['stage_name'].map({'Group Stage': 1.0, 'Round of 16': 2.0, 'Quarter-final': 3.0, 'Semi-final': 4.0, 'Final': 5.0}).fillna(1.0)

for name, spend in scenarios.items():
    df[f'revenue_{name}'] = (df['official_attendance'] * spend * df['stage_weight'])

# 4. Venue Efficiency Metric
# Efficiency = Revenue per capacity unit (shows which stadiums earn the most)
df['revenue_efficiency'] = df['revenue_Base'] / df['capacity']

# 5. Export for Dashboarding
df.to_csv('final_pro_analysis.csv', index=False)

print("--- Professional Analysis Engine Complete ---")
print("Exported columns: revenue_Conservative, revenue_Base, revenue_Aggressive, revenue_efficiency")