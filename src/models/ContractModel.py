from . import db
import datetime
from marshmallow import fields, Schema, INCLUDE
from .ContractProductModel import ContractProductSchema
from .ContractEntityModel import ContractEntitySchema
from .ContractTypeModel import ContractTypeSchema
from .ContractStageModel import ContractStageSchema

class ContractModel(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    contract_no = db.Column(db.String(200))
    title = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    contract_entity_purchaser_id = db.Column(db.Integer, db.ForeignKey('contract_entities.id'), nullable=False)
    contract_entity_supplier_id = db.Column(db.Integer, db.ForeignKey('contract_entities.id'), nullable=False)
    contract_type_id =  db.Column(db.Integer, db.ForeignKey('contract_types.id'))
    contract_stage_id =  db.Column(db.Integer, db.ForeignKey('contract_stages.id'))

    contract_products = db.relationship('ContractProductModel', backref='contracts', lazy=True)
    contract_type = db.relationship('ContractTypeModel', backref='contracts', lazy=True)
    contract_stage = db.relationship('ContractStageModel', backref='contracts', lazy=True)
    contract_entity_purchaser = db.relationship("ContractEntityModel", foreign_keys=[contract_entity_purchaser_id])
    contract_entity_supplier = db.relationship("ContractEntityModel", foreign_keys=[contract_entity_supplier_id])

    def __init__(self,data):
        self.id = data.get('id')
        self.contract_no = data.get('contract_no')
        self.title = data.get('title')
        self.created_at = data.get('created_at')
        self.created_by = data.get('created_by')
        self.modified_at = data.get('modified_at')
        self.modified_by = data.get('modified_by')
        self.contract_entity_purchaser_id = data.get('contract_entity_purchaser_id')
        self.contract_entity_supplier_id = data.get('contract_entity_supplier_id')
        self.contract_type_id = data.get('contract_type_id')

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
    def get_all_contracts():
        return ContractModel.query.all()

    @staticmethod
    def get_one_contract(id):
        return ContractModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractSchema(Schema):
    """
    Contract Schema
    """
    class Meta:
        unknown = INCLUDE

    id = fields.Int(dump_only=True)
    contract_no = fields.Str(required=True)
    title = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)
    contract_entity_purchaser_id  =  fields.Int(dump_only=True)
    contract_entity_supplier_id  =  fields.Int(dump_only=True)
    contract_type_id  =  fields.Int(dump_only=True)
    contract_stage_id  =  fields.Int(dump_only=True)
    contract_entity_purchaser = fields.Nested(ContractEntitySchema)
    contract_entity_supplier = fields.Nested(ContractEntitySchema)
    contract_products = fields.Nested(ContractProductSchema, many=True)
    contract_type = fields.Nested(ContractTypeSchema)
    contract_stage = fields.Nested(ContractStageSchema)

    