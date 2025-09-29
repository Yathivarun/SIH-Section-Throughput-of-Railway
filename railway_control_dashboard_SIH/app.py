import streamlit as st
import pandas as pd
import time
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION (APPLIES TO ALL PAGES) ---
st.set_page_config(
    page_title="AI Railway Traffic Control DSS",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SHARED STYLES (APPLIES TO ALL PAGES) ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }
        .stMetric { border: 1px solid #262730; border-radius: 10px; padding: 15px; background-color: #1a1c22; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); }
        .stButton>button { width: 100%; border-radius: 8px; }
        /* Style for containers */
        .st-emotion-cache-1r6slb0 { border-radius: 10px; border: 1px solid #262730; }
    </style>
""", unsafe_allow_html=True)


# --- PAGE 1: LIVE OPERATIONS ---
def live_operations_page():
    # --- HEADER SECTION ---
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col1:
        st.title("Live Operations Dashboard")
    with col2:
        st.metric(label="Status", value="● LIVE", help="Real-time data feed is active.")
    with col3:
        st.metric(label="Punctuality", value="94.2%", delta="0.2%", help="Percentage of trains on time.")
    with col4:
        st.metric(label="Avg. Delay", value="2.8m", delta="-0.1m", delta_color="inverse", help="Average delay across all trains in the section.")

    st.divider()

    # --- MAIN LAYOUT ---
    left_column, right_column = st.columns([1, 2])

    # --- LEFT COLUMN: Recommendations & Manual Control ---
    with left_column:
        st.subheader("🤖 AI Recommendation")
        with st.container(border=True):
            st.info("Hold Train **45678 (Freight)** at **Siding SL-02** for **6 minutes**.")
            st.caption("REASON: To allow high-priority Train 12301 (Rajdhani) to pass, preventing a projected 15-minute delay.")
            
            rec_col1, rec_col2 = st.columns(2)
            if rec_col1.button("✅ Accept", type="primary", use_container_width=True):
                st.toast("✅ Recommendation Accepted! Executing action.", icon="👍")
            if rec_col2.button("❌ Reject", use_container_width=True):
                st.toast("❌ Recommendation Rejected. Awaiting manual override.", icon="👎")

        st.subheader("🕹️ Manual Override")
        with st.container(border=True):
            st.text_input("Train ID", placeholder="e.g., 12301", key="manual_train_id")
            st.selectbox("Action", ["Proceed Via Main Line", "Hold at Next Station", "Route to Siding"], key="manual_action")
            if st.button("Execute Command", type="primary", use_container_width=True):
                st.success("Manual command sent successfully!")
                
        st.subheader("📜 Event Log")
        with st.container(border=True, height=220):
            st.text("[11:39:35] System Initialized. Awaiting controller input.")
            st.text("[11:39:35] AI recommendation generated.")
            st.text("[11:39:22] Train 12301 departed Station A.")
            st.text("[11:38:50] Train 45678 approaching Siding SL-02.")
            st.text("[11:37:15] Train 20825 arrived at Station B.")

    # --- RIGHT COLUMN: Map & Train List ---
    with right_column:
        st.subheader("🗺️ Network Visualization")
        st.image(
            "https://raw.githubusercontent.com/Yathivarun/SIH-Section-Throughput-of-Railway/refs/heads/main/railway_control_dashboard_SIH/Live_map.jpg", # Placeholder image
            caption="Live network view showing train positions between Station A and Station B.",
            use_container_width=True
        )

        st.subheader("📋 Train List (In Section)")
        
        train_data = {
            'ID': ['12301', '45678', '20825', '12859', '54321'],
            'TYPE': ['Rajdhani', 'Freight', 'Express', 'Express', 'Local'],
            'NEXT STOP': ['Raipur', 'Nagpur', 'Durg', 'Nagpur', 'Durg'],
            'ETA': ['16:45', '17:10', '16:22', '18:05', '17:30'],
            'STATUS': ['On Time', 'Delayed 6m', 'Early 3m', 'On Time', 'Delayed 12m']
        }
        df = pd.DataFrame(train_data)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

# --- PAGE 2: SIMULATION STUDIO ---
def simulation_studio_page():
    st.title("🤔 \"What-If\" Simulation Studio")
    st.caption("Test hypothetical scenarios to understand their impact before taking action.")
    st.divider()

    # --- LAYOUT ---
    left_column, right_column = st.columns([1, 2])

    # --- LEFT COLUMN: SCENARIO BUILDER ---
    with left_column:
        st.subheader("Scenario Builder")
        with st.container(border=True):
            scenario_type = st.selectbox(
                "Select Scenario Type",
                ["Introduce Train Delay", "Add Unscheduled Train", "Schedule Maintenance Block"]
            )
            
            if scenario_type == "Introduce Train Delay":
                st.text_input("Train ID to Delay", "12301")
                st.slider("Delay Duration (minutes)", 5, 60, 15)
            
            elif scenario_type == "Add Unscheduled Train":
                st.selectbox("Train Type", ["Freight", "Express", "Maintenance"])
                st.time_input("Departure Time")
                st.selectbox("Starting Point", ["Station A", "Station B"])

            elif scenario_type == "Schedule Maintenance Block":
                st.selectbox("Track Section", ["Section A-1", "Section B-2", "Main Line 1"])
                st.slider("Block Duration (hours)", 1, 4, 2)
            
            if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
                with st.spinner("Calculating impact..."):
                    time.sleep(3)
                st.session_state.simulation_run = True

    # --- RIGHT COLUMN: IMPACT ANALYSIS & VISUALIZATION ---
    with right_column:
        st.subheader("Predicted Impact Analysis")
        
        if 'simulation_run' in st.session_state and st.session_state.simulation_run:
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Projected Punctuality", value="88.1%", delta="-6.1%")
            col2.metric(label="Projected Avg. Delay", value="7.2m", delta="+4.4m")
            col3.metric(label="Potential Conflicts", value="2", delta="2")
            
            st.subheader("Visual Simulation")
            st.image(
                "https://raw.githubusercontent.com/Yathivarun/SIH-Section-Throughput-of-Railway/refs/heads/main/railway_control_dashboard_SIH/Simulation_map.png", # Placeholder image
                caption="Visual forecast of train movements based on the selected scenario.",
                use_container_width=True
            )
            st.warning("The simulation predicts 2 new conflicts and a significant increase in average delay.")

        else:
            st.info("Build a scenario and click 'Run Simulation' to see the predicted impact here.")


# --- PAGE 3: PERFORMANCE AUDIT ---
def performance_audit_page():
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
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Live Operations", "Simulation Studio", "Performance & Audit"])

if page == "Live Operations":
    live_operations_page()
elif page == "Simulation Studio":
    simulation_studio_page()
elif page == "Performance & Audit":
    performance_audit_page()
