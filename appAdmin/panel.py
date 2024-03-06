from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/panel',methods=["GET"])
def adminPanel():
    if session["userId"]!=0:
        return redirect('/')
    noOfUsers=db.noOfUsers()
    noOfData=db.noOfData()
    dataTypes=db.getDataTypes()
    categoriesAndFields=db.getCategoriesAndFields()
    revCategortyAndField=db.getrevCategoryAndField()
    return render_template('admin/panel.html',session=session,noOfData=noOfData,noOfUsers=noOfUsers,
        categoriesAndFields=categoriesAndFields,dataTypes=dataTypes,revCategortyAndField=revCategortyAndField)

@app.route('/addCategory',methods=["POST"])
def addCategory():
    if session["userId"]!=0:
        return redirect('/')

    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.addCategory(request.form['category'])

    return redirect('/admin/panel')

@app.route('/removeCategory',methods=["POST"])
def removeCategory():
    if session["userId"]!=0:
        return redirect('/')
    
    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.removeCategory(request.form['category'])

    return redirect('/admin/panel')


@app.route('/addField',methods=["POST"])
def addField():
    if session["userId"]!=0:
        return redirect('/')
    
    if any(i not in request.form for i in ['category','field','dataType','privacy']):
        return jsonify("Require:{category,field,dataType}")
    
    db.addField(request.form['category'],request.form['field'],request.form['dataType'],request.form['privacy'])

    return redirect('/admin/panel')


@app.route('/removeField',methods=["POST"])
def removeField():
    if session["userId"]!=0:
        return redirect('/')
    
    if 'field' not in request.form:
        return jsonify("Require:{field}")
    
    db.removeField(request.form['field'])

    return redirect('/admin/panel')