from flask import Blueprint

app = Blueprint('appAdmin', __name__)

from data import dbAdmin as db
from . import panel

def init(main):
    # session.init_app(main)
    pass