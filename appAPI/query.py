from flask import render_template, session, request, redirect,jsonify
from . import app,db


@app.route('/getCategoryFields',methods=["POST"])
def getStats():
    if any(i not in request.form for i in ['authKey','fields']):
        return jsonify("Require:{authKey,fields}")
    
    if not db.validAuth(request.form['authKey']):
        return jsonify('Error:"Invalid Key"')
    
    return jsonify(db.categoriesAndFields)

@app.route('/getStats',methods=["POST"])
def getStats():
    if any(i not in request.form for i in ['authKey','fields']):
        return jsonify("Require:{authKey,fields}")
    
    if not db.validAuth(request.form['authKey']):
        return jsonify('Error:"Invalid Key"')
    
    data = db.getInfos(request.form['fields'])
    
    return jsonify(data)


@app.route('/getUserData',methods=["POST"])
def getStats():
    if any(i not in request.form for i in ['authKey','userId','fields']):
        return jsonify("Require:{authKey,userId,fields}")
    
    if not db.validAuth(request.form['authKey']):
        return jsonify('Error:"Invalid Key"')
    
    data = db.getUserInfo(request.form['userId'],request.form['authKey'],request.form['fields'])
    
    return render_template('viewProfile.html',session=session,data=data)