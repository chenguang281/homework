# pyFlask
倒表命令
flask-sqlacodegen "mysql+pymysql://root:123456@127.0.0.1:3306/flask" --tables sys_user --outfile "Sys/model/sys_user.py" --flask

后台包下载:
切换到Base目录下,输入pip install -r requirements.txt 等待安装完成即可.如有报错,可多次尝试(一般都为网络问题)
前端包初始化:
切换到WebPage/VUE_Page目录下,输入npm install 等待安装完成即可.如有报错,可多次尝试(一般都为网络问题)
SQl脚本保存在Base/docs/mysqld.md下

0.0.2版本加入内容.
1,flask权限验证.
    采用token请求头验证,vue每次传参需要在请求头设置authorization(加密签名串)和user_id(用户UUID).
    每次会生成唯一的authorization(加密签名串),且用于做OSS验证,30分钟无操作则失效.
    注意:  203没有权限,
          204和上次登录信息不匹配,未做鉴权(OSS验证未通过).
          205没有登录,或登录超时(30分钟未操作).
    需要在每个axios加入code验证.