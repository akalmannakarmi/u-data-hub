from .data import db,ConnPool,convertValue,toBlob,db_logger,sqlite3
from . import dbAPI

class dbUser:
    def newKey(userId):
        dbAPI.changeKey(userId)
    
    def getCategories():
        return db.categories
    
    def getCategoriesAndFields():
        return db.categoriesAndFields

    def getUserId(userTag):
        db_logger.info("Getting User Id: %s",userTag)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM User WHERE tag=?", (userTag,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result

    def getUserTag(userId):
        db_logger.info("Getting User Tag: %d",userId)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tag FROM User WHERE id=?", (userId,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result

    def getUserKey(userId):
        db_logger.info("Getting UserKey: %d",userId)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT apiKey FROM User WHERE id=?", (userId,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result

    def findUsers(tag):
        db_logger.info("Searching users: %s",tag)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            tag=f"%{tag}%"
            cursor.execute("SELECT tag FROM User WHERE tag LIKE ?",(tag,))
            result=cursor.fetchmany(50)
            cursor.close()
            return result

    def getUserData(sharedId, userId):
        db_logger.info("Getting UserData: %d->%d", sharedId, userId)
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT fieldId FROM Shared WHERE ownerId=? AND userId=?", (sharedId,userId))
            fieldIds = cursor.fetchall()
            fieldIds = [id[0] for id in fieldIds]
            placeholders = ",".join("?" for _ in fieldIds)

            query = "SELECT fieldId, value, isPrivate FROM Data WHERE userId=? AND (isPrivate NOT IN (1,2) OR fieldId IN ({placeholders}))".format(placeholders=placeholders)
            cursor.execute(query, (sharedId, *fieldIds))

            values = cursor.fetchall()
            cursor.close()

            result = {}
            for fieldId, raw, isPrivate in values:
                category, field, value = convertValue(fieldId, raw)
                result.setdefault(category, {})[field] = (value, isPrivate)
            return result

    def getMyData(userId):
        db_logger.info("Getting My data: %d",userId)
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

    def saveInfo(userId, category, fieldValues, fieldPrivacy):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()

            for field, value in fieldValues.items():
                fieldId, defaultPrivacy = db.categoriesAndFields[category][field]
                bvalue = toBlob(fieldId, value)
                privacy = fieldPrivacy[field]

                if not value:
                    # If value is empty, delete the record
                    delete_query = "DELETE FROM Data WHERE userId = ? AND fieldId = ?"
                    cursor.execute(delete_query, (userId, fieldId))
                else:
                    # Try to insert. If duplicate key detected, update the existing record.
                    try:
                        insert_query = "INSERT INTO Data (userId, fieldId, value, isPrivate) VALUES (?, ?, ?, ?)"
                        cursor.execute(insert_query, (userId, fieldId, bvalue, privacy))
                    except sqlite3.IntegrityError:
                        update_query = "UPDATE Data SET value = ?, isPrivate = ? WHERE userId = ? AND fieldId = ?"
                        cursor.execute(update_query, (bvalue, privacy, userId, fieldId))
            conn.commit()
            cursor.close()
        db_logger.info("Saved Info: %d->%s", userId, category)
    
    def removeInfo(userId,category,keys):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()

            q="DELETE FROM Data WHERE userId=? AND fieldId IN ?"
            
            for field in keys:
                fieldId,defaultPrivacy=db.categoriesAndFields[category][field]
                cursor.execute(q,(userId,fieldId))
            
            conn.commit()
            cursor.close()
        db_logger.info("Remove Info: %d->%s",userId,category)

    def getShared(userId):
        result={}
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("""\
                SELECT 
                    U.id AS receiverId,
                    U.tag AS receiver,
                    C.name AS category,
                    F.name AS field,
                    F.id AS fieldId
                FROM 
                    Shared AS S
                JOIN 
                    User AS U ON S.userId = U.id
                JOIN 
                    Field AS F ON S.fieldId = F.id
                JOIN 
                    Category AS C ON F.categoryId = C.id
                WHERE 
                    S.ownerId = ?;
                """,(userId,))
            
            tResult = cursor.fetchall()
            for row in tResult:
                result.setdefault((row["receiverId"],row["receiver"]), {})
                result[(row["receiverId"],row["receiver"])].setdefault(row["category"], [])
                result[(row["receiverId"],row["receiver"])][row["category"]].append((row["field"],row["fieldId"]))
            cursor.close()

        db_logger.info("Got Shared Datas: %d",userId)
        return result

    def rmUserShared(senderId,receiverId):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Shared WHERE ownerId = ? AND userId = ?;",(senderId,receiverId))
            conn.commit()
            cursor.close()
        db_logger.info("Remove Shared With User: %d->%d",senderId,receiverId)

    def rmShared(senderId,receiverId,fieldIds):
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            p = ','.join(['?' for _ in fieldIds])
            cursor.execute(f"DELETE FROM Shared WHERE ownerId = ? AND userId = ? AND fieldId IN {p};",(senderId,receiverId,*fieldIds))
            conn.commit()
            cursor.close()
        db_logger.info("Remove Some Shared With User: %d->%d  (%s)",senderId,receiverId,str(fieldIds))