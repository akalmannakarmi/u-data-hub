from flask import Blueprint

app = Blueprint('components', __name__,url_prefix='/components')

from . import auth
