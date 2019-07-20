# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysRole(db.Model):
    __tablename__ = 'sys_role'

    id = db.Column(db.Integer, primary_key=True, index=True)
    role_name = db.Column(db.String(50))
    describe = db.Column(db.String(100))
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
