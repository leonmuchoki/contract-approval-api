from . import db
import datetime
from marshmallow import fields, Schema

class ContractClauseModel(db.Model):
    __tablename__ = 'contract_clauses'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    clause_details = db.Column(db.String(800))
    department_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,data):
        self.id = data.get('id')
        self.clause_details = data.get('clause_details')
        self.department_id = data.get('department_id')
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
    def get_all_contract_clauses():
        return ContractClauseModel.query.all()

    @staticmethod
    def get_one_contract_clause(id):
        return ContractClauseModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractClauseSchema(Schema):
    """
    ContractClause Schema
    """
    id = fields.Int(dump_only=True)
    clause_details = fields.Str(required=True)
    department_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)