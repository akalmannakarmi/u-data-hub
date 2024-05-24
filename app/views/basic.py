from flask import render_template,session,request,redirect
from app.wrapers import isUser
from . import app

@app.route('/')
@app.route('/index',methods=["GET"])
@isUser
def index():
    return render_template('basic/index.html',session=session)