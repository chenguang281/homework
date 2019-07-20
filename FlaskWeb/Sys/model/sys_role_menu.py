# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysRoleMenu(db.Model):
    __tablename__ = 'sys_role_menu'

    id = db.Column(db.Integer, primary_key=True, index=True)
    role_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)
