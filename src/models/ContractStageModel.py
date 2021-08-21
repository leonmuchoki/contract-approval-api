from . import db
import datetime
from marshmallow import fields, Schema, INCLUDE

class ContractStageModel(db.Model):
    __tablename__ = 'contract_stages'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    contract_stage = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,data):
        self.id = data.get('id')
        self.contract_stage = data.get('contract_stage')
        self.created_at = data.get('created_at')
        self.created_by = data.get('created_by')
        self.modified_at = data.get('modified_at')
        self.modified_by = data.get('modified_by')

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
    def get_all_contract_stages():
        return ContractStageModel.query.all()

    @staticmethod
    def get_one_contract_stage(id):
        return ContractStageModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractStageSchema(Schema):
    """
    Contract stage Schema
    """
    class Meta:
        unknown = INCLUDE

    id = fields.Int(dump_only=True)
    contract_stage = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)

    