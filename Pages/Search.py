from BackEnd.Functions import filter
from BackEnd.PopUp import popUp
import streamlit as st
import sqlite3
import os

with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
    db = f.readline()
con = sqlite3.connect(f"Users/{db}.db")
cur = con.cursor()
c1, c2 = st.columns([1,4],gap="small")
with c1:
    if st.button("Goto Inventory"):
        st.switch_page("./Pages/Inventory.py")
with c2:
    x = filter()
s = st.text_input("Item")
i = 0
m = 3
rows = st.columns(m)
names = [z[0] for z in cur.execute(f"Select Name from Items").fetchall() if (z[0][:len(s)]).upper()==s.upper()]
for item in names:
    if x(item):
        continue
    with rows[i]:
        popUp(item)
    i+=1
    i%=3