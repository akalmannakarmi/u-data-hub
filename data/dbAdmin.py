from .data import db,ConnPool

class dbAdmin:
    def isAdmin(userId):
        return True

    def noOfData():
        with ConnPool.getConn() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Data")
            cursor.close()

    def noOfUsers():
        with ConnPool.getConn() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT userId) FROM Data")
            cursor.close()

    def getCategories():
        return db.categories.copy()
    
    def getCategoriesAndFields():
        return db.categoriesAndFields.copy()


    def addCategory(category):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Category (name) VALUES (?)",(category,))
            conn.commit()

            cursor.execute("SELECT id FROM Category WHERE name=?",(category,))
            result=cursor.fetchone()
            cursor.close()
            db.categories[category]=result[0]

    def removeCategory(category):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Category WHERE name=?",(category,))
            conn.commit()
            cursor.close()

            db.categories.pop(category,0)
            db.categoriesAndFields.pop(category,0)
            for id,(cat,field) in db.revCategoryAndField.copy().items():
                if cat==category:
                    db.revCategoryAndField.pop(id,0)

    def addField(category,field,dataTypeId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            if category not in db.categories:
                raise Exception("Category does not exists")
            categoryId = db.categories[category]
            cursor.execute("INSERT INTO Field (categoryId,name,dataTypeId) VALUES (?,?,?)",(categoryId,field,dataTypeId))
            conn.commit()

            cursor.execute("SELECT id FROM Field WHERE categoryId=? AND name=?",(categoryId,field))
            result = cursor.fetchone()
            cursor.close()
            db.categoriesAndFields[category][field]=result[0]
            db.revCategoryAndField[result[0]]=(category,field,dataTypeId)

    def removeField(fieldId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Field WHERE id=?",(fieldId,))
            conn.commit()
            cursor.close()

            category,field,dataTypeId=db.revCategoryAndField[fieldId]
            db.categoriesAndFields[category].pop(field,0)
            db.revCategoryAndField.pop(fieldId,0)

