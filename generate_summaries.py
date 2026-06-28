import pandas as pd

# Load your data
df = pd.read_csv('final_pro_analysis.csv')

def generate_summary(row):
    # Logic to create a summary based on match stats
    goals = row['home_goals'] + row['away_goals']
    attendance = row['official_attendance']
    
    # Simple logic to create diverse-sounding summaries
    if attendance > 70000:
        summary = "Record-breaking crowd with high energy."
    elif goals > 3:
        summary = "Exciting match with high scoring action."
    elif row['stage_name'] == 'Final':
        summary = "High-stakes atmosphere for the championship."
    else:
        summary = "Standard tournament match with moderate attendance."
    
    return summary

# Apply the function
df['match_summary'] = df.apply(generate_summary, axis=1)

# Save the file with the new column
df.to_csv('final_pro_analysis_with_summaries.csv', index=False)
print("File saved as 'final_pro_analysis_with_summaries.csv'. Now you can run the AI enrichment!")