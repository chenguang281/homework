# coding: utf-8
from Base.application import db


class SetDictionary(db.Model):
    __tablename__ = 'set_dictionary'

    id = db.Column(db.Integer, primary_key=True, index=True)
    num = db.Column(db.Integer)
    table_code = db.Column(db.String(50), index=True)
    column_code = db.Column(db.String(50))
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    status = db.Column(db.Integer)
