import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import db_utils  # Import the db_utils module

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

    # Initialize the database
    db_utils.init_db()

    names_dict = {
        "10학년 남자": ["김하윤","김예준","김주안","강민주","박하람","손예랑","아현서","유승효","윤희상","장선후","한얼","홍휘성","호담"]
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
        db_utils.save_attendance_to_db(at, date)
        st.success("Attendance data saved successfully!")
