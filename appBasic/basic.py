from flask import render_template,session,request,redirect
from . import app

@app.route('/contact')
def contact():
    return render_template('basic/contact.html',session=session)

@app.route('/help')
def help():
    return render_template('basic/help.html',session=session)

@app.route('/faq')
def faq():
    return render_template('basic/faq.html',session=session)

@app.route('/qna')
def qna():
    return render_template('basic/qna.html',session=session)