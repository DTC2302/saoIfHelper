import streamlit as st
import os
s = st.text_input("Enter UserName")
c1,c2 = st.columns(2)
with c1:
    if st.button("Create User"):
        signUp = st.Page("./Pages/SignUp.py", title="Signup")
        pg = st.navigation([signUp], position="hidden")
        pg.run()
        st.switch_page("./Pages/SignUp.py")
with c2:
    if st.button("Login"):
        if os.path.exists(f"Users/{s}.db"):

            inv = st.Page("./Pages/Inventory.py", title="Inventory")
            ser = st.Page("./Pages/Search.py", title="Search")
            pg = st.navigation([inv,ser])
            
            with open(f"/Users/cur.txt", 'w') as f:
                f.write(s)
            st.switch_page("./Pages/Inventory.py")
        else:
            st.write("Invalid UserName")