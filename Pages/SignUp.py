import streamlit as st
import os
from BackEnd.dbCreator import Create

if st.button("Return to Login"):
    st.switch_page("Pages/LogIN.py")
s = st.text_input("Enter UserName")
if st.button("SignUp"):
    if len(s) and os.path.exists(f"Users/{s}.db"):
        st.write("UserName Taken")
    else:
        st.query_params['db'] = f"{s}.db"
        Create()
        st.switch_page("Pages/LogIN.py")
