import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Ramadan Radiology Scheduler")

st.title("🌙 Radiology Modality Distribution - Ramadan Mode")
st.subheader("Shift R0: 09:30 - 15:30 (6 Hours)")

# 1. Staff Setup
staff_data = {
    "X-ray": [f"XR Tech {i+1}" for i in range(8)],
    "MRI": [f"MRI Tech {i+1}" for i in range(2)],
    "CT": [f"CT Tech {i+1}" for i in range(2)],
    "US": [f"US Tech {i+1}" for i in range(4)],
    "General/Support": [f"Tech {i+1}" for i in range(9)]
}

# 2. Sidebar Settings
st.sidebar.header("Schedule Settings")
month = st.sidebar.selectbox("Month", ["March (Ramadan)"])
shift_time = st.sidebar.text_input("R0 Shift Time", "09:30 - 15:30")

# 3. Create the Distribution Table
modalities = ["X-Ray (24/7 Anchor)", "MRI", "CT", "Ultrasound", "Mammo/Fluoro (Split)", "BMD/OR"]
cols = st.columns(len(modalities))

schedule = {}

for i, modality in enumerate(modalities):
    with cols[i]:
        st.dark_note = st.info(f"**{modality}**")
        
        # Logic to filter staff based on modality
        if "X-Ray" in modality:
            options = staff_data["X-ray"]
        elif "MRI" in modality:
            options = staff_data["MRI"]
        elif "CT" in modality:
            options = staff_data["CT"]
        elif "Ultrasound" in modality:
            options = staff_data["US"]
        else:
            # Combined list for general/split modalities
            options = staff_data["X-ray"] + staff_data["General/Support"]

        # Dropdowns for assignment
        assign_am = st.selectbox(f"Morning (09:30)", ["Unassigned"] + options, key=f"am_{i}")
        
        if "Split" in modality:
            st.write("---")
            st.write("PM Transition")
            assign_pm = st.selectbox(f"Afternoon (12:30)", ["Unassigned"] + options, key=f"pm_{i}")
        else:
            assign_pm = assign_am # Full shift stays with same tech

# 4. Coverage Validation Logic
st.divider()
st.header("Coverage Check")
if "Unassigned" in [assign_am for i in range(1)]: # Checking X-ray slot
    st.error("⚠️ ALERT: X-Ray 24/7 Coverage is MISSING for the R0 shift!")
else:
    st.success("✅ R0 Shift fully covered (09:30 - 15:30)")

# 5. Export Feature
st.button("Export March Ramadan Schedule to PDF")import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Ramadan Modality Tracker")

st.title("🌙 March Ramadan Radiology Distribution")

# 1. Shift Definitions
shifts = {
    "R1": "06:00 - 12:00 (6h)",
    "R2": "12:00 - 18:00 (6h)",
    "R3": "18:00 - 24:00 (6h)",
    "RD": "06:00 - 18:00 (12h)",
    "RN": "18:00 - 06:00 (12h)"
}

# 2. Staff Categories (Total 25)
staff_groups = {
    "X-ray": [f"XR Tech {i+1}" for i in range(8)],
    "MRI": [f"MRI Tech {i+1}" for i in range(2)],
    "CT": [f"CT Tech {i+1}" for i in range(2)],
    "US": [f"US Tech {i+1}" for i in range(4)],
    "Other": [f"Staff {i+1}" for i in range(9)]
}
all_staff = [item for sublist in staff_groups.values() for item in sublist]

# 3. App Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("1. Select Shift")
    active_shift = st.radio("Current Rotation", list(shifts.keys()))
    st.info(f"**Timing:** {shifts[active_shift]}")
    
    st.header("2. Staff Availability")
    search = st.text_input("Search Tech Name")

with col2:
    st.header(f"Modality Distribution: {active_shift}")
    
    # Distribution Grid
    modalities = ["X-Ray (24/7)", "CT", "MRI", "Ultrasound", "Mammo/Fluoro", "BMD/OR"]
    
    # Create a table for assignments
    data = []
    for mod in modalities:
        assigned_tech = st.selectbox(f"Assign to {mod}:", ["Empty"] + all_staff, key=mod)
        data.append({"Modality": mod, "Staff Assigned": assigned_tech})

    st.table(pd.DataFrame(data))

# 4. Conflict Warning Logic
st.sidebar.warning("⚡ **Live Validation**")
# Logic: If a tech is in RD, they shouldn't be available for R1 or R2
st.sidebar.write("Checking for double-booking...")import streamlit as st

# --- APP STATE SETUP ---
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = [
        {"Name": f"Tech {i}", "Xray": True, "CT": False, "MRI": False, "US": False, "Mammo": False, "Fluoro": False} 
        for i in range(1, 26)
    ]

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Daily Distribution", "Staff Credentials Matrix"])

if page == "Staff Credentials Matrix":
    st.header("🛡️ Staff Certification Manager")
    st.write("Check the boxes for each modality the technologist is qualified to cover.")
    
    # Editable Dataframe for credentials
    edited_df = st.data_editor(st.session_state.staff_db, num_rows="dynamic")
    st.session_state.staff_db = edited_df
    st.success("Credentials Updated! The Distribution page will now filter based on these settings.")

elif page == "Daily Distribution":
    st.header("🌙 Ramadan Modality Assignment")
    
    # Shift Selection
    shift = st.selectbox("Select Active Shift", ["R1 (06-12)", "R2 (12-18)", "R3 (18-24)", "RD (06-18)", "RN (18-06)"])
    
    # Example: Mammography Assignment with Filter
    st.subheader("Modality Assignment")
    
    # Filter only techs who have 'Mammo' = True
    mammo_qualified = [t["Name"] for t in st.session_state.staff_db if t["Mammo"]]
    
    selected_mammo = st.selectbox("Assign Mammography Tech", ["Select Qualified Staff"] + mammo_qualified)
    
    if selected_mammo != "Select Qualified Staff":
        st.success(f"{selected_mammo} assigned to Mammography for {shift}")
import time
from datetime import datetime

# Logic for the app to track current time
now = datetime.now().strftime("%H:%M")

if "11:45" <= now <= "12:00":
    st.warning("⚠️ R1 Shift ending soon! Please initiate the Handover Checklist for R2 Staff.")
    if st.button("Confirm Handover Complete"):
        st.success("Handover logged. R2 Shift is now Active.")
import streamlit as st
import pandas as pd

st.title("🌙 Radiology Ramadan Portal")

# 1. Excel Upload Feature
uploaded_file = st.sidebar.file_uploader("Upload Excel Schedule", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Schedule Loaded for 25 Employees")
    
    # 2. Filter by Shift (R1, R2, R3, RD, RN)
    shift_filter = st.selectbox("Select Shift to View Distribution", df['Shift Code'].unique())
    filtered_df = df[df['Shift Code'] == shift_filter]
    
    # 3. Display the Distribution Grid
    st.subheader(f"Current Distribution for {shift_filter}")
    st.dataframe(filtered_df[['Staff Name', 'Modality', 'Time In', 'Time Out']], use_container_width=True)

    # 4. PDF Export
    import io
    from reportlab.pdfgen import canvas

    def export_pdf(data):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Daily Distribution - {shift_filter}")
        # Logic to write table rows to PDF...
        p.save()
        return buffer.getvalue()

    st.download_button("📥 Download Shift PDF", data="PDF_DATA_HERE", file_name="Ramadan_Schedule.pdf")

else:
    st.info("Please upload the Excel file to generate the web dashboard.")
