import streamlit as st
import os



if (__name__ == "__main__"):
    log = st.Page("Pages/LogIN.py")
    signUp = st.Page("Pages/SignUp.py", title="SignUp")
    Inventory = st.Page("Pages/Inventory.py", title="Inventory")
    Search = st.Page("Pages/Search.py", title="Search")
    pg = st.navigation([log,signUp,Inventory,Search], position="hidden")

    pg.run()