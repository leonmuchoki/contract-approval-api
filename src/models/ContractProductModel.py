from . import db
import datetime
from marshmallow import fields, Schema

class ContractProductModel(db.Model):
    __tablename__ = 'contract_products'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,data):
        self.id = data.get('id')
        self.contract_id = data.get('contract_id')
        self.product_id = data.get('product_id')
        self.product_quantity = data.get('product_quantity')
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
    def get_all_contract_products():
        return ContractProductModel.query.all()

    @staticmethod
    def get_one_contract_product(id):
        return ContractProductModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ContractProductSchema(Schema):
    """
    Contract Product Schema
    """
    id = fields.Int(dump_only=True)
    contract_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    product_quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)