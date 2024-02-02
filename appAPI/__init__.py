from flask import Blueprint

app = Blueprint('appAPI', __name__)

from data import dbAPI as db

from . import query

def init(main):
    # session.init_app(main)
    pass