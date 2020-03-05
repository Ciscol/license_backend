import os
from flask import Flask, render_template, jsonify, request, make_response, current_app, g, redirect, url_for
from random import *
from flask_cors import CORS
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash

app = Flask(__name__,
            static_folder="../dist/static",  # 设置静态文件夹目录
            template_folder="../dist")  # 设置vue编译输出目录dist文件夹，为Flask模板文件目录
app.config.from_object('config')
CORS(app, supports_credentials=True)


# 跨域配置
@app.after_request
def after_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'content-type,Authorization'
    return resp


# -----------------------------------auth begin--------------------------------------------
def auth_login(view_func):
    @wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["Authorization"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4103, msg='缺少参数token')

        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except Exception:
            # return redirect(url_for('login'))
            return jsonify(code=4101, msg="登录已过期")

        return view_func(*args, **kwargs)
        # return view_func(*args, **kwargs)

    return verify_token


# auth = HTTPTokenAuth(scheme='Bearer')
#
#
# @auth.verify_token
# def verify_token(token):
#     token = request.headers.get('Authorization')
#     print("what have I get?: ", token)
#     g.user = None
#     return TokenTool.verify_auth_token(token)


# -----------------------------------auth  end--------------------------------------------

# 随机数test
@app.route('/api/random')
@auth_login
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


# token验证
@app.route('/api/authCheck')
@auth_login
def authCheck():
    pass


# 登录验证
@app.route('/api/login', methods=['POST'])
def login():
    token = TokenTool.generate_auth_token()
    response = {
        'state': 1,
        'token': token,
    }
    return response


# url redirect 所有的url将被重定向至index.html，由前端vue-router进行分发
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @auth_login
def catch_all(path):
    # 使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。
    return render_template("index.html", name="index")


# -----------------------------------error begin--------------------------------------------

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return '404', 404


# -----------------------------------error  end  --------------------------------------------


# -----------------------------------Data Base begin--------------------------------------------
# token生成验证工具 后续应存储于数据库
class TokenTool:
    @staticmethod
    def generate_auth_token(expiration=1800):
        serializer = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        token = serializer.dumps({'username': 'Cisco'}).decode('utf-8')
        return token

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
            print("what have I get?: ", data)
        except Exception:
            return jsonify(code=4101, msg="登录已过期")
        if 'username' in data:
            g.user = data['username']
            return True
        return False

# -----------------------------------end----------------------------------------------------

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
