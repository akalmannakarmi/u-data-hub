import sqlite3

class db:
    name="example.db"
    conn = sqlite3.connect('example.db')
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