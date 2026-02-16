import pandas as pd

# Load dataset
df = pd.read_excel("Assignment_dataset.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Convert to numeric
df['q7'] = pd.to_numeric(df['q7'], errors='coerce')   # Age
df['q46'] = pd.to_numeric(df['q46'], errors='coerce') # Risk Score

# Clean consent
df['q2'] = df['q2'].astype(str).str.strip().str.upper()

# Map facility names
facility_mapping = {
    'health_facility9': 'CHC Harsana',
    'health_facility8': 'CHC Rajgarh',
    'health_facility7': 'PHC Dhamred',
    'health_facility6': 'PHC Bahatukala',
    'health_facility5': 'CHC Laxmangarh',
    'health_facility4': 'CHC Pinan',
    'health_facility3': 'CHC Tahla',
    'health_facility2': 'PHC Bhanokhar',
    'health_facility1': 'PHC Ramanagar'
}

df['facility_name'] = df['health_facility'].map(facility_mapping)

# Assignment filtering criteria
filtered = df[
    (df['q2'] == 'YES') &
    (df['q7'] > 30) &
    (df['q46'] > 3)
]

# Required facilities list
required_facilities = [
    'CHC Harsana',
    'CHC Laxmangarh',
    'CHC Pinan',
    'CHC Rajgarh',
    'CHC Tahla',
    'PHC Bahatukala',
    'PHC Bhanokhar',
    'PHC Dhamred',
    'PHC Ramanagar'
]

filtered = filtered[
    filtered['facility_name'].isin(required_facilities)
]

# Generate summary table
summary = filtered.groupby('facility_name').agg(
    total_participants=('facility_name', 'count'),
    avg_age=('q7', 'mean'),
    avg_risk_score=('q46', 'mean'),
    max_risk_score=('q46', 'max'),
    min_risk_score=('q46', 'min')
).reset_index()

# Sort properly
summary = summary.sort_values('facility_name')

# Save
summary.to_excel("facility_summary.xlsx", index=False)

# Show result
print(summary)