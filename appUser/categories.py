from flask import render_template, session, request, redirect,jsonify
from . import app,db

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