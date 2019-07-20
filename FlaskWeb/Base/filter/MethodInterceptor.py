# -*- coding: utf-8 -*-
from Base.application import app, db
from Sys.model.sys_login_log import db as logDB
from flask import jsonify, Response, json, make_response, session, request
from Sys.service.SysLogService import SysLogService

"""
500错误统一处理
"""


@app.errorhandler(Exception)
def error_500(e):
    print(e.args[0])
    return Response(json.dumps({'error': "111", "msg": "系统内部错误", "code": "403"}), 200, content_type='application/json')


"""
404错误统一处理
"""


@app.errorhandler(404)
def error_404(e):
    response = make_response(
        "<script>alert('页面不存在');window.opener=null;window.open('','_self');window.close();</script>")
    return response


"""
请求前验签,203没有权限,204和上次登录信息不匹配,未做鉴权(OSS验证未通过),205没有登录,或登录超时(30分钟未操作).
"""
# 不参与鉴权列表
PATH = {
    "/api/sys_user/login",  # 登录方法不参与鉴权
    "/api/sys_user/logOut"  # 退出方法不参与鉴权
}


@app.before_request
def before_request():
    bool = True
    for p in PATH:
        if request.path == p:
            bool = False
            break
    if bool:
        authorization = request.headers.get("authorization")  # 得到token加密签名
        user_id = request.headers.get("user_id")  # 得到用户的UUID
        path = request.headers.get("url")  # 并不是上面的后台路径,而是需要和前端交互,传过来前端真实路径.
        path = path.replace('/', '')  # 去掉/,貌似有点小bug
        if authorization and user_id:
            return SysLogService.checkAuthorization(authorization, user_id, path)
        else:
            return jsonify({'data': None, 'msg': '您还没有登录,请先登录', 'code': 205})
    return None


@app.before_request
def encryption():
    print("可以加密")
    return None
