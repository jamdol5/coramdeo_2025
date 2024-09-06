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
    # df = pd.read_excel(r'/Users/hyungju/Documents/Coding/Langchain/2024-2025 연락처.xlsx',sheet_name='Small Group_스몰그룹')

    # Define the names directly in a dictionary
    names_dict = {
        "6학년 남자": ["권예준","김지훈","박시후","신준민","정라온"]
    }
    
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

