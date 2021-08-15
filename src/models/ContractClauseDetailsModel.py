from . import db
import datetime
from marshmallow import fields, Schema

class ContractClauseDetailModel(db.Model):
    __tablename__ = 'contract_clause_details'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    contract_clause_id = db.Column(db.Integer, db.ForeignKey('contract_clauses.id'), nullable=False)
    clause_part = db.Column(db.String(200))
    clause_part_name = db.Column(db.String(200))
    clause_part_detail = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,data):
        self.id = data.get('id')
        self.contract_id = data.get('contract_id')
        self.clause_part = data.get('clause_part')
        self.clause_part_name = data.get('clause_part_name')
        self.clause_part_detail = data.get('clause_part_detail')
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
    def get_all_contract_clause_details():
        return ContractClauseDetailModel.query.all()

    @staticmethod
    def get_one_contract_clause_detail(id):
        return ContractClauseDetailModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractClauseDetailsSchema(Schema):
    """
    ContractClauseDetail Schema
    """
    id = fields.Int(dump_only=True)
    contract_id = fields.Int(required=True)
    clause_part = fields.Str(required=True)
    clause_part_name = fields.Str(required=True)
    clause_part_detail = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)