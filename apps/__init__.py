from flask import Blueprint

app = Blueprint('apps', __name__)

from . import index,basic,session

def init(main):
    session.init_app(main)