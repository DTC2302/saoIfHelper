import streamlit as st
import sqlite3
from BackEnd.Functions import craft, craftable
import os
global ButtonId
ButtonId = 0

def popUp(item):
    with open(f"{os.path.dirname(__file__)}\\..\\Users\\cur.txt", 'r') as f:
        db = f.readline()
    con = sqlite3.connect(f"Users/{db}.db")
    cur = con.cursor()
    with st.popover(item):
        global ButtonId
        ButtonId+=1
        if (not cur.execute(f"Select * from Inventory Where item='{item}'").fetchone()):
            if st.button("Add to Inventory", f"addSearch{item}"):
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
                if (eType not in ["Chest","Leggings"]):
                    cur.execute("Select * from Weapon where name = '%s'" % item)
                    weapon = cur.fetchone()
                    st.write("Min Atk: %s" % (weapon[1]))
                    st.write("Max Atk: %s" % (weapon[2]))
                else:
                    cur.execute("Select * from Armor where name = '%s'" % item)
                    Armor = cur.fetchone()
                    st.write("Min Def: %s" % (Armor[1]))
                    st.write("Max Def: %s" % (Armor[2]))
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
                    if (st.button("Craft", f"Craft{item}")):
                        craft(item)
                        st.rerun()
            usedIn = cur.execute(f"Select Rname from Materials Where Name='{item}'").fetchall()
            if (usedIn):
                st.header("Used In")
                for recipe in usedIn:
                    with st.container():
                        r, n, c = st.columns(3)
                        with r:
                            st.write(recipe[0])
                        with n:
                            st.write(cur.execute(f"Select Qty from Materials where (Rname='{recipe[0]}' and Name='{item}')").fetchone()[0])
                        with c:
                            if (craftable(recipe[0])):
                                if st.button("Craft", f"craft{recipe[0]}UsedIn{item}"):
                                    craft(recipe[0])
            DropsFrom = cur.execute(f"Select Enemy from Drops Where Item='{item}'").fetchall()
            
            if (DropsFrom):
                st.header("Drops From")
                for e in DropsFrom:
                    with st.container():
                        eName, Earea = st.columns(2)
                        with eName:
                            st.write(e[0])
                        with Earea:
                            area = cur.execute(f"Select Aname from Spawns Where Enemy='{e[0]}'").fetchone()[0]
                            floor = cur.execute(f"Select FloorNum from Area Where Name='{area}'").fetchone()[0]
                            st.write(f"Spawns in {area} on floor {floor}")
                        
