# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysUserRole(db.Model):
    __tablename__ = 'sys_user_role'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
