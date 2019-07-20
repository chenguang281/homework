# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysUser(db.Model):
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
