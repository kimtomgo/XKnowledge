from flask import Flask, Blueprint, redirect, url_for

from xk_homepage import XKHomePageViewAPI
from xk_mainview import XKMainViewAPI


class XKBlueprint:
    @staticmethod
    def creator_blueprint():
        blueprint = Blueprint("XKnowledge", __name__, url_prefix="/", static_folder="static",
                              template_folder="templates")
        blueprint.add_url_rule("XKHomePageView", view_func=XKHomePageViewAPI.as_view("XKHomePageView"))
        blueprint.add_url_rule("XKMainView", view_func=XKMainViewAPI.as_view("XKMainView"))
        return blueprint


if __name__ == "__main__":
    """软件入口"""
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.register_blueprint(XKBlueprint.creator_blueprint())  # 在app中注册蓝图


    @app.route("/")
    def index():
        return redirect(url_for("XKnowledge.XKHomePageView"))


    print(app.url_map)
    app.run(debug=True)  # 以debug模式运行应用
