from . import db
import datetime
from marshmallow import fields, Schema

class ContractDetailModel(db.Model):
    __tablename__ = 'contract_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isactive = db.Column(db.String(1))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tender_id = db.Column(db.Integer, db.ForeignKey('tenders.id'), nullable=False) 
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    clause_id = db.Column(db.Integer, db.ForeignKey('contract_clauses.id'), nullable=False)
    iscomplete = db.Column(db.String(1))
    legal_forward_to_procurement = db.Column(db.String(1))
    ceo_forward_to_legal = db.Column(db.String(1))
    ceo_approve = db.Column(db.String(1))
    legal_approve = db.Column(db.String(1))
    date_initiated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_approved_legal = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_approved_ceo = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_forwardedback_legal = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_forwardedback_procurement = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    contract_expiry_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    contract_type = db.Column(db.Integer, db.ForeignKey('contract_types.id'), nullable=False)
    supplier = db.Column(db.Integer)
    date_supplier_signed = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    contract_value = db.Column(db.Numeric(10,2))
    

    def __init__(self,data):
       
        self.id = data.get('contract_id')
        self.isactive = data.get('isactive')
        self.created_by = data.get('created_by')
        self.tender_id = data.get('tender_id')
        self.product_id = data.get('product_id')
        self.clause_id = data.get('clause_id')
        self.iscomplete = data.get('iscomplete')
        self.legal_forward_to_procurement = data.get('legal_forward_to_procurement')
        self.ceo_forward_to_legal = data.get('ceo_forward_to_legal')
        self.ceo_approve = data.get('ceo_approve')
        self.legal_approve = data.get('legal_approve')
        self.date_initiated = data.get('date_initiated')
        self.date_approved_legal = data.get('date_approved_legal')
        self.date_approved_ceo = data.get('date_approved_ceo')
        self.date_forwardedback_legal = data.get('date_forwardedback_legal')
        self.date_forwardedback_procurement = data.get('date_forwardedback_procurement')
        self.contract_expiry_date = data.get('contract_expiry_date')
        self.supplier = data.get('supplier')
        self.date_supplier_signed = data.get('date_supplier_signed')
        self.contract_value = data.get('contractvalue')   

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
    def get_all_contract_details():
        return ContractDetailModel.query.all()

    @staticmethod
    def get_one_contract_detail(id):
        return ContractDetailModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id) 


class ContractDetailSchema(Schema):
    """
    ContractDetail Schema
    """
    id = fields.Int(dump_only=True)
    isactive = fields.Str(dump_only=True)
    created_by = fields.Str(dump_only=True)
    tender_id = fields.Str(dump_only=True)
    product_id = fields.Int(dump_only=True)
    clause_id = fields.Int(dump_only=True)
    iscomplete = fields.Str(dump_only=True)
    legal_forward_to_procurement = fields.Str(dump_only=True)
    ceo_forward_to_legal = fields.Str(dump_only=True)
    ceo_approve = fields.Str(dump_only=True)
    legal_approve = fields.Int(dump_only=True)
    date_initiated = fields.DateTime(dump_only=True)
    date_approved_legal = fields.DateTime(dump_only=True)
    date_approved_ceo = fields.DateTime(dump_only=True)
    date_forwardedback_legal = fields.DateTime(dump_only=True)
    date_forwardedback_procurement = fields.DateTime(dump_only=True)
    contract_expiry_date = fields.DateTime(dump_only=True)
    contract_type = fields.Str(dump_only=True)
    supplier = fields.Int(dump_only=True)
    date_supplier_signed = fields.DateTime(dump_only=True)
    contract_value = fields.Float(dump_only=True)