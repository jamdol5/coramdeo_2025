import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from db_utils import save_attendance_to_db, get_attendance_summary  # Import specific functions

def app():
    custom_css = """
    <style>
        div[data-testid='HorizontalBlock'] {
            width: 1000%;  /* Adjust the width to be full-width */
            height: 100px; /* Set a specific height, adjust as needed */
            background-color: lightblue; /* Adding background color to visualize the change */
        }

        div.row-widget.stTextInput {
                display: flex;
                flex-direction: row;
                align-items: center;
        }
        .input-form .row-widget.stTextInput > div {
            flex: 3;
        }
        .input-form label {
            font-weight: bold;
            margin-right: 1px;
            flex-grow: 0;
            flex-shrink: 0;
            text-align: right;
            width: 10000px;  # Adjust the width based on your label length
        }
        
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

    # Get the database connection from session state
    conn = st.session_state.db_connection

    # Define the names directly in a dictionary
    names_dict = {
        "10/11학년 남자": ["김지온","김지석","김동원","김민상","구세경","배지호","서예담","신유찬","윤민상","임요셉","이용조","주아(Jaron)","하정민","온유닮"]
    }

    # Create the Roster dictionary dynamically
    Roster = {grade: [{"label": name, "default":False} for name in names] for grade, names in names_dict.items()}

    # Initialize attendance tracking
    at = {grade: {} for grade in names_dict.keys()}

    # Create a Streamlit expander and display the values
    st.title('Student Roster')
    
    for grade, students in Roster.items():
        with st.expander(grade):
            for student in students:
                at[grade][student["label"]] = st.checkbox(student["label"], key=student["label"],value=True)
    
    # Button to save attendance data
    if st.button("Save Attendance"):
        date = datetime.now().strftime('%Y-%m-%d')
        save_attendance_to_db(conn, at, date)
        st.success("Attendance data saved successfully!")
