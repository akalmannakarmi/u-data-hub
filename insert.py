import sqlite3
import json
from data import dbUser,dbAdmin,dbBasic
from data.data import dataTypes
from appBasic.encrypt import hash_password

conn = sqlite3.connect('instance/user.db')

# Creating categories and Field
structure = {}
with open("insert/structure.json","r",encoding='utf-8') as f:
    structure = json.load(f)

for category, fields in structure.items():
    try:
        dbAdmin.addCategory(category)
    except Exception as e:
        print(f"Failed to Add Category:{category} Error:{e}")
        pass
    for field,dataType in fields.items():
        try:
            dbAdmin.addField(category,field,dataTypes[dataType],0)
        except Exception as e:
            print(f"Failed to Add Field:{field} Error:{e}")
            pass

userData = {}
with open("insert/data.json","r",encoding='utf-8') as f:
    userData = json.load(f)

for user,data in userData.items():
    cur= conn.cursor()
    try:
        cur.execute("INSERT INTO User (username,password,is_active) VALUES (?,?,?)",(user,hash_password(user),1))
        conn.commit()
    except Exception as e:
        print(f"Failed to add user:{user} Error:{e}")
        pass
    cur.execute("SELECT id FROM User WHERE username = ?",(user,))
    id_ = cur.fetchone()[0]
    cur.close()

    try:
        dbBasic.addUser(id_,user)
    except Exception as e:
        print(f"Failed to add User to data:{id_},{user} = {type(id_)},{type(user)}")
        pass

    for category,fieldData in data.items():
        fieldPrivacy = {k:0 for k in fieldData}
        try:
            dbUser.saveInfo(id_,category,fieldData,fieldPrivacy)
        except Exception as e:
            print(f"Failed to add user data Error:{e}")
            pass


conn.close()