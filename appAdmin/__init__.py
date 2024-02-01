from flask import Blueprint

app = Blueprint('appAdmin', __name__)

from data import db
from . import query

def init(main):
    # session.init_app(main)
    pass