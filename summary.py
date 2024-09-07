import streamlit as st
import pandas as pd
from datetime import datetime
from pytz import timezone
from db_utils import get_attendance_summary, get_non_attendees, get_db_connection, update_contact_status, get_contacted_students

def app():
    st.title('Attendance Summary')

    # Get the database connection from session state
    conn = st.session_state.db_connection

    # Get current date in US Pacific Time
    pacific_tz = timezone('US/Pacific')
    current_date = datetime.now(pacific_tz).date()

    # Date selection (default to current Pacific Time date)
    summary_date = st.date_input("Select date for summary", value=current_date)
    date_str = summary_date.strftime('%Y-%m-%d')

    # Rest of your code remains the same
    # ...

    with st.expander("Attendance Summary:"):
        summary = get_attendance_summary(conn, date_str)
        if summary:
            for grade, total, attended in summary:
                st.write(f"{grade}: {attended}/{total} attended")
        else:
            st.write("No attendance data for the selected date.")

    # ... (rest of your existing code)

    # When saving contact status, use Pacific Time
    if st.button("Save Contact Status"):
        current_datetime = datetime.now(pacific_tz)
        for student, contacted in st.session_state.contacted_status.items():
            update_contact_status(conn, student, contacted, current_datetime)
        st.success("Contact status saved successfully!")
            
    if st.button("Show Contacted Students"):
        st.write("Students who have been contacted:")
        contacted_students = get_contacted_students(conn)
        for student, contact_date in contacted_students:
            # Convert contact_date to Pacific Time for display
            if contact_date:
                contact_date = timezone('UTC').localize(datetime.strptime(contact_date, '%Y-%m-%d %H:%M:%S')).astimezone(pacific_tz)
                st.write(f"{student} was contacted on {contact_date.strftime('%Y-%m-%d %I:%M %p %Z')}")
            else:
                st.write(f"{student} has not been contacted")
