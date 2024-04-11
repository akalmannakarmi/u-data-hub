from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/request',methods=["GET","POST"])
def requeste():
	if 'userId' not in session:
		return redirect('/login')
	if request.method != "POST":
		categoriesAndFields = db.getCategoriesAndFields()
		categories=db.getCategories()
		return render_template('user/request.html',session=session,categories=categories,categoriesAndFields=categoriesAndFields)

	if "fields" not in request.form:
		return jsonify({"Require":["fields"]})
	
	reqId = db.getRequestId(request.form.getlist("fields"))
	url= request.url_root+f"request?userId={session['userId']}&reqId={reqId}"
	return jsonify(url)