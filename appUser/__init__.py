from flask import Blueprint

app = Blueprint('appUser', __name__)

from data import dbUser as db

from . import profile,search,request,shared,categories

def init(main):
    # session.init_app(main)
    pass