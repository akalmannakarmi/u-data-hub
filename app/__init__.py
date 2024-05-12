from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

from .models import User

def createApp(app:Flask,config:Config):

	app.config.from_object(config)

	db.init_app(app)

	with app.app_context():
		db.create_all()

	
	from . import views,actions,components
	app.register_blueprint(actions.app)
	app.register_blueprint(components.app)
	app.register_blueprint(views.app)

	return app