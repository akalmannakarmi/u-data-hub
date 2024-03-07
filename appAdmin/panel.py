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


@app.route('/editCategory',methods=["POST"])
def editCategory():
    if session["userId"]!=0:
        return redirect('/')
    
    if any(i not in request.form for i in ['category','oldCategory']):
        return jsonify("Require:{category,oldCategory}")
    
    db.editCategory(request.form['category'],request.form['oldCategory'])

    return redirect('/admin/panel')


@app.route('/addField',methods=["POST"])
def addField():
    if session["userId"]!=0:
        return redirect('/')
    
    if any(i not in request.form for i in ['category','field','dataType','privacy']):
        return jsonify("Require:{category,field,dataType,privacy}")
    
    db.addField(request.form['category'],request.form['field'],request.form['dataType'],request.form['privacy'])

    return redirect('/admin/panel')


@app.route('/removeField/<fieldId>',methods=["GET"])
def removeField(fieldId):
    if session["userId"]!=0:
        return redirect('/')
    
    db.removeField(int(fieldId))

    return redirect('/admin/panel')


@app.route('/editField/<fieldId>',methods=["POST"])
def editField(fieldId):
    if session["userId"]!=0:
        return redirect('/')
    
    if any(i not in request.form for i in ['field','dataType','privacy']):
        return jsonify("Require:{field,dataType,privacy}")
    
    db.editField(int(fieldId),request.form['field'],int(request.form['dataType']),int(request.form['privacy']))

    return redirect('/admin/panel')