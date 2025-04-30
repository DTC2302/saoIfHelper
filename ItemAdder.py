import sqlite3

con = sqlite3.connect("saoifHelper.db")
cur = con.cursor()
name = "Bronze Sword"
Type = "Equipment"
Equiptype = "Sword"
EnhanceType = ""
LevelReq = 1
minAtk = 65
minDef = -1
maxAtk = 139
maxDef = -1
xpVal = -1
materials = [("Coarse Stone", 1), ("Boar Hide", 1)]


cur.execute(f"Delete from Items Where name='{"board hide"}'")
if (not cur.execute(f"Select * from items Where name='{name}'").fetchall()):
    cur.execute(f"Insert into items values('{name}', '{Type}')")
if (Type == "Equipment"):
    if (not cur.execute(f"Select * from Equipment Where name='{name}'").fetchall()):
        cur.execute(f"Insert into Equipment values('{name}', {LevelReq}, '{Equiptype}')")
    if (Equiptype in ["Head", "Chest", "Leggings"]):
        print(-1)
    else:
        if (not cur.execute(f"Select * from Weapon Where name='{name}'").fetchall()):
            cur.execute(f"Insert into Weapon values('{name}', {minAtk}, {maxAtk})")

if (materials):
    if (not cur.execute(f"Select * from Recipe Where name='{name}'").fetchall()):
        cur.execute(f"Insert into Recipe values('{name}', '{len(materials)+1}')")
    for i in range(1,len(materials)+1):
        if (not cur.execute(f"Select * from Items Where name='{materials[i-1][0]}'").fetchall()):
            cur.execute(f"Insert into items values('{materials[i-1][0]}', 'Material')")
        cur.execute(f"Insert into Materials values('{materials[i-1][0]}', {materials[i-1][1]}, {i}, '{name}')")

con.commit()