import sqlite3
from .data import db,convertValue

class dbAPI:
    def __init__(self):
        self.conn = sqlite3.connect(db.name)
    
    def getCategoriesAndFields(self):
        return db.categoriesAndFields.copy()
    
    def validAuth(self):
        return True
    
    def getStats(self,fields):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, value FROM Data WHERE isPrivate != 1 AND id IN ?", (tuple(fields),))
        values = cursor.fetchall()
        result={}
        for fieldId,raw in values:
            category,field,value = convertValue(fieldId,raw)
            result[category][field]=value
        return result
    
    def getUserInfo(self,userId,authKey,fields):
        if not authKey:
            return
        cursor = self.conn.cursor()
        cursor.execute("SELECT fieldId, value, isPrivate FROM Data WHERE userId=?", (userId,))
        values = cursor.fetchall()
        result={}
        for fieldId,raw,isPrivate in values:
            category,field,value = convertValue(fieldId,raw)
            result[category][field]=(value,isPrivate==1)
        return result