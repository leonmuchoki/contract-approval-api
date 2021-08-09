from marshmallow import fields, Schema
from . import db
import datetime
from .UserModel import UserSchema

class RoleModel(db.Model):
	"""
	Role Model for storing roles e.g. procurement, legal, ceo, supplier
	"""
	__tablename__ = 'roles'
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	role_name = db.Column(db.String(200), unique=True, nullable=False)
	users = db.relationship('UserModel', backref='roles', lazy=True)

	def __init__(self, role_name):
		self.role_name = role_name

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self, data):
		for key, item in data.items():
			setattr(self, key, item)
		self.modified_at = datetime.datetime.utcnow()
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	@staticmethod
	def get_all_roles():
		return RoleModel.query.all()

	@staticmethod
	def get_one_role(id):
		return RoleModel.query.get(id)

	def __repr__(self):
		return '<id: role_name: {}'.format(self.role_name)

class RoleSchema(Schema):
	id = fields.Int(dump_only=True)
	role_name = fields.Str(required=True)
	users = fields.Nested(UserSchema, many=True)