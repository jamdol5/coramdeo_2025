import streamlit as st
import pandas as pd
from datetime import datetime
from db_utils import get_attendance_summary, get_non_attendees, get_db_connection, update_contact_status, get_contacted_students

def app():
    st.title('Attendance Summary')

    # Get the database connection from session state
    conn = st.session_state.db_connection

    # Date selection
    summary_date = st.date_input("Select date for summary", datetime.now())
    date_str = summary_date.strftime('%Y-%m-%d')

    # Display attendance summary
    with st.expander("Attendance Summary:"):
        summary = get_attendance_summary(conn, date_str)
        if summary:
            for grade, total, attended in summary:
                st.write(f"{grade}: {attended}/{total} attended")
        else:
            st.write("No attendance data for the selected date.")

    # Display non-attendees
    with st.expander("Non-Attendees Report:"):
        non_attendees = get_non_attendees(conn, date_str)
        if non_attendees:
            for grade, student in non_attendees:
                st.write(f"{grade}: {student} did not attend")
        else:
            st.write("All students attended on the selected date.")

    # Check for students who missed church 3 or more times
    with st.expander("Students who missed church 3 or more weeks:"):
        c = conn.cursor()
        c.execute('''
            SELECT student_name, COUNT(*) as missed_count
            FROM attendance
            WHERE attended = 0
            GROUP BY student_name
            HAVING missed_count >= 3
        ''')
        frequent_non_attendees = c.fetchall()

        # Fetch current contact status for each student
        c.execute('''
            SELECT student_name, MAX(contacted)
            FROM attendance
            GROUP BY student_name
        ''')
        contact_status = c.fetchall()

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
                update_contact_status(conn, student, contacted)
            st.success("Contact status saved successfully!")
            
    if st.button("Show Contacted Students"):
        st.write("Students who have been contacted:")
        contacted_students = get_contacted_students(conn)
        for student, contact_date in contacted_students:
            st.write(f"{student} was contacted on {contact_date}")
