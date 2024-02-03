from .data import ConnPool
from . import dbAPI

class dbBasic:
    def addUser(userId,userTag):
        key = dbAPI.generateKey()
        with ConnPool.getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (id,tag,apiKey) VALUES (?,?,?)", (userId,userTag,key))
            conn.commit()