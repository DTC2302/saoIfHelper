import streamlit as st
import sqlite3
import os

def inc(item):
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    if (not cur.execute(f"Select * from Inventory Where Item='{item}'").fetchone()):
        cur.execute(f"Insert into Inventory values('{item}', 1)")
        con.commit()
    else:
        cur.execute(f"Update Inventory Set Qty = {cur.execute("Select Qty from Inventory Where Item='%s'" %item).fetchone()[0]+1} where Item='{item}'")
        con.commit()

def dec(item):
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    cur.execute(f"Update Inventory Set Qty = {cur.execute("Select Qty from Inventory Where Item='%s'" %item).fetchone()[0]-1} where Item='{item}'")
    if (cur.execute(f"Select Qty from Inventory Where item='{item}';").fetchone()[0])<1:
        cur.execute(f"Delete from Inventory Where item='{item}'")
    con.commit()

def filter():
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    with st.popover("Filter"):
        craftFilter = st.checkbox("Craftable")
        isEquipment = st.checkbox("Equipment")
        if (isEquipment):
            levelFilter = st.checkbox("Levels")
            if levelFilter:
                minLevel, maxLevel = st.select_slider("Min and Max Level", [i for i in range(1,101)], value=(1,100))
        isMaterial = st.checkbox("Material")
    i =lambda item:(craftFilter and not craftable(item)) or (isEquipment and not cur.execute(f"select * from Equipment Where name='{item}'").fetchall()) or (isEquipment and levelFilter and not minLevel<=cur.execute(f"Select LevelReq from Equipment Where name='{item}'").fetchone()[0]<=maxLevel) or (isMaterial and not cur.execute(f"Select Rname from Materials Where Name='{item}'").fetchall())
    return i

def craftable(item):
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    a = set(cur.execute(f"Select * from Materials Where Rname='{item}'").fetchall())
    if (not a):
        return False
    for i in a:
        if (not cur.execute(f"Select * from Inventory Where Item='{i[0]}'").fetchall() or cur.execute(f"Select Qty from Inventory Where Item='{i[0]}'").fetchone()[0]<i[1]):
            return False
    return True

def craft(item):
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    cur.execute(f"Select * from Materials Where Rname='{item}'")
    a = cur.fetchall()

    for i in (a):
        for z in range(1,i[1]+1):
            dec(i[0])
    inc(item)