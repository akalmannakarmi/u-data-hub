from .data import db,ConnPool,convertValue,toBlob

class dbUser:
    def getUserId(userTag):
        pass

    def getUserData(userId):
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
    
    def addInfo(userId,keyvalues):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            if any(key not in db.revCategoryAndField for key in keyvalues):
                raise Exception("Category or Field does not exists")
            
            q="INSERT INTO Data (userId,fieldId,valueId,isPrivate) VALUES (?,?,?)"

            for fieldId,(value,isPrivate) in keyvalues.items():
                bvalue=toBlob(value)
                cursor.execute(q,(userId,fieldId,bvalue,isPrivate))
            
            conn.commit()
            cursor.close()

    def editInfo(userId,keyvalues):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            if any(key not in db.revCategoryAndField for key in keyvalues):
                raise Exception("Category or Field does not exists")
            
            q="UPDATE Data SET value=?, isPrivate=? WHERE userId=? AND fieldId=?"

            for fieldId,(value,isPrivate) in keyvalues.items():
                bvalue=toBlob(value)
                cursor.execute(q,(bvalue,isPrivate,userId,fieldId))
            
            conn.commit()
            cursor.close()
        
    
    def removeInfo(userId,keys):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Data WHERE userId=? AND fieldId IN ?")
            conn.commit()
            cursor.close()