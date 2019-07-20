#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

SERVER_PORT = 5000
DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/flask?charset=utf8mb4&autocommit=True"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENCODING = 'utf-8'