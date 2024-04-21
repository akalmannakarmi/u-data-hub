from flask import session, request, redirect
from . import app

@app.route('/authenticate',methods=["GET"])
def authenticate():
    if 'userId' not in session:
        return redirect(f'/login?next={request.url}')
    
    return redirect(request.args.get("url","/")+f"?userId={session['userId']}")