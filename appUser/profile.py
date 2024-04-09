from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/viewProfile/<userTag>',methods=["GET"])
def viewProfile(userTag):
    if 'userId' not in session:
        return redirect('/login')
    
    userId = db.getUserId(userTag)
    if userId == session['userId']:
        userData = db.getUserData(userId,0)
    else:
        userData = db.getUserData(userId,session['userId'])
    return render_template('user/viewProfile.html',session=session,userTag=userTag,userData=userData)

@app.route('/myProfile/newKey',methods=["GET"])
def newKey():
    if 'userId' not in session:
        return redirect('/login')
    
    db.newKey(session['userId'])
    return redirect('/myProfile/home')

@app.route('/myProfile/home',methods=["GET"])
def myProfile():
    if 'userId' not in session:
        return redirect('/login')
    
    categories = db.getCategories()
    userTag = db.getUserTag(session['userId'])
    userKey = db.getUserKey(session['userId'])
    return render_template('user/myProfile.html',session=session,categories=categories,userTag=userTag,userKey=userKey,subpage="home")
