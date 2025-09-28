import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Performance & Audit",
    page_icon="📊",
    layout="wide",
)

# --- SHARED STYLES ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }
        .stMetric { border: 1px solid #262730; border-radius: 10px; padding: 15px; background-color: #1a1c22; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); }
        .stButton>button { width: 100%; border-radius: 8px; }
        .st-emotion-cache-1r6slb0 { border-radius: 10px; border: 1px solid #262730; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📊 Performance & Audit Center")
st.caption("Review historical performance trends and audit operational decisions.")
st.divider()

# --- HISTORICAL PERFORMANCE SECTION ---
st.subheader("Historical Performance")
time_period = st.selectbox(
    "Select Time Period",
    ["Last 24 Hours", "Last 7 Days", "Last 30 Days"],
    key="time_period"
)

# --- GENERATE SAMPLE DATA FOR CHARTS ---
def generate_chart_data(period):
    if period == "Last 24 Hours":
        points = 24
        freq = 'H'
    elif period == "Last 7 Days":
        points = 7
        freq = 'D'
    else:
        points = 30
        freq = 'D'
    
    timestamps = pd.to_datetime(pd.date_range(end=pd.Timestamp.now(), periods=points, freq=freq))
    punctuality = np.random.uniform(low=85.0, high=98.0, size=points).round(1)
    avg_delay = np.random.uniform(low=1.5, high=5.0, size=points).round(1)
    
    return pd.DataFrame({
        'Time': timestamps,
        'Punctuality (%)': punctuality,
        'Average Delay (min)': avg_delay
    })

chart_data = generate_chart_data(time_period)

# --- DISPLAY CHARTS ---
col1, col2 = st.columns(2)
with col1:
    fig_punctuality = px.line(
        chart_data, x='Time', y='Punctuality (%)',
        title='Punctuality Over Time', markers=True,
        template='plotly_dark'
    )
    fig_punctuality.update_layout(yaxis_range=[80,100])
    st.plotly_chart(fig_punctuality, use_container_width=True)

with col2:
    fig_delay = px.area(
        chart_data, x='Time', y='Average Delay (min)',
        title='Average Delay Over Time', markers=True,
        template='plotly_dark'
    )
    st.plotly_chart(fig_delay, use_container_width=True)

st.divider()

# --- AUDIT TRAIL SECTION ---
st.subheader("📜 Audit Trail")

audit_data = {
    'Timestamp': pd.to_datetime(['2025-09-28 11:39:35', '2025-09-28 11:40:12', '2025-09-28 11:42:05', '2025-09-28 11:45:30']),
    'User': ['SYSTEM', 'Controller_A', 'Controller_A', 'SYSTEM'],
    'Event Type': ['AI Recommendation', 'User Action', 'Manual Override', 'Conflict Resolution'],
    'Details': [
        "Hold Train 45678 for 6 mins.",
        "Rejected AI Recommendation for Train 45678.",
        "Executed 'Proceed Via Main Line' for Train 45678.",
        "AI automatically rerouted Train 54321 to avoid conflict."
    ]
}
audit_df = pd.DataFrame(audit_data)

# --- FILTERS FOR THE AUDIT LOG ---
filter_col1, filter_col2 = st.columns([1, 2])
with filter_col1:
    user_filter = st.selectbox("Filter by User", ["All"] + list(audit_df['User'].unique()))
with filter_col2:
    event_filter = st.selectbox("Filter by Event Type", ["All"] + list(audit_df['Event Type'].unique()))

filtered_df = audit_df.copy()
if user_filter != "All":
    filtered_df = filtered_df[filtered_df['User'] == user_filter]
if event_filter != "All":
    filtered_df = filtered_df[filtered_df['Event Type'] == event_filter]

# --- DISPLAY THE AUDIT LOG ---
# MODIFICATION: Updated parameter to use_container_width for the dataframe.
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

