from app import db
from sqlalchemy import Column, Integer, String,Enum

class User(db.Model):
	id = Column(Integer, primary_key=True)
	username = Column(String(64), unique=True, nullable=False)
	password = Column(String(128), nullable=False)
	kind = Column(Enum('user','mod','admin'),nullable=False)

	def isAdmin(id):
		user = User.query.filter_by(id=id).first()
		if user and user.kind == 'admin':
			return True
		else:
			return False

	def isMod(id):
		user = User.query.filter_by(id=id).first()
		if user and user.kind == 'mod':
			return True
		else:
			return False
	
	def isUser(id):
		user = User.query.filter_by(id=id).first()
		if user:
			return True
		else:
			return False


