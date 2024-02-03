from flask import Blueprint

app = Blueprint('appBasic', __name__)

from data import dbBasic
from . import index,basic,session

def init(main):
    session.init_app(main)