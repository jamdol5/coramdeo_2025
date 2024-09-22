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
        "9학년 여자": ["박정현","김지아","박지효","박지빈","박서현","박예림","성다애","이민주","최윤지"]
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
        # Get the current date and time in PST
        from datetime import datetime
        from pytz import timezone

        pst = timezone('US/Pacific')
        date = datetime.now(pst).strftime('%Y-%m-%d')
        
        save_attendance_to_db(conn, at, date)
        st.success(f"Attendance data saved successfully for {date} (PST)!")
