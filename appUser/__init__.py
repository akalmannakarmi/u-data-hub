from flask import Blueprint

app = Blueprint('userApp', __name__)

from . import profile

def init(main):
    # session.init_app(main)
    pass