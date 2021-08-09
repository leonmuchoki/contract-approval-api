from . import db
import datetime
from marshmallow import fields, Schema

class ContractEntityModel(db.Model):
    __tablename__ = 'contract_entities'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    entity_name = db.Column(db.String(200))
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    #contracts = db.relationship('ContractModel', backref='contract_entities', lazy=True)

    def __init__(self,data):
        self.id = data.get('id')
        self.entity_name = data.get('entity_name')
        self.description = data.get('description')
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
    def get_all_contract_entities():
        return ContractEntityModel.query.all()

    @staticmethod
    def get_one_contract_entity(id):
        return ContractEntityModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractEntitySchema(Schema):
    """
    Contract Entity Schema
    """
    id = fields.Int(dump_only=True)
    entity_name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)
    #contracts = fields.Nested(ContractSchema, many=True)