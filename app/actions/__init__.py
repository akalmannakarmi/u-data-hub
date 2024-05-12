from flask import Blueprint

app = Blueprint('actions', __name__)

from . import auth
