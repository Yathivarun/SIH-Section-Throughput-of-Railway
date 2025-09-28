import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Railway Traffic Control DSS",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
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
    # MODIFICATION: Replaced broken URL and updated parameter to use_container_width.
    st.image(
        "Live_map.jpg",
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
    
    # MODIFICATION: Updated parameter to use_container_width for the dataframe.
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

