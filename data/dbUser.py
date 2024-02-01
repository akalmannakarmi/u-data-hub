import sqlite3
from .data import db,convertValue,toBlob

class dbUser:
    def __init__(self):
        self.conn = sqlite3.connect(db.name)
    
    def getUserId(self,userTag):
        pass

    def getUserData(self,userId):
        cursor = self.conn.cursor()
        cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=?", (userId,))
        values = cursor.fetchall()
        result={}
        for fieldId,raw,isPrivate in values:
            category,field,value = convertValue(fieldId,raw)
            result[category][field]=(value,isPrivate==1)
        return result
    
    def addInfo(self,userId,keyvalues):
        cursor = self.conn.cursor()
        if any(key not in db.revCategoryAndField for key in keyvalues):
            raise Exception("Category or Field does not exists")
        
        q="INSERT INTO Data (userId,fieldId,valueId,isPrivate) VALUES (?,?,?)"

        for fieldId,(value,isPrivate) in keyvalues.items():
            bvalue=toBlob(value)
            cursor.execute(q,(userId,fieldId,bvalue,isPrivate))
        
        self.conn.commit()
        cursor.close()

    def editInfo(self,userId,keyvalues):
        cursor = self.conn.cursor()
        if any(key not in db.revCategoryAndField for key in keyvalues):
            raise Exception("Category or Field does not exists")
        
        q="UPDATE Data SET value=?, isPrivate=? WHERE userId=? AND fieldId=?"

        for fieldId,(value,isPrivate) in keyvalues.items():
            bvalue=toBlob(value)
            cursor.execute(q,(bvalue,isPrivate,userId,fieldId))
        
        self.conn.commit()
        cursor.close()
        
    
    def removeInfo(self,userId,keys):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Data WHERE userId=? AND fieldId IN ?")
        self.conn.commit()
        cursor.close()