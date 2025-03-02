# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
import time
from db_utils import get_db_connection
from page6 import app as page6_app
from page6_3 import app as page6_3_app
from page7 import app as page7_app
from page7_2 import app as page7_2_app
from page7_3 import app as page7_3_app
from page7_4 import app as page7_4_app
from page8_2 import app as page8_2_app
from page8_3 import app as page8_3_app
from page8_4 import app as page8_4_app
from page9_1 import app as page9_1_app
from page9_2 import app as page9_2_app
from page9_3 import app as page9_3_app
from page10 import app as page10_app
from page10_2 import app as page10_2_app
from page11_2 import app as page11_2_app
from page11_3 import app as page11_3_app
from page12 import app as page12_app
from page12_2 import app as page12_2_app
from summary import app as summary_app
# from page7 import app as page7_app
# from streamlit_pandas_profiling import st_profile_report

# Add this at the beginning of the file
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] == st.secrets.get("username")
            and st.session_state["password"] == st.secrets.get("password")
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct
        return True

PAGES = {
    "시은쌤": page6_app,
    "배니쌤": page6_3_app,
    "영민쌤": page7_app,
    "서지선쌤": page7_2_app,
    "승환쌤": page7_3_app,
    "준희쌤": page7_4_app,
    "희주쌤": page8_3_app,
    "예은쌤": page8_4_app,
    "재원쌤/태림쌤": page8_2_app,
    "수진쌤": page9_3_app,
    "병규쌤": page9_1_app,
    "우진쌤": page9_2_app,
    "진희쌤": page10_app,
    "태욱쌤/형준쌤": page10_2_app,
    "주연쌤": page11_3_app,
    "도현쌤/예닮쌤": page11_2_app,
    "원쌤": page12_app,
    "정훈쌤/현건쌤": page12_2_app,
    "이번주 출석부": summary_app
}

# Modify the main function
def main():
    st.sidebar.title('코람데오 선생님들의 공간')
    
    if check_password():
        # Initialize database connection
        if 'db_connection' not in st.session_state:
            st.session_state.db_connection = get_db_connection()
        
        selection = st.sidebar.radio("메뉴 선택", list(PAGES.keys()))
        page_function = PAGES[selection]
        page_function()
    else:
        st.stop()

if __name__ == "__main__":
    main()

# llm.invoke(

# )





