#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from Sys.service.SysMenuService import SysMenuService

route_sys_menu = Blueprint("sys_menu", __name__)


# 获得菜单列表(只取一级菜单)
@route_sys_menu.route("/get_menu_list", methods=["POST"])
def getMenuList():
    return SysMenuService.getMenuList(request)


# 获得下级菜单
@route_sys_menu.route("/get_next_menu_list", methods=["POST"])
def getNextMenuList():
    return SysMenuService.getNextMenuList(request)


# 获得菜单列表(只取一级菜单),角色支持tree
@route_sys_menu.route("/get_menu_list_role", methods=["POST"])
def getMenuListRole():
    return SysMenuService.getMenuListRole(None)


# 获得下级菜单列表,角色支持tree
@route_sys_menu.route("/get_next_menu_list_role", methods=["POST"])
def getNextMenuListRole():
    return SysMenuService.getNextMenuListRole(request)


# 新增菜单
@route_sys_menu.route("/add_menu", methods=["POST"])
def addMenu():
    return SysMenuService.addMenu(request)


# 逻辑删除菜单
@route_sys_menu.route("/del_menu", methods=["POST"])
def delMenu():
    return SysMenuService.delMenu(request)


# 得到所有菜单
@route_sys_menu.route("/get_all_menu", methods=["POST"])
def getAllMenu():
    return SysMenuService.getAllMenu(None)
