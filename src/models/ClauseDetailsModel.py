from . import db
import datetime
from marshmallow import fields, Schema
from .ClauseSubDetailsModel import ClauseSubDetailsSchema

class ClauseDetailsModel(db.Model):
    __tablename__ = 'clause_details'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    clause_id = db.Column(db.Integer, db.ForeignKey('clauses.id'), nullable=False)
    clause_part_id = db.Column(db.Integer, db.ForeignKey('clause_parts.id'), nullable=False)
    clause_detail = db.Column(db.String(500))
    has_table = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    clause_sub_details = db.relationship('ClauseSubDetailsModel', backref='clause_details', lazy=True)

    def __init__(self,data):
        self.id = data.get('id')
        self.clause_id = data.get('clause_id')
        self.clause_part_id = data.get('clause_part_id')
        self.clause_detail = data.get('clause_detail')
        self.has_table = data.get('has_table')
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
    def get_all_clause_details():
        return ClauseDetailsModel.query.all()

    @staticmethod
    def get_one_clause_detail(id):
        return ClauseDetailsModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ClauseDetailsSchema(Schema):
    """
    Clause Details Schema
    """
    id = fields.Int(dump_only=True)
    clause_id = fields.Int(required=True)
    clause_part_id = fields.Int(required=True)
    clause_detail = fields.Str(required=True)
    has_table = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.Int(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    modified_by  =  fields.Int(dump_only=True)
    clause_sub_details = fields.Nested(ClauseSubDetailsSchema, many=True)