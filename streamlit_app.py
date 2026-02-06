import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- 1. GLOBAL APP CONFIG ---
st.set_page_config(layout="wide", page_title="Radiology Ramadan Hub")

# --- 2. INITIALIZE STAFF DATABASE (State Management) ---
if 'staff_db' not in st.session_state:
    # Creating your 25 employees with default credentials
    st.session_state.staff_db = pd.DataFrame([
        {"Name": f"Tech {i}", "Xray": True, "CT": (3<=i<=4), "MRI": (1<=i<=2), 
         "US": (5<=i<=8), "Mammo": (i>20), "Fluoro": (i>20)} 
        for i in range(1, 26)
    ])

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🌙 Ramadan Scheduler")
page = st.sidebar.radio("Navigation", ["Daily Distribution", "Manage Credentials", "Excel Tools"])

# --- PAGE 1: DAILY DISTRIBUTION ---
if page == "Daily Distribution":
    st.title("📋 Daily Modality Distribution")
    
    # Handover Alert Logic
    now = datetime.now().strftime("%H:%M")
    if "11:45" <= now <= "12:00":
        st.warning("⚠️ R1 Shift ending soon! Please initiate the Handover Checklist for R2 Staff.")
        if st.button("Confirm Handover Complete"):
            st.success("Handover logged successfully.")

    # Shift Selection
    shifts = {
        "R1": "06:00 - 12:00", "R2": "12:00 - 18:00", "R3": "18:00 - 24:00",
        "RD": "06:00 - 18:00", "RN": "18:00 - 06:00"
    }
    selected_shift = st.selectbox("Select Active Shift", list(shifts.keys()))
    st.info(f"Shift Timing: {shifts[selected_shift]}")

    # Modality Grid
    modalities = ["X-Ray (24/7)", "CT", "MRI", "Ultrasound", "Mammo/Fluoro", "BMD/OR"]
    cols = st.columns(3)
    
    for i, mod in enumerate(modalities):
        with cols[i % 3]:
            # Filter staff based on credentials stored in session_state
            if "Mammo" in mod:
                valid_staff = st.session_state.staff_db[st.session_state.staff_db["Mammo"]]["Name"]
            elif "CT" in mod:
                valid_staff = st.session_state.staff_db[st.session_state.staff_db["CT"]]["Name"]
            else:
                valid_staff = st.session_state.staff_db["Name"]
            
            st.selectbox(f"Assign {mod}", ["Unassigned"] + list(valid_staff), key=f"mod_{mod}")

# --- PAGE 2: MANAGE CREDENTIALS ---
elif page == "Manage Credentials":
    st.title("🛡️ Staff Certification Matrix")
    st.write("Update which of your 25 techs are qualified for specific modalities.")
    st.session_state.staff_db = st.data_editor(st.session_state.staff_db, num_rows="dynamic")

# --- PAGE 3: EXCEL TOOLS ---
elif page == "Excel Tools":
    st.title("📊 Excel Integration")
    uploaded_file = st.file_uploader("Upload Monthly Excel Schedule", type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("Excel Schedule Loaded!")
        st.dataframe(df)
    
    st.divider()
    st.subheader("Export to PDF")
    if st.button("Generate Today's PDF"):
        st.write("PDF Generation initiated... (Ensure reportlab is in requirements.txt)")
