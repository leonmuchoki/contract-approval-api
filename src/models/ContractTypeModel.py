from . import db
import datetime
from marshmallow import fields, Schema

class ContractTypeModel(db.Model):
    __tablename__ = 'contract_types'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self,data):
        self.id = data.get('id')
        self.name = data.get('name')

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
    def get_all_contract_types():
        return ContractTypeModel.query.all()

    @staticmethod
    def get_one_contract_type(id):
        return ContractTypeModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractTypeSchema(Schema):
	"""
	ContractType Schema
	"""
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True)