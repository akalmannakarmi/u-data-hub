from flask import session, request, redirect,url_for
from . import app

@app.route('/authenticate',methods=["GET"])
def authenticate():
    if 'userId' not in session:
        return redirect(f'/login?next={request.url}')
    
    redirect_url=request.args.get("url","/")
    if '?' in redirect_url:
        redirect_url += f"&userId={session['userId']}"
    else:
        redirect_url += f"?userId={session['userId']}"
    print(redirect_url)
    return redirect(redirect_url)