from flask import render_template,session,request,redirect
from . import app

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('errors/error.html', error=error), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', message=error.description), 403
