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
            db.categoriesAndFields[name]={}
        cursor.execute("SELECT Field.id, Category.name AS category_name, Field.name, Field.dataTypeId, Field.defaultPrivacy FROM Field JOIN Category ON Field.categoryId = Category.id")
        result=cursor.fetchall()
        for (id,category,name,dataTypeId,defaultPrivacy) in result:
            db.categoriesAndFields[category][name]=(id,defaultPrivacy)
            db.revCategoryAndField[id]=(category,name,dataTypeId,defaultPrivacy)
        cursor.close()

    def createTables(conn:sqlite3.Connection):
        cursor = conn.cursor()
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY,
            tag TEXT UNIQUE NOT NULL,
            apiKey TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS Category(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS Field(
            id INTEGER PRIMARY KEY,
            categoryId INTEGER,
            name TEXT,
            defaultPrivacy INTEGER,
            dataTypeId INTEGER,
            UNIQUE (categoryId, name),
            FOREIGN KEY (categoryId) REFERENCES Category(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Data(
            id INTEGER PRIMARY KEY,
            userId INTEGER,
            fieldId INTEGER,
            value BLOB,
            isPrivate INTEGER,
            UNIQUE (userId, fieldId),
            FOREIGN KEY (fieldId) REFERENCES Field(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Shared(
            dataId INTEGER,
            userId INTEGER,
            PRIMARY KEY (dataId,userId),
            FOREIGN KEY (dataId) REFERENCES Data(id) ON DELETE CASCADE,
            FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_Data_user
        ON Data (userId);
        CREATE INDEX IF NOT EXISTS idx_Data_field
        ON Data (fieldId);
        CREATE INDEX IF NOT EXISTS idx_User_apiKey
        ON User (apiKey);
        
        CREATE TRIGGER IF NOT EXISTS delete_field_rows
        AFTER DELETE ON Category
        FOR EACH ROW
        BEGIN
            DELETE FROM Field WHERE categoryId = OLD.id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS delete_data_rows
        AFTER DELETE ON Field
        FOR EACH ROW
        BEGIN
            DELETE FROM Data WHERE fieldId = OLD.id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS delete_shared_rows
        AFTER DELETE ON Data
        FOR EACH ROW
        BEGIN
            DELETE FROM Shared WHERE dataId = OLD.id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS delete_shared2_rows
        AFTER DELETE ON User
        FOR EACH ROW
        BEGIN
            DELETE FROM Data WHERE userId = OLD.id;
        END;
        ''')
        conn.commit()
        cursor.close()


import struct

def convertValue(fieldId,raw:bytes):
    cat,field,dataTypeId,defaultPrivacy = db.revCategoryAndField[fieldId]
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

def toBlob(fieldId,value):
    cat,field,dataTypeId,defaultPrivacy = db.revCategoryAndField[fieldId]
    if dataTypeId=="integer":
        return value.to_bytes(4, 'big')
    elif dataTypeId=="float":
        return struct.pack('>f', value)
    elif dataTypeId=="bool":
        return bytes([value])
    elif dataTypeId=="string":
        return value.encode('utf-8')
    else:
        return value