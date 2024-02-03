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

    def getDataTypes():
        return db.dataTypes

    def getCategories():
        return db.categories
    
    def getCategoriesAndFields():
        return db.categoriesAndFields
    
    def getrevCategoryAndField():
        return db.revCategoryAndField
    
    def validAuth(apiKey):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE apiKey=?",(apiKey,))
            if cursor.fetchall():
                return True
            return False
    
    def getStats(apiKey,fields):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Shared.dataId FROM User JOIN Shared ON User.id = Shared.userId WHERE User.apiKey = ?",(apiKey,))
            dataIds=cursor.fetchall()
            dataIds=[id[0] for id in dataIds]
            cursor.execute("SELECT fieldId, value FROM Data WHERE fieldId IN ? AND (isPrivate !=1 OR id IN ?)", (tuple(fields),dataIds))
            result = cursor.fetchall()
            return result
    
    def getUserInfo(userId,apiKey,fields):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Shared.dataId FROM User JOIN Shared ON User.id = Shared.userId WHERE User.apiKey = ?",(apiKey,))
            dataIds=cursor.fetchall()
            dataIds=[id[0] for id in dataIds]
            cursor.execute("""SELECT fieldId,value FROM Data WHERE
                userId=? AND fieldId in ? AND (isPrivate NOT IN (1,2) OR id IN ?)""", (userId,tuple(fields),dataIds))
            result = cursor.fetchall()
            return result