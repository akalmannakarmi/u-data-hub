from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/search',methods=["GET"])
def search():
    tag=request.args.get('q',"",str)
    users=db.findUsers(tag)
    return render_template('user/search.html',session=session,users=users)