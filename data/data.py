from threading import Lock
import sqlite3

class Conn(sqlite3.Connection):
    def __exit__(self, __type, __value, __traceback):
        ConnPool.release(self)
        return super().__exit__(__type, __value, __traceback)

class ConnPool:
    _pool=[]
    _lock=Lock()

    def getConn():
        with ConnPool._lock:
            if not ConnPool._pool:
                # print("new conn")
                return Conn(db.name,check_same_thread=False)
            else:
                # print("reuse conn")
                return ConnPool._pool.pop()
    
    def release(conn:Conn):
        with ConnPool._lock:
            ConnPool._pool.append(conn)

class db:
    name="example.db"
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
        with ConnPool.getConn() as conn:
            db.createTables(conn)
            db.loadData(conn)

    def loadData(conn:sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("SELECT id,name FROM Category")
        result=cursor.fetchall()
        for (id,name) in result:
            db.categories[name]=id
        cursor.execute("SELECT Field.id, Category.name AS category_name, Field.name, Field.dataTypeId FROM Field JOIN Category ON Field.categoryId = Category.id")
        result=cursor.fetchall()
        for (id,category,name,dataTypeId) in result:
            if category not in db.categoriesAndFields:
                db.categoriesAndFields[category]={}
            db.categoriesAndFields[category][name]=id
            db.revCategoryAndField[id]=(category,name,dataTypeId)
        cursor.close()

    def createTables(conn:sqlite3.Connection):
        cursor = conn.cursor()
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
        conn.commit()
        cursor.close()


import struct

def convertValue(fieldId,raw:bytes):
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