import streamlit as st
import pandas as pd
from datetime import datetime
from db_utils import get_attendance_summary, get_non_attendees

def app():
    st.title('Attendance Summary')

    # Get the database connection from session state
    conn = st.session_state.db_connection

    # Date selection
    summary_date = st.date_input("Select date for summary", datetime.now())

    # Display attendance summary
    st.subheader("Attendance Summary")
    summary = get_attendance_summary(conn, summary_date.strftime('%Y-%m-%d'))
    if summary:
        summary_df = pd.DataFrame(summary, columns=['Grade', 'Total Students', 'Attended'])
        st.table(summary_df)
    else:
        st.write("No attendance data for the selected date.")

    # Display non-attendees
    st.subheader("Non-Attendees")
    non_attendees = get_non_attendees(conn, summary_date.strftime('%Y-%m-%d'))
    if non_attendees:
        non_attendees_df = pd.DataFrame(non_attendees, columns=['Grade', 'Student Name'])
        st.table(non_attendees_df)
    else:
        st.write("All students attended on the selected date.")

    # You can add more summary statistics or visualizations here
    # For example, you could show attendance trends over time, or attendance rates by grade
