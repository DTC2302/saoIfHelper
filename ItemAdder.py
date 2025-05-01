import sqlite3

con = sqlite3.connect("saoifHelper.db")
cur = con.cursor()
name = "Small Metal Piece"
Type = "Material"
Equiptype = ""
EnhanceType = ""
LevelReq = -1
minAtk = -1
minDef = -1
maxAtk = -1
maxDef = -1
xpVal = -1
materials = []
dropsFrom = ['Kobold Henchman']

if (cur.execute(f"Select * from items Where name='{name}'").fetchall()):
    cur.execute(f"Delete from items where name='{name}'")    
cur.execute(f"Insert into items values('{name}', '{Type}')")

if (Type == "Equipment"):
    if (cur.execute(f"Select * from Equipment Where name='{name}'").fetchall()):
        cur.execute(f"Delete from Equipment where name='{name}'")
    cur.execute(f"Insert into Equipment values('{name}', {LevelReq}, '{Equiptype}')")
    if (Equiptype in ["Chest", "Leggings"]):
        if (cur.execute(f"Select * from Armor Where name='{name}'").fetchall()):
            cur.execute(f"Delete from Armor where name='{name}'")
        cur.execute(f"Insert into Armor values('{name}', {minDef}, {maxDef})")
    else:
        if (cur.execute(f"Select * from Weapon Where name='{name}'").fetchall()):
            cur.execute(f"Delete from Weapon where name='{name}'")
        cur.execute(f"Insert into Weapon values('{name}', {minAtk}, {maxAtk})")

if (materials):
    if (cur.execute(f"Select * from Recipe Where name='{name}'").fetchall()):
        cur.execute(f"Delete from Recipe where name='{name}'")
    cur.execute(f"Insert into Recipe values('{name}', '{len(materials)+1}')")
    for i in range(1,len(materials)+1):
        if (not cur.execute(f"Select * from Items Where name='{materials[i-1][0]}'").fetchall()):
            cur.execute(f"Insert into Items values('{materials[i-1][0]}', 'Material')")
        if (cur.execute(f"Select * from Materials Where name='{materials[i-1][0]}' and Rname='{name}'").fetchall()):
            cur.execute(f"Delete from Materials where name='{materials[i-1][0]}' and Rname='{name}'")
        cur.execute(f"Insert into Materials values('{materials[i-1][0]}', {materials[i-1][1]}, {i}, '{name}')")

if (len(dropsFrom)):
    for i in dropsFrom:
        if (cur.execute(f"Select * from Drops Where Item='{name}' and Enemy='{i}'").fetchall()):
            cur.execute(f"Delete from Drops where name='{name}' and Enemy='{i}'")
        cur.execute(f"Insert into Drops Values('{name}', '{i}')")

con.commit()
