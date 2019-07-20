#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Sys.controller.sys_user_controller import route_sys_user
from Sys.controller.sys_role_controller import route_sys_role
from Sys.controller.sys_menu_controller import route_sys_menu
from Sys.controller.sys_log_controller import route_sys_log
from SysSet.controller.sys_dicts_controller import route_sys_set_dicts

from Goods.controller.g_channel_controller import route_g_channel

'''
统一拦截处理和统一错误处理,包含500,404,403验证,签名验证,数据入库加密,出库解密等操作.
'''
from Base.filter.MethodInterceptor import *

"""
蓝图配置
"""
"""
sys模块路由
"""
app.register_blueprint(route_sys_user, url_prefix="/api/sys_user")  # 注入sys用户模块蓝图管理
app.register_blueprint(route_sys_role, url_prefix="/api/sys_role")  # 注入sys角色模块蓝图管理
app.register_blueprint(route_sys_menu, url_prefix="/api/sys_menu")  # 注入sys角色模块蓝图管理
app.register_blueprint(route_sys_log, url_prefix="/api/sys_log")  # 注入sys日志模块蓝图管理

"""
G商品模块路由
"""
app.register_blueprint(route_g_channel, url_prefix="/api/goods/channel")  # 注入商品渠道模块蓝图管理

"""
文件服务路由
"""
"""
系统设置路由
"""
app.register_blueprint(route_sys_set_dicts, url_prefix="/api/sys_set/dicts")  # 注入字典模块蓝图管理
