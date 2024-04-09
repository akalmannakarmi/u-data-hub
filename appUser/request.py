from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/request',methods=["GET"])
def requeste():
    if 'userId' not in session:
        return redirect('/login')
    
    categories = db.getCategories()
    userTag = db.getUserTag(session['userId'])
    userKey = db.getUserKey(session['userId'])
    return render_template('user/myProfile.html',session=session,categories=categories,userTag=userTag,userKey=userKey,subpage="home")
