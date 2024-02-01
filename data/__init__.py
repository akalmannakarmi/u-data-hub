from .data import db
from .dbAdmin import dbAdmin
from .dbAPI import dbAPI
from .dbUser import dbUser

def init():
    db.init()