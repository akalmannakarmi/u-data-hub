from flask import render_template, session, request, redirect,jsonify
from . import app,db


@app.route('/getDataTypes',methods=["POST"])
def getDataTypes():
    if any(i not in request.form for i in ['apiKey','fields']):
        return jsonify("Require:{apiKey,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    return jsonify(db.getDataTypes())

@app.route('/getCategories',methods=["POST"])
def getCategories():
    if any(i not in request.form for i in ['apiKey','fields']):
        return jsonify("Require:{apiKey,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    return jsonify(db.getCategories())

@app.route('/getCategoriesAndFields',methods=["POST"])
def getCategoriesAndFields():
    if any(i not in request.form for i in ['apiKey','fields']):
        return jsonify("Require:{apiKey,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    return jsonify(db.getCategoriesAndFields())

@app.route('/getrevCategoryAndField',methods=["POST"])
def getrevCategoryAndField():
    if any(i not in request.form for i in ['apiKey','fields']):
        return jsonify("Require:{apiKey,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    return jsonify(db.getrevCategoryAndField())

@app.route('/getStats',methods=["POST"])
def getStats():
    if any(i not in request.form for i in ['apiKey','fields']):
        return jsonify("Require:{apiKey,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    data = db.getStats(request.form['apiKey'],request.form['fields'])
    
    return jsonify(data)


@app.route('/getUserData',methods=["POST"])
def getUserData():
    if any(i not in request.form for i in ['apiKey','userId','fields']):
        return jsonify("Require:{apiKey,userId,fields}")
    
    if not db.validAuth(request.form['apiKey']):
        return jsonify('Error:"Invalid Key"')
    
    data = db.getUserInfo(request.form['userId'],request.form['apiKey'],request.form['fields'])
    
    return render_template('viewProfile.html',session=session,data=data)