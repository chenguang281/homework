#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os


class Application(Flask):
    def __init__(self, import_name, template_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder)
        self.config.from_pyfile('config/base_setting.py')
        # self.config.from_pyfile('config/redis_setting.py')
        if "ops_config" in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__)

app.secret_key = os.urandom(24)
manager = Manager(app)
