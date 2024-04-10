from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/shared',methods=["GET"])
def shared():
	if 'userId' not in session:
		return redirect('/login')
		
	categories= db.getCategories()
	shared = db.getShared(session['userId'])
	return render_template('user/shared.html',session=session,shared=shared,subpage="shared",categories=categories)

@app.route('/myProfile/shared/rmUser',methods=["POST"])
def rmUserShared():
	if 'userId' not in session:
		return redirect('/login')

	if "sharedUserId" not in request.form:
		return jsonify({"Require":["sharedUserId"]})
	
	db.rmUserShared(session['userId'],request.form["sharedUserId"])

	return redirect('/myProfile/shared')

@app.route('/myProfile/shared/remove',methods=["POST"])
def removeShared():
	if 'userId' not in session:
		return redirect('/login')
		
	if "sharedUserId" not in request.form or "dataIds" not in request.form:
		return jsonify({"Require":["sharedUserId","dataIds"]})
	
	dataIds = [int(x) for x in request.form["dataIds"].split(",")]
	
	db.rmShared(session['userId'],dataIds)

	return redirect('/myProfile/shared')