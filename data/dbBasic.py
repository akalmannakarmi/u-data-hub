from .data import ConnPool,db_logger
from . import dbAPI

class dbBasic:
    def addUser(userId,userTag):
        db_logger.info("Creating User:%s",userTag)
        key = dbAPI.generateKey()
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (id,tag,apiKey) VALUES (?,?,?)", (userId,userTag,key))
            conn.commit()
        return key