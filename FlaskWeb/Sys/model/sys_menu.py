# coding: utf-8
# cg 2019-06-13 1.0.0
from Base.application import db


class SysMenu(db.Model):
    __tablename__ = 'sys_menu'

    id = db.Column(db.Integer, primary_key=True, index=True)
    menu_name = db.Column(db.String(50))
    url = db.Column(db.String(100))
    icon = db.Column(db.String(50))
    order = db.Column(db.Integer)
    type = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    pid = db.Column(db.Integer)
