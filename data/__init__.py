from .data import db
from .dbAPI import dbAPI
from .dbUser import dbUser
from .dbBasic import dbBasic
from .dbAdmin import dbAdmin

def init():
    db.init()