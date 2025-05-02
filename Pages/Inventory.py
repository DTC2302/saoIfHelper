
import streamlit as st
import sqlite3
from BackEnd.Functions import dec, inc, filter
from BackEnd.PopUp import popUp
import os

global ButtonId
ButtonId = 0
with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
    db = f.readline()
con = sqlite3.connect(f"Users/{db}.db")
cur = con.cursor()

items = cur.execute("Select * from Inventory").fetchall()

if st.button("Goto Search"):
    st.switch_page("./Pages/Search.py")
st.title("Inventory")
for i in (items):
    #if x(i):
    #    continue
    with st.container():
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            item = i[0]
            popUp(item)    
        with c2:
                st.header(f"{i[1]}x")
        with c3:
            ButtonId+=1
            if (st.button("Inc", f"Inc{item}{ButtonId}")):
                inc(i[0])
                st.rerun()
        with c4:
            ButtonId+=1
            if (st.button("Dec", f"{i[0]}dec{ButtonId}")):
                dec(i[0])
                st.rerun()
        with c5:
            ButtonId+=1
            if (st.button("Delete", f"Del{item}{ButtonId}")):
                cur.execute(f"Delete from Inventory Where item='{i[0]}'")
                con.commit()
                st.rerun()
