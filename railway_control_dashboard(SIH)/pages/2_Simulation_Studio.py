import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Simulation Studio",
    page_icon="🤔",
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
        # MODIFICATION: Replaced crashing URL and updated parameter to use_container_width.
        st.image(
            "Simulation_map.png",
            caption="Visual forecast of train movements based on the selected scenario.",
            use_container_width=True
        )
        st.warning("The simulation predicts 2 new conflicts and a significant increase in average delay.")

    else:
        st.info("Build a scenario and click 'Run Simulation' to see the predicted impact here.")

