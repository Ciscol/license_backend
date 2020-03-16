import json

from flask import Flask, render_template, jsonify, request, make_response, current_app, logging
from random import *
from flask_cors import CORS
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import logging
from logging.handlers import RotatingFileHandler
from flask_httpauth import HTTPTokenAuth
from app.license_util import license_generate, license_verify

# -----------------------------------setting begin--------------------------------------------
logging.basicConfig(level=logging.DEBUG)
file_log_handler = RotatingFileHandler('logs', maxBytes=1024 * 1024, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s %(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象添加日志记录器
logging.getLogger().addHandler(file_log_handler)

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


# -----------------------------------setting end--------------------------------------------


# -----------------------------------auth begin--------------------------------------------
auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    return TokenTool.verify_auth_token(token)


# -----------------------------------auth end--------------------------------------------


# -----------------------------------routes begin--------------------------------------------
# 登录态检查
@app.route('/api/authCheck')
@auth.login_required
def authCheck():
    return jsonify({'msg': 'ok'})


# license验证登录
@app.route('/api/login', methods=['POST'])
def login():
    try:
        user = license_verify.license_verify()
    except Exception as ex:
        return unauthorized('Invalid license. ' + str(ex))
    token = TokenTool.generate_auth_token(600, user)
    response = {
        'token': token,
    }
    return response


# license生成
@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_data()
    data = json.loads(data)['data']
    username = data['username']
    valid_seconds = data['valid_seconds']
    modules = data['modules']
    try:
        license_generate.license_generate(username, valid_seconds, modules)
    except Exception as ex:
        return unauthorized('Generate license failed. ' + str(ex))
    return jsonify({'msg': 'ok'})


# 测试接口
@app.route('/api/random')
@auth.login_required
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


# url redirect 所有的url将被重定向至index.html，由前端vue-router进行分发
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @auth_login
def catch_all():
    # 使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。
    return render_template("index.html", name="index")


# -----------------------------------routes  end--------------------------------------------


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


# -----------------------------------error  end  --------------------------------------------


# -----------------------------------Data Base begin--------------------------------------------
# token生成验证工具 后续应存储于数据库
class TokenTool:
    @staticmethod
    def generate_auth_token(expiration=1800, user=None):
        if user is None:
            user = {}
        serializer = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        token = serializer.dumps(user).decode('utf-8')
        return token

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            modules = serializer.loads(token)
        except Exception:
            return False
        # logging.info(modules)
        return True

# -----------------------------------end----------------------------------------------------

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
