from .data import db,ConnPool,db_logger

class dbAdmin:
    def isAdmin(userId):
        return True

    def noOfData():
        db_logger.info("Calculating No of Data")
        with ConnPool.getConn() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Data")
            result=cursor.fetchone()[0]
            cursor.close()
            return result

    def noOfUsers():
        db_logger.info("Calculating No of Users")
        with ConnPool.getConn() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT COUNT(id) FROM User")
            result=cursor.fetchone()[0]
            cursor.close()
            return result

    def getDataTypes():
        return db.dataTypes

    def getCategories():
        return db.categories
    
    def getCategoriesAndFields():
        return db.categoriesAndFields
    
    def getrevCategoryAndField():
        return db.revCategoryAndField


    def addCategory(category):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Category (name) VALUES (?)",(category,))
            conn.commit()

            cursor.execute("SELECT id FROM Category WHERE name=?",(category,))
            result=cursor.fetchone()
            cursor.close()
            db.categories[category]=result[0]
        db.categoriesAndFields[category]={}
        db_logger.info("Added Category: %s",category)

    def removeCategory(category):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Category WHERE name=?",(category,))
            conn.commit()
            cursor.close()
            db.loadData(conn)
        
        db_logger.info("Removed Category: %s",category)
    
    def editCategory(category,oldCategory):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Category set name=? WHERE name=?",(category,oldCategory))
            conn.commit()
            cursor.close()
            db.loadData(conn)
        
        db_logger.info("Updated Category: %s->%s",oldCategory,category)

    def addField(category,field,dataTypeId,privacy):
        with ConnPool.getConn() as conn:
            dataTypeId=int(dataTypeId)
            cursor = conn.cursor()
            if category not in db.categories:
                db_logger.warn("Trying to add Field in a category that doesnt Exits: %s->%s",category,field)
                raise Exception("Category does not exists")

            categoryId = db.categories[category]
            cursor.execute("INSERT INTO Field (categoryId,name,dataTypeId,defaultPrivacy) VALUES (?,?,?,?)",(categoryId,field,dataTypeId,privacy))
            conn.commit()
            db.loadData(conn)
        
        db_logger.info("Added Field: %s->%s",category,field)

    def removeField(fieldId):
        with ConnPool.getConn() as conn:
            fieldId=int(fieldId)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Field WHERE id=?",(fieldId,))
            conn.commit()
            cursor.close()

        category,field,*_=db.revCategoryAndField[fieldId]
        db.categoriesAndFields[category].pop(field,0)
        db.revCategoryAndField.pop(fieldId,0)
        db_logger.info("Removed Field: %s->%s",category,field)

    def editField(fieldId,field,dataTypeId,privacy):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()

            cursor.execute("UPDATE Field SET name=?, dataTypeId=? ,defaultPrivacy=? WHERE id=?",(field,dataTypeId,privacy,fieldId))
            cursor.close()
        
            category,oldField,oldDataTypeId,oldPrivacy=db.revCategoryAndField[fieldId]
            db.loadData(conn)
            db_logger.info("Updated Field: (%s,%s,%d.%d)->(%s,%s,%d.%d)",category,oldField,oldDataTypeId,oldPrivacy,category,field,dataTypeId,privacy)