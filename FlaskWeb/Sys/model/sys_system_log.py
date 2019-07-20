# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysSystemLog(db.Model):
    __tablename__ = 'sys_system_log'

    id = db.Column(db.Integer, primary_key=True, index=True)
    requestURL = db.Column(db.String(32))
    requestIP = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    describe = db.Column(db.String(100))
    returnCODE = db.Column(db.Integer)
    msg = db.Column(db.String(255))
