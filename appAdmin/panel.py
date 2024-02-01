from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/adminPanel',methods=["GET"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    noOfUsers=db.noOfUsers()
    noOfData=db.noOfData()
    return render_template('adminPanel.html',session=session,noOfData=noOfData,noOfUsers=noOfUsers)

@app.route('/admin/addCategory',methods=["POST"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')

    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.addCategory(request.form['category'])

    return redirect('/adminPanel')

@app.route('/admin/removeCategory',methods=["POST"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if 'category' not in request.form:
        return jsonify("Require:{category}")
    
    db.addCategory(request.form['category'])

    return redirect('/adminPanel')


@app.route('/admin/addField',methods=["POST"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if any(i not in request.form for i in ['category','field','dataType']):
        return jsonify("Require:{category,field,dataType}")
    
    db.addField(request.form['category'],request.form['field'],request.form['dataType'])

    return redirect('/adminPanel')


@app.route('/admin/removeField',methods=["POST"])
def adminPanel():
    if not db.isAdmin(session["userId"]):
        return redirect('/')
    
    if any(i not in request.form for i in ['field']):
        return jsonify("Require:{field}")
    
    db.removeField(request.form['field'])

    return redirect('/adminPanel')