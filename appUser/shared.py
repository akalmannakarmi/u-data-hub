from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/shared',methods=["GET"])
def shared():
	if 'userId' not in session:
		return redirect('/login')
		
	categories= db.getCategories()
	shared = db.getShared(session['userId'])
	return render_template('user/shared.html',session=session,shared=shared,subpage="shared",categories=categories)

@app.route('/myProfile/shared/rmUser',methods=["GET"])
def rmUserShared():
	if 'userId' not in session:
		return redirect('/login')

	if "receiverId" not in request.args:
		return jsonify({"Require":["receiverId"]})
	
	db.rmUserShared(session['userId'],request.args["receiverId"])

	return redirect('/myProfile/shared')

@app.route('/myProfile/shared/remove',methods=["GET"])
def removeShared():
	if 'userId' not in session:
		return redirect('/login')
		
	if "receiverId" not in request.args or "dataIds" not in request.args:
		return jsonify({"Require":["receiverId","dataIds"]})
	
	dataIds = [int(x) for x in request.args["dataIds"].split(",")]
	
	db.rmShared(session['userId'],request.args["receiverId"],dataIds)

	return redirect('/myProfile/shared')