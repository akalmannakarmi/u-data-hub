import sqlite3

class db:
    __conn = sqlite3.connect('example.db')
    dataTypes={
        1:"integer",
        2:"float",
        3:"bool",
        4:"string"
    }
    categories={}
    categoriesAndFields={}
    revCategoryAndField={}

    def init():
        db.createTables()
        db.loadData()

    def loadData():
        cursor = db.__conn.cursor()
        cursor.execute("SELECT id,name FROM Category")
        result=cursor.fetchall()
        for (id,name) in result:
            db.categories[name]=id
        cursor.execute("SELECT Field.id, Category.name AS category_name, Field.name, Field.dataTypeId FROM Field JOIN Category ON Field.categoryId = Category.id")
        result=cursor.fetchall()
        for (id,category,name,dataTypeId) in result:
            if not isinstance(db.categoriesAndFields[category],dict):
                db.categoriesAndFields[category]={}
            db.categoriesAndFields[category][name]=id
            db.revCategoryAndField[id]=(category,name,dataTypeId)

    def createTables():
        cursor = db.__conn.cursor()
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Category(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS Field(
            id INTEGER PRIMARY KEY,
            categoryId INTEGER,
            name TEXT,
            dataTypeId INTEGER,
            UNIQUE (categoryId, name),
            FOREIGN KEY (categoryId) REFERENCES Category(id)
        );

        CREATE TABLE IF NOT EXISTS Data(
            userId INTEGER,
            fieldId INTEGER,
            value BLOB,
            isPrivate INTEGER,
            PRIMARY KEY (userId, fieldId),
            FOREIGN KEY (fieldId) REFERENCES Field(id)
        );

        CREATE INDEX IF NOT EXISTS idx_Data_user
        ON Data (userId);
        CREATE INDEX IF NOT EXISTS idx_Data_field
        ON Data (fieldId);
        ''')
        db.__conn.commit()
        cursor.close()

    def addCategory(category):
        cursor = db.__conn.cursor()
        cursor.execute("INSERT INTO Category (name) VALUES (?)",(category,))
        db.__conn.commit()

        cursor.execute("SELECT id FROM Category WHERE name=?",(category,))
        result=cursor.fetchone()
        db.categories[category]=result[0]

        cursor.close()

    def removeCategory(category):
        cursor = db.__conn.cursor()
        cursor.execute("DELETE FROM Category WHERE name=?",(category,))
        db.__conn.commit()

        db.categories.pop(category,0)
        db.categoriesAndFields.pop(category,0)
        for id,(cat,field) in db.revCategoryAndField.copy().items():
            if cat==category:
                db.revCategoryAndField.pop(id,0)

        cursor.close()

    def addField(category,field,dataTypeId):
        cursor = db.__conn.cursor()
        if category not in db.categories:
            raise Exception("Category does not exists")
        categoryId = db.categories[category]
        cursor.execute("INSERT INTO Field (categoryId,name,dataTypeId) VALUES (?,?,?)",(categoryId,field,dataTypeId))
        db.__conn.commit()

        cursor.execute("SELECT id FROM Field WHERE categoryId=? AND name=?",(categoryId,field))
        result = cursor.fetchone()
        db.categoriesAndFields[category][field]=result[0]
        db.revCategoryAndField[result[0]]=(category,field,dataTypeId)

        cursor.close()

    def removeField(fieldId):
        cursor = db.__conn.cursor()
        cursor.execute("DELETE FROM Field WHERE id=?",(fieldId,))
        db.__conn.commit()

        category,field,dataTypeId=db.revCategoryAndField[fieldId]
        db.categoriesAndFields[category].pop(field,0)
        db.revCategoryAndField.pop(fieldId,0)

        cursor.close()

    def getUserInfo(userId,authKey):
        if not authKey:
            return
        cursor = db.__conn.cursor()
        cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=?", (userId,))
        values = cursor.fetchall()
        result={}
        for fieldId,raw,isPrivate in values:
            category,field,value = convertValue(fieldId,raw)
            result[category][field]=(value,isPrivate==1)
        return result


    def getInfos(fields):
        cursor = db.__conn.cursor()
        cursor.execute("SELECT id, value FROM Data WHERE isPrivate != 1 AND id IN ?", (tuple(fields),))
        values = cursor.fetchall()
        result={}
        for fieldId,raw in values:
            category,field,value = convertValue(fieldId,raw)
            result[category][field]=value
        return result


        
    def addInfo(userId,keyvalues):
        cursor = db.__conn.cursor()
        if any(key not in db.revCategoryAndField for key in keyvalues):
            raise Exception("Category or Field does not exists")
        
        q="INSERT INTO Data (userId,fieldId,valueId,isPrivate) VALUES (?,?,?)"

        for fieldId,(value,isPrivate) in keyvalues.items():
            bvalue=toBlob(value)
            cursor.execute(q,(userId,fieldId,bvalue,isPrivate))
        
        db.__conn.commit()
        cursor.close()

    def editInfo(userId,keyvalues):
        cursor = db.__conn.cursor()
        if any(key not in db.revCategoryAndField for key in keyvalues):
            raise Exception("Category or Field does not exists")
        
        q="UPDATE Data SET value=?, isPrivate=? WHERE userId=? AND fieldId=?"

        for fieldId,(value,isPrivate) in keyvalues.items():
            bvalue=toBlob(value)
            cursor.execute(q,(bvalue,isPrivate,userId,fieldId))
        
        db.__conn.commit()
        cursor.close()
        
    
    def removeInfo(userId,keys):
        cursor = db.__conn.cursor()
        cursor.execute("DELETE FROM Data WHERE userId=? AND fieldId IN ?")
        db.__conn.commit()
        cursor.close()

import struct

def convertValue(fieldId,raw):
    cat,field,dataTypeId = db.revCategoryAndField[fieldId]
    if dataTypeId=="integer":
        return (cat,field,struct.unpack('>I', raw)[0])
    elif dataTypeId=="float":
        return (cat,field,struct.unpack('>I', raw)[0])
    elif dataTypeId=="bool":
        return (cat,field,bool(raw))
    elif dataTypeId=="string":
        return (cat,field,raw.decode('utf-8'))
    else:
        return (cat,field,raw)

def toBlob(value):
    if isinstance(value, int):
        return value.to_bytes(4, 'big')
    elif isinstance(value, float):
        return struct.pack('>f', value)
    elif isinstance(value, bool):
        return bytes([value])
    elif isinstance(value, str):
        return value.encode('utf-8')
    else:
        return value