from .data import db,ConnPool,convertValue,db_logger
import secrets

class dbAPI:
    def generateKey():
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()

            db_logger.info("Generating APIkey")
            while True:
                key= secrets.token_hex(16)
                cursor.execute("SELECT * FROM User WHERE apiKey=?",(key,))
                if not cursor.fetchall():
                    return key

    def changeKey(userId):
        key = dbAPI.generateKey()
        db_logger.info("Changing Key for user:%d",userId)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET apiKey=? WHERE id=?", (key,userId))
            conn.commit()
            cursor.close()
        return key

    def getDataTypes():
        return db.dataTypes

    def getCategories():
        return db.categories
    
    def getCategoriesAndFields():
        return db.categoriesAndFields
    
    def getrevCategoryAndField():
        return db.revCategoryAndField
    
    def validAuth(apiKey):
        db_logger.info("Validating APIkey")
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE apiKey=?",(apiKey,))
            if cursor.fetchall():
                return True
            return False
    
    def getStats(apiKey,fields):
        db_logger.info("API getting stats")
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM User WHERE apiKey=?",(apiKey,))
            userId=cursor.fetchall()[0][0]
            
            p = ','.join(['?' for _ in fields])

            cursor.execute(f"""\
                SELECT Data.fieldId, Data.value
                FROM Data
                LEFT JOIN Shared ON Data.userId = Shared.ownerId AND Data.fieldId = Shared.fieldId
                WHERE Data.fieldId IN ({p}) AND 
                (Data.isPrivate != 1 OR (Data.isPrivate <> 0 AND Shared.userId = ?));
                """,(*fields,userId))
            
            result = cursor.fetchall()
            return result
    
    def getUserInfo(sharedId,apiKey,fields):
        db_logger.info("API getting user Info")
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM User WHERE apiKey = ?",(apiKey,))
            userId=cursor.fetchall()[0][0]
            p = ','.join(['?' for _ in fields])

            cursor.execute(f"""\
                SELECT Data.fieldId, Data.value
                FROM Data
                LEFT JOIN Shared ON Data.userId = Shared.ownerId AND Data.fieldId = Shared.fieldId
                WHERE Data.userId = ? AND Data.fieldId IN ({p}) AND 
                (Data.isPrivate = 0 OR (Data.isPrivate <> 0 AND Shared.userId = ?));
                """,(sharedId,*fields,userId))
            
            result = cursor.fetchall()
            return result