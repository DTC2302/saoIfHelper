import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os

global ButtonId
ButtonId = 0

def inc(item):
    if (not cur.execute(f"Select * from Inventory Where Item='{item}'").fetchone()):
        cur.execute(f"Insert into Inventory values('{item}', 1)")
        con.commit()
    else:
        cur.execute(f"Update Inventory Set Qty = {cur.execute("Select Qty from Inventory Where Item='%s'" %item).fetchone()[0]+1} where Item='{item}'")
        con.commit()

def dec(item):
    cur.execute(f"Update Inventory Set Qty = {cur.execute("Select Qty from Inventory Where Item='%s'" %item).fetchone()[0]-1} where Item='{item}'")
    if (cur.execute(f"Select Qty from Inventory Where item='{item}';").fetchone()[0])<1:
        cur.execute(f"Delete from Inventory Where item='{item}'")
    con.commit()

def craftable(item):
    for i in set(cur.execute(f"Select * from Materials Where Rname='{item}'").fetchall()):
        if (not cur.execute(f"Select * from Inventory Where Item='{i[0]}'").fetchall() or cur.execute(f"Select Qty from Inventory Where Item='{i[0]}'").fetchone()[0]<i[1]):
            return False
    return True

def craft(item):
    cur.execute(f"Select * from Materials Where Rname='{item}'")
    a = cur.fetchall()

    for i in (a):
        for z in range(1,i[1]+1):
            dec(i[0])
    inc(item)


def popUp(item):
    with st.popover(item):
        global ButtonId
        ButtonId+=1
        if (not cur.execute(f"Select * from Inventory Where item='{item}'").fetchone()):
            if st.button("Add to Inventory", f"addSearch{item}{ButtonId}"):
                cur.execute(f"Insert into Inventory values('{item}', 1)")
                con.commit()
                st.rerun()
        st.header("Details")
        a = cur.execute(f"Select * from items where name = '{item}'").fetchone()
        if (a):     
            type = a[1]
            st.write("Type: %s" % type)
            if (type.lower() == "equipment"):
                cur.execute("Select * from Equipment where name = '%s'" % item)
                vals = cur.fetchone()
                eType = vals[2]
                st.write("Level Req: %s" % (vals)[1])
                if (eType not in ["Helm","Chest","Leggings"]):
                    cur.execute("Select * from Weapon where name = '%s'" % item)
                    weapon = cur.fetchone()
                    st.write("Min Atk: %s" % (weapon[1]))
                    st.write("Max Atk: %s" % (weapon[2]))
                else:
                    cur.execute("Select * from Armor where name = '%s'" % item)
                    Armor = cur.fetchone()
                    st.write("Min Atk: %s" % (Armor[1]))
                    st.write("Max Atk: %s" % (Armor[2]))
            elif(type.lower() == "enhancement"):
                en = cur.execute(f"Select * from Enhancement Where Name='{item}'").fetchone()
                st.write(f"Enhancement Type: {en[2]}")
                st.write(f"xpVal: {en[1]}")
            recipes = cur.execute(f"Select * from Recipe Where Name='{item}'").fetchone()
            if (recipes):
                st.header("Recipe")
                for i in set(cur.execute(f"Select * from Materials Where Rname='{item}'").fetchall()):
                    with st.container():
                        c1,c2 = st.columns(2)
                        with c1:
                            st.write(i[0])
                        with c2:
                            st.write(i[1])
                if (craftable(item)):
                    ButtonId+=1
                    if (st.button("Craft", ButtonId)):
                        craft(item)
                        st.rerun()

def Inventory():
    items = cur.execute("Select * from Inventory").fetchall()    
    for i in (items):
        with st.container():
            c1,c2,c3,c4,c5 = st.columns(5)
            with c1:
                item = i[0]
                popUp(item)    
            with c2:
                    st.header(f"{i[1]}x")
            with c3:
                global ButtonId
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
            


def search():
    s = st.text_input("Item")
    i = 0
    m = 3
    rows = st.columns(m)
    names = [z[0] for z in cur.execute(f"Select Name from Items").fetchall() if (z[0][:len(s)]).upper()==s.upper()]
    for item in names:
        with rows[i]:
            popUp(item)
        i+=1
        i%=3


con = sqlite3.connect("saoifHelper.db")
cur = con.cursor()

inv = st.Page(Inventory, title="Inventory")
ser = st.Page(search, title="Search")
pg = st.navigation([inv,ser])
pg.run()
