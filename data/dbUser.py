from .data import db,ConnPool,convertValue,toBlob
from . import dbAPI

class dbUser:
    def newKey(userId):
        dbAPI.changeKey(userId)
    
    def getCategories():
        return db.categories
    
    def getCategoriesAndFields():
        return db.categoriesAndFields
    
    def getUserId(userTag):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM User WHERE tag=?", (userTag,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
    
    def getUserTag(userId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tag FROM User WHERE id=?", (userId,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
    
    def getUserKey(userId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT apiKey FROM User WHERE id=?", (userId,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        
    def findUsers(tag):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            tag=f"%{tag}%"
            cursor.execute("SELECT tag FROM User WHERE tag LIKE ?",(tag,))
            result=cursor.fetchmany(50)
            cursor.close()
            return result
    
    def getUserData(userId,userId2):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT dataId FROM Shared WHERE userId=?",(userId2,))
            dataIds=cursor.fetchall()
            dataIds=[id[0] for id in dataIds]
            cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=? AND (isPrivate NOT IN (1,2) OR id IN ?)", (userId,dataIds))
            values = cursor.fetchall()
            cursor.close()

            result={}
            for fieldId,raw,isPrivate in values:
                category,field,value = convertValue(fieldId,raw)
                result[category][field]=(value,isPrivate)
            return result
    
    def getMyData(userId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=?", (userId,))
            values = cursor.fetchall()
            cursor.close()

            result={}
            for fieldId,raw,isPrivate in values:
                category,field,value = convertValue(fieldId,raw)
                result[fieldId]=(value,isPrivate)
            return result
    
    def addInfo(userId,category,fieldValues,fieldPrivacy):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            q="INSERT INTO Data (userId,fieldId,value,isPrivate) VALUES (?,?,?,?)"

            for field,value in fieldValues.items():
                fieldId,defaultPrivacy=db.categoriesAndFields[category][field]
                bvalue=toBlob(fieldId,value)
                privacy = fieldPrivacy[field]
                cursor.execute(q,(userId,fieldId,bvalue,privacy))
            
            conn.commit()
            cursor.close()

    def editInfo(userId,category,fieldValues,fieldPrivacy):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            
            q="UPDATE Data SET value=?, isPrivate=? WHERE userId=? AND fieldId=?"

            for field,value in fieldValues.items():
                fieldId,defaultPrivacy=db.categoriesAndFields[category][field]
                bvalue=toBlob(fieldId,value)
                privacy=fieldPrivacy[field]
                cursor.execute(q,(bvalue,privacy,userId,fieldId))
            
            conn.commit()
            cursor.close()
        
    
    def removeInfo(userId,category,keys):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()

            q="DELETE FROM Data WHERE userId=? AND fieldId IN ?"
            
            for field in keys:
                fieldId,defaultPrivacy=db.categoriesAndFields[category][field]
                cursor.execute(q,(userId,fieldId))
            
            conn.commit()
            cursor.close()