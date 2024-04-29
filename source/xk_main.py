from flask import Flask

from source.front.xk_index import IndexBlueprint

if __name__ == "__main__":
    """软件入口"""
    app = Flask(__name__)

    app.register_blueprint(IndexBlueprint.creator_blueprint())  # 在app中注册蓝图

    app.run(debug=True)  # 以debug模式运行应用
