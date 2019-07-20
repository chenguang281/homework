# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysLoginLog(db.Model):
    __tablename__ = 'sys_login_log'

    id = db.Column(db.Integer, primary_key=True, index=True)
    token = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)
    userID = db.Column(db.String(32))
    username = db.Column(db.String(50))
    status = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)
