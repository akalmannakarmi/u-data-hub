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

@app.route('/myProfile',methods=["GET"])
def myProfile():
    if 'userId' not in session:
        return redirect('/login')
    
    categoriesAndFields = db.getCategoriesAndFields()
    userTag = db.getUserTag(session['userId'])
    userKey = db.getUserKey(session['userId'])
    userData = db.getMyData(session['userId'])
    print(userData)
    print(categoriesAndFields)
    return render_template('user/myProfile.html',categoriesAndFields=categoriesAndFields,session=session,userTag=userTag,userKey=userKey,userData=userData)

@app.route('/myProfile/newKey',methods=["POST"])
def newKey():
    if 'userId' not in session:
        return redirect('/login')
    
    db.newKey(session['userId'])
    return redirect('/myProfile')

@app.route('/myProfile/<category>/add',methods=["POST"])
def addFields(category):
    if 'userId' not in session:
        return redirect('/login')

    categoriesAndFields= db.getCategoriesAndFields()
    if category not in categoriesAndFields:
        return jsonify('Category Does not Exists')
    
    data = request.form
    fields = categoriesAndFields[category]
    fieldValues = {key: value for key, value in data.items() if key in fields}
    fieldPrivacy = {key[:-1]: value for key, value in data.items() if key[:-1] in fields}
    
    db.addInfo(session['userId'],category,fieldValues,fieldPrivacy)

    return redirect('/myProfile')

@app.route('/myProfile/<category>/edit',methods=["POST"])
def editFields(category):
    if 'userId' not in session:
        return redirect('/login')

    categoriesAndFields= db.getCategoriesAndFields()
    if category not in categoriesAndFields:
        return jsonify('Category Does not Exists')
    
    
    data = request.form
    fields = categoriesAndFields[category]
    fieldValues = {key: value for key, value in data.items() if key in fields}
    fieldPrivacy = {key[:-1]: value for key, value in data.items() if key[:-1] in fields}
    
    db.editInfo(session['userId'],category,fieldValues,fieldPrivacy)

    return redirect('/myProfile')

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

    return redirect('/myProfile')