from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/adminPanel',methods=["GET"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    noOfUsers=db.noOfUsers()
    noOfData=db.noOfData()
    return render_template('admin/panel.html',session=session,noOfData=noOfData,noOfUsers=noOfUsers)

@app.route('/admin/addCategory',methods=["POST"])
def addCategory():
    if not db.isAdmin(session["userId"]):
        return redirect('/')

    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.addCategory(request.form['category'])

    return redirect('/adminPanel')

@app.route('/admin/removeCategory',methods=["POST"])
def removeCategory():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.addCategory(request.form['category'])

    return redirect('/adminPanel')


@app.route('/admin/addField',methods=["POST"])
def addField():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if any(i not in request.form for i in ['category','field','dataType']):
        return jsonify("Require:{category,field,dataType}")
    
    db.addField(request.form['category'],request.form['field'],request.form['dataType'])

    return redirect('/adminPanel')


@app.route('/admin/removeField',methods=["POST"])
def removeField():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if 'field' not in request.form:
        return jsonify("Require:{field}")
    
    db.removeField(request.form['field'])

    return redirect('/adminPanel')