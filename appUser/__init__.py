from flask import Blueprint

app = Blueprint('appUser', __name__)

from data import dbUser as db

from . import profile,search

def init(main):
    # session.init_app(main)
    pass