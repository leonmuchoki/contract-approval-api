from . import db
import datetime
from marshmallow import fields, Schema

class ClauseSubDetailsModel(db.Model):
    __tablename__ = 'clause_sub_details'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    clause_details_id = db.Column(db.Integer, db.ForeignKey('clause_details.id'), nullable=False)
    clause_sub_detail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,data):
        self.id = data.get('id')
        self.clause_details_id = data.get('clause_details_id')
        self.clause_sub_detail = data.get('clause_sub_detail')
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
    def get_all_clause_sub_details():
        return ClauseSubDetailsModel.query.all()

    @staticmethod
    def get_one_clause_sub_detail(id):
        return ClauseSubDetailsModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ClauseSubDetailsSchema(Schema):
    """
    Clause Sub Details Schema
    """
    id = fields.Int(dump_only=True)
    clause_details_id = fields.Int(required=True)
    clause_sub_detail = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)