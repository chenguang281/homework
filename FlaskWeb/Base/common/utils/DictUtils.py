#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DictUtils:

    @staticmethod
    def RowProxy_Dict(rowProxy,SysMenu):
        # 取得对象内的所有属性
        li = []
        for i in dir(SysMenu):
            if not i.startswith('_') and not i.endswith('_'):
                li.append(i)
        returnData = {}
        for v in rowProxy:
            key = None
            for k in dir(SysMenu):
                key = k
            print(k.str(SysMenu.id))
        print(111)
        None