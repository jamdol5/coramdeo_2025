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

    # Define the names directly in a dictionary
    # df = pd.read_excel(r'/Users/hyungju/Documents/Coding/Langchain/2024-2025 연락처.xlsx',sheet_name='Small Group_스몰그룹')

    names_dict = {
        "6학년 여자": ["지윤","강재인","김예나","김윤","김하늘","박서연","손효진","이다인"
        ,"이지안","전지안","정세연","최주아","한유라"]
    }

    # ############# Cleaning dataframe ####################
    # #Setting up a new header
    # new_header = df.iloc[0]
    # df.columns = new_header 

    # # Drop the first four rows (rows 0 to 3)
    # df = df.drop([0, 1, 2])

    # # Keep only the first 15 columns
    # df = df.iloc[:, :15]

    # # Keep only rows up to the 24th row (since the index starts at 0, row 24 is at index 23)
    # df = df.iloc[:18]

    # # Reset the index
    # df = df.reset_index(drop=True)
    # ####################################################

    #Upload values from dataframe
    ####################################################
##############################################################
    # Create the Roster dictionary dynamically
    Roster = {grade: [{"label": name, "default":False} for name in names] for grade, names in names_dict.items()}

    # # Select the columns with headers
    # seven_g1_values = df['7학년 남자'].dropna().tolist()
    # # seven_g2_values = df['7학년여자 #2'].dropna().tolist()
    # # seven_b_values = df['7학년 남자'].dropna().tolist()

    # # Create the Roster dictionary dynamically
    # Roster = {
    #     "6학년 남자": [{"label": value, "default": False} for value in seven_g1_values],
    #     # "7학년 여자 #2": [{"label": value, "default": False} for value in seven_g2_values],
    #     # "7학년 남자": [{"label": value, "default": False} for value in seven_b_values]
    # }

    # Initialize attendance tracking
    at = {grade: {} for grade in names_dict.keys()}

    # Create a Streamlit expander and display the values
    st.title('Student Roster')

    # Example           
    # Second row with a single column
    # col3 = st.columns([2])
    # with col3[0]:
    #     with st.expander("6학년 남자"):
    #         for item in Roster["6학년 남자"]:
    #             at["6학년 남자"][item["label"]] = st.checkbox(item["label"], key=item["label"], value=True)

    for grade, students in Roster.items():
        with st.expander(grade):
            for student in students:
                at[grade][student["label"]] = st.checkbox(student["label"], key=student["label"],value=True)
    

     # Button to save attendance data
    if st.button("Save Attendance"):
        date = datetime.now().strftime('%Y-%m-%d')
        db_utils.save_attendance_to_db(at, date)
        st.success("Attendance data saved successfully!")
