#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cg 2019-06-13 1.0.0
from flask import Blueprint, request
from SysSet.service.SysDictsService import SysDictsService

route_sys_set_dicts = Blueprint("sys_set_dicts", __name__)


# 得到所有标签页
@route_sys_set_dicts.route("/get_tab", methods=["POST"])
def getTab():
    return SysDictsService.getTab(None)


# 得到所有表的汉字名
@route_sys_set_dicts.route("/get_tables", methods=["POST"])
def getTables():
    return SysDictsService.getTables(request)


# 得到所有字典
@route_sys_set_dicts.route("/get_tab_column", methods=["POST"])
def getTabColumn():
    return SysDictsService.getTabColumn(request)


# 得到表内的列信息
@route_sys_set_dicts.route("/get_column", methods=["POST"])
def getColumn():
    return SysDictsService.getColumn(request)

# 得到表内的列信息
@route_sys_set_dicts.route("/save_dicts", methods=["POST"])
def saveDicts():
    return SysDictsService.saveDicts(request)