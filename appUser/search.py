from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/search',methods=["GET"])
def search():
    request.args
    users=findUsers(request.args)
    return render_template('search.html',session=session,users=users)