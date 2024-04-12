from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/request',methods=["GET","POST"])
def requeste():
	if 'userId' not in session:
		return redirect('/login')
	if request.method == "GET":
		categoriesAndFields = db.getCategoriesAndFields()
		categories=db.getCategories()
		return render_template('user/request.html',session=session,categories=categories,categoriesAndFields=categoriesAndFields)

	if "fields" not in request.form:
		return jsonify({"Require":["fields"]})
	
	reqId = db.getRequestId(request.form.getlist("fields"))
	url= request.url_root+f"request?receiverId={session['userId']}&reqId={reqId}"
	return jsonify(url)

@app.route('/request',methods=["GET","POST"])
def acceptRequest():
	if 'userId' not in session:
		return redirect('/login')
	if request.method == "GET":
		if "receiverId" not in request.args and "reqId" not in request.args:
			return jsonify({"Require":["receiverId","reqId"]})
		categoriesAndFields = db.getCategoriesAndFields()
		reqFields = db.getRequestFields(request.args["reqId"])
		return render_template('user/acceptRequest.html',session=session,categoriesAndFields=categoriesAndFields,reqFields=reqFields,receiverId=request.args["receiverId"])
	
	rq = ["receiverId","fields"]
	if any(i not in request.form for i in rq):
		return jsonify({"Require":["receiverId","fields"]})
	
	db.shareFields(session["userId"],request.form["receiverId"],request.form.getlist("fields"))
	return redirect("/myProfile/shared")