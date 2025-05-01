import sqlite3
con = sqlite3.connect("saoifHelper.db")
cur = con.cursor()

name = "Little Nepenthes"
floor = 1
minLvl = 4
maxLevel = 4
minHp = 882
maxHp = 882
minDef = 9
maxDef = 9
regSpawns = ["Rivalry Planes"]
if (not cur.execute(f"Select * from Enemy Where name='{name}'").fetchall()):
    cur.execute(f"Insert into Enemy Values('{name}',{minLvl},{maxLevel},{minHp},{maxHp},{minDef},{maxDef})")
for i in regSpawns:
    if (not cur.execute(f"Select * from Area Where name='{i}'").fetchall()):
        cur.execute(f"Insert into Area Values('{i}',{floor})")
    if (not cur.execute(f"select * from Spawns where Enemy='{name}' and AName = '{i}'").fetchall()):
        cur.execute(f"Insert into Spawns Values('{name}', '{i}')")
con.commit()