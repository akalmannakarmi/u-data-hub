from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/profile/<userTag>',methods=["GET"])
def viewProfile(userTag):
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

@app.route('/myProfile/<category>',methods=["GET"])
def category(category):
    if 'userId' not in session:
        return redirect('/login')
    
    categoriesAndFields = db.getCategoriesAndFields()
    if category not in categoriesAndFields:
        return jsonify("Error:Invalid Category")
    
    categories = db.getCategories()
    fieldValues=categoriesAndFields[category]
    userData = db.getMyData(session['userId'])
    return render_template('user/myCategory.html',session=session,category=category,subpage=category,categories=categories,fieldValues=fieldValues,userData=userData)

@app.route('/myProfile/<category>/save',methods=["POST"])
def saveFields(category):
    if 'userId' not in session:
        return redirect('/login')

    categoriesAndFields= db.getCategoriesAndFields()
    if category not in categoriesAndFields:
        return jsonify('Category Does not Exists')
    
    data = request.form
    fields = categoriesAndFields[category]
    fieldValues = {key: value for key, value in data.items() if key in fields}
    fieldPrivacy = {key[:-1]: value for key, value in data.items() if key[:-1] in fields}
    
    db.saveInfo(session['userId'],category,fieldValues,fieldPrivacy)

    return redirect('/myProfile/home')

@app.route('/myProfile/<category>/remove',methods=["POST"])
def removeFields(category):
    if 'userId' not in session:
        return redirect('/login')
    
    categoriesAndFields= db.getCategoriesAndFields()
    if category not in categoriesAndFields:
        return jsonify('Category Does not Exists')

    
    data = request.form
    fields = categoriesAndFields[category]
    fieldValues = [key for key in data if key in fields]
    
    db.removeInfo(session['userId'],category,fieldValues)

    return redirect('/myProfile/home')