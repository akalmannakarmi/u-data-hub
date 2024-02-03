from .data import db,ConnPool,convertValue
import secrets

class dbAPI:
    def generateKey():
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            while True:
                key= secrets.token_hex(16)
                cursor.execute("SELECT * FROM User WHERE apiKey=?",(key,))
                if not cursor.fetchall():
                    return key
        
    def changeKey(userId):
        key = dbAPI.generateKey()
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET apiKey=? WHERE id=?", (key,userId))
            conn.commit()
            cursor.close()


    def getCategoriesAndFields():
        return db.categoriesAndFields.copy()
    
    def validAuth(authKey):
        return True
    
    def getStats(fields):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, value FROM Data WHERE isPrivate != 1 AND id IN ?", (tuple(fields),))
            values = cursor.fetchall()
            cursor.close()
            result={}
            for fieldId,raw in values:
                category,field,value = convertValue(fieldId,raw)
                result[category][field]=value
            return result
    
    def getUserInfo(userId,authKey,fields):
        if not authKey:
            return
        
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=?", (userId,))
            values = cursor.fetchall()
            cursor.close()
            result={}
            for fieldId,raw,isPrivate in values:
                category,field,value = convertValue(fieldId,raw)
                result[category][field]=(value,isPrivate==1)
            return result