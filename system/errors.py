"""
错误处理函数
@author 杨明树
@date 2022-03-31
"""
import json
import os
import traceback
from datetime import date

from flask import request
from werkzeug.exceptions import HTTPException

from system.configuration import SystemConfiguration as sc
from system.utils import get_project_path


class APIException(HTTPException):
    """
    自定义异常类
    @author 杨明树
    @date 2022-04-01
    """
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 999
    data = None

    def __init__(self, msg=None, code=None, error_code=None, data=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            data=self.data,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body, sort_keys=False, ensure_ascii=False)
        return text

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers"""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        """获取请求路径"""
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class Success(APIException):
    """请求成功"""
    code = 200
    msg = 'ok'
    error_code = 0
    data = None


class ServerError(APIException):
    """服务器内部错误"""
    code = 500
    msg = 'Internal server exceptions!'
    error_code = 999
    data = None


class ParameterException(APIException):
    """无效参数"""
    code = 400
    msg = 'invalid parameter'
    error_code = 1000
    data = None


class NotFound(APIException):
    """资源不存在"""
    code = 404
    msg = 'the resource are not found'
    error_code = 1001
    data = None


class AuthFailed(APIException):
    """授权失败"""
    code = 401
    msg = 'authorization failed'
    error_code = 1005
    data = None


class Forbidden(APIException):
    """权限不足"""
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'
    data = None


@sc.APP.errorhandler(Exception)
def framework_error(e: Exception):
    """全局AOP错误处理"""
    sc.logger.error(f"Error Info: {e} --- Request URL: {request.remote_addr} - {APIException.get_url_no_param()}")  # 对错误进行日志记录
    log_file = get_project_path() + os.getenv('LOG_FILE_PATH') + (date.today().isoformat() + '.log')
    with open(file=log_file, mode='a') as f:
        traceback.print_exc(file=f)

    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # if not APP.config['DEBUG']:
        #     return ServerError()
        # else:
        #     return e
        return ServerError(ServerError.msg + str(e))
