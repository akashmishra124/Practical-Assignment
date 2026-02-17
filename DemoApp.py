import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Health Risk Screening Dashboard",
    layout="wide"
)

# Title
st.title("Health Risk Screening Dashboard")
st.markdown("Interactive dashboard for screening data analysis")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("Assignment_dataset.xlsx")
    df.columns = df.columns.str.strip()
    df['q7'] = pd.to_numeric(df['q7'], errors='coerce')
    df['q46'] = pd.to_numeric(df['q46'], errors='coerce')
    df['q2'] = df['q2'].astype(str).str.strip().str.upper()
    return df

df = load_data()

# Facility mapping
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

# Sidebar filters
st.sidebar.header("Filters")

selected_facility = st.sidebar.multiselect(
    "Select Facility",
    options=df['facility_name'].dropna().unique(),
    default=df['facility_name'].dropna().unique()
)

risk_filter = st.sidebar.slider(
    "Minimum Risk Score",
    min_value=int(df['q46'].min()),
    max_value=int(df['q46'].max()),
    value=3
)

age_filter = st.sidebar.slider(
    "Minimum Age",
    min_value=int(df['q7'].min()),
    max_value=int(df['q7'].max()),
    value=30
)

# Apply filters
filtered = df[
    (df['q2'] == 'YES') &
    (df['q7'] >= age_filter) &
    (df['q46'] >= risk_filter) &
    (df['facility_name'].isin(selected_facility))
]

# Summary table
summary = filtered.groupby('facility_name').agg(
    Participants=('facility_name', 'count'),
    Average_Age=('q7', 'mean'),
    Average_Risk=('q46', 'mean')
).reset_index()

# Display metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Participants", len(filtered))
col2.metric("Average Age", round(filtered['q7'].mean(), 1))
col3.metric("Average Risk Score", round(filtered['q46'].mean(), 1))

# Show table
st.subheader("Summary Table")
st.dataframe(summary, use_container_width=True)

# Charts
st.subheader("Visualizations")

col1, col2 = st.columns(2)

# Bar chart
fig_bar = px.bar(
    summary,
    x='facility_name',
    y='Participants',
    title="Participants by Facility",
    color='Participants'
)

col1.plotly_chart(fig_bar, use_container_width=True)

# Pie chart
fig_pie = px.pie(
    summary,
    names='facility_name',
    values='Participants',
    title="Participant Distribution"
)

col2.plotly_chart(fig_pie, use_container_width=True)

# Line chart
fig_line = px.line(
    filtered,
    x='q7',
    y='q46',
    color='facility_name',
    title="Risk Score vs Age"
)

st.plotly_chart(fig_line, use_container_width=True)

# Download option
st.download_button(
    "Download Summary CSV",
    summary.to_csv(index=False),
    "facility_summary.csv"

)

