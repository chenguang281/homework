# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from Base.common.utils.UUIDUtils import UUIDUtils

db = SQLAlchemy()


class SysUserRole(db.Model):
    __tablename__ = 'sys_user_role'

    id = db.Column(db.String(32), default=UUIDUtils.gen_id, primary_key=True)
    user_id = db.Column(db.String(32))
    role_id = db.Column(db.String(32))
