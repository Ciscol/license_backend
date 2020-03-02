from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS

app = Flask(__name__,
            static_folder="../dist/static",  # 设置静态文件夹目录
            template_folder="../dist")  # 设置vue编译输出目录dist文件夹，为Flask模板文件目录
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html", name="index")  # 使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。

# if __name__ == '__main__':
#     app.debug = True
#     app.run()