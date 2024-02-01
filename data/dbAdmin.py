import sqlite3
from .data import db

class dbAdmin:
    def __init__(self):
        self.conn = sqlite3.connect(db.name)

    def noOfData(self):
        cursor=self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FORM Data")
        cursor.close()

    def noOfUsers(self):
        cursor=self.conn.cursor()
        cursor.execute("SELECT COUNT(userId) Distinct FORM Data")
        cursor.close()

    def getCategories(self):
        return db.categories.copy()
    
    def getCategoriesAndFields(self):
        return db.categoriesAndFields.copy()


    def addCategory(self,category):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Category (name) VALUES (?)",(category,))
        self.conn.commit()

        cursor.execute("SELECT id FROM Category WHERE name=?",(category,))
        result=cursor.fetchone()
        db.categories[category]=result[0]

        cursor.close()

    def removeCategory(self,category):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Category WHERE name=?",(category,))
        self.conn.commit()

        db.categories.pop(category,0)
        db.categoriesAndFields.pop(category,0)
        for id,(cat,field) in db.revCategoryAndField.copy().items():
            if cat==category:
                db.revCategoryAndField.pop(id,0)

        cursor.close()

    def addField(self,category,field,dataTypeId):
        cursor = self.conn.cursor()
        if category not in db.categories:
            raise Exception("Category does not exists")
        categoryId = db.categories[category]
        cursor.execute("INSERT INTO Field (categoryId,name,dataTypeId) VALUES (?,?,?)",(categoryId,field,dataTypeId))
        self.conn.commit()

        cursor.execute("SELECT id FROM Field WHERE categoryId=? AND name=?",(categoryId,field))
        result = cursor.fetchone()
        db.categoriesAndFields[category][field]=result[0]
        db.revCategoryAndField[result[0]]=(category,field,dataTypeId)

        cursor.close()

    def removeField(self,fieldId):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Field WHERE id=?",(fieldId,))
        self.conn.commit()

        category,field,dataTypeId=db.revCategoryAndField[fieldId]
        db.categoriesAndFields[category].pop(field,0)
        db.revCategoryAndField.pop(fieldId,0)

        cursor.close()
