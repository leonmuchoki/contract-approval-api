from . import db
import datetime
from marshmallow import fields, Schema
from .ClauseDetailsModel import ClauseDetailsSchema
from .ContractTypeModel import ContractTypeSchema

class ClauseModel(db.Model):
    __tablename__ = 'clauses'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contract_types.id'), nullable=False)
    clause_title = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    clause_details = db.relationship('ClauseDetailsModel', backref='clauses', lazy=True)
    contract_types = db.relationship('ContractTypeModel', backref='clauses', lazy=True)

    def __init__(self,data):
        self.id = data.get('id')
        self.contract_type_id = data.get('contract_type_id')
        self.clause_title = data.get('clause_title')
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
    def get_all_clauses():
        return ClauseModel.query.all()

    @staticmethod
    def get_one_clause(id):
        return ClauseModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ClauseSchema(Schema):
    """
    Clauses Schema
    """
    id = fields.Int(dump_only=True)
    contract_type_id = fields.Int(required=True)
    clause_title = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)
    clause_details = fields.Nested(ClauseDetailsSchema, many=True)
    contract_types = fields.Nested(ContractTypeSchema)