import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import sqlite3
import db_utils  # Assuming db_utils contains all the database functions

def app():
    st.title("코람데오 출석부")

    # Initialize the database (in case it hasn't been done)
    db_utils.init_db()

    # Date input for selecting the date
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now().date()
    
    selected_date = st.date_input("Select Date", value=st.session_state.selected_date)
    st.session_state.selected_date = selected_date
    date_str = selected_date.strftime('%Y-%m-%d')

    # Analytics    
    with st.expander("Attendance Summary:"):
        summary = db_utils.get_attendance_summary(date_str)
        for grade, total, attended in summary:
            st.write(f"{grade}: {attended}/{total} attended")

    # Report for students who did not attend
    
    
    with st.expander("Non-Attendees Report:"):
        non_attendees = db_utils.get_non_attendees(date_str)
        if non_attendees:
            for grade, student in non_attendees:
                st.write(f"{grade}: {student} did not attend")
        # else:
        #     st.write("All students attended")

    # if st.button("Contact Lists"):
    with st.expander("Students who missed church 3 or more weeks:"):
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute('''
            SELECT student_name, COUNT(*) as missed_count
            FROM attendance
            WHERE attended = 0
            GROUP BY student_name
            HAVING missed_count >= 2
        ''')
        frequent_non_attendees = c.fetchall()

        # Fetch current contact status for each student
        c.execute('''
            SELECT student_name, MAX(contacted)
            FROM attendance
            GROUP BY student_name
        ''')
        contact_status = c.fetchall()
        conn.close()

        contact_status_dict = {student: status for student, status in contact_status}
   
        for student, count in frequent_non_attendees:
            st.write(f"{student}: missed {count} weeks")
            checkbox_key = f"contact_{student}"

            # Use session state to persist the checkbox states
            if 'contacted_status' not in st.session_state:
                st.session_state.contacted_status = contact_status_dict

            initial_contacted = st.session_state.contacted_status.get(student, 0) == 1
            contacted = st.checkbox(f"Contacted {student}", value=initial_contacted, key=checkbox_key)
            
            # Update the contact status in the session state only
            st.session_state.contacted_status[student] = 1 if contacted else 0

        if st.button("Save Contact Status"):
            for student, contacted in st.session_state.contacted_status.items():
                db_utils.update_contact_status(student, contacted)
            st.success("Contact status saved successfully!")
            
    if st.button("Show Contacted Students"):
        st.write("Students who have been contacted:")
        contacted_students = db_utils.get_contacted_students()
        for student, contact_date in contacted_students:
            st.write(f"{student} was contacted on {contact_date}")