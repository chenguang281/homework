#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cg 2019-06-13 1.0.0
from flask import Blueprint, request
from Sys.service.SysLogService import SysLogService

route_sys_log = Blueprint("sys_log", __name__)


# 得到所有日志
@route_sys_log.route("/get_all", methods=["POST"])
def getAllLog():
    return SysLogService.getAllLog(request)
