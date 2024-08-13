# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
import time
# import ollama
from b_verse import app as b_verse_app
from b_study import app as b_study_app
from page6 import app as page6_app
from page6_2 import app as page6_2_app
from page6_3 import app as page6_3_app
from page7 import app as page7_app
from page7_2 import app as page7_2_app
from page7_3 import app as page7_3_app
from page7_4 import app as page7_4_app
from page8 import app as page8_app
from page8_2 import app as page8_2_app
from page8_3 import app as page8_3_app
from page8_4 import app as page8_4_app
from page9 import app as page9_app
from page9_2 import app as page9_2_app
from page9_3 import app as page9_3_app
from page10 import app as page10_app
from page10_2 import app as page10_2_app
from page10_3 import app as page10_3_app
from page11 import app as page11_app
from page11_2 import app as page11_2_app
from page11_3 import app as page11_3_app
from page12 import app as page12_app
from page12_2 import app as page12_2_app
from summary import app as summary_app
# from page7 import app as page7_app
# from streamlit_pandas_profiling import st_profile_report

PAGES = {
    "오늘의 성경구절": b_verse_app,
    "주일 스몰그룹": b_study_app,
    "시은쌤": page6_app,
    "예림쌤": page6_2_app,
    "병규쌤/배니쌤": page6_3_app,
    "영민쌤": page7_app,
    "수진쌤": page7_2_app,
    "준희쌤": page7_3_app,
    "야곱쌤": page7_4_app,
    "태림쌤": page8_app,
    "재원쌤": page8_2_app,
    "태은쌤": page8_3_app,
    "희주쌤": page8_4_app,
    "비건쌤": page9_app,
    "승환쌤": page9_2_app,
    "지선쌤": page9_3_app,
    "진희쌤": page10_app,
    "형준쌤": page10_2_app,
    "태욱쌤": page10_3_app,
    "예닮쌤": page11_app,
    "도현쌤": page11_2_app,
    "주연쌤": page11_3_app,
    "원쌤": page12_app,
    "정훈쌤/현건쌤": page12_2_app,
    "이번주 출석부": summary_app
}

def main():
    st.sidebar.title('코람데오 선생님들의 공간')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    
    page_function = PAGES[selection]
    page_function()  # Call the app function which we'll define in each module

if __name__ == "__main__":
    main()

# llm.invoke(

# )





