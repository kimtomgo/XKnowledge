import os

from flask import render_template, Blueprint, request
from flask.views import View

from source.storage.xk_storage import JsonFileHandler


class XKIndex(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "GET":
            title = "test.json"
            absolute_path = os.path.abspath("..\\data\\{0}".format(title))
            file_handler = JsonFileHandler(absolute_path)
            file_handler.reader()
            file_handler.package_data(title)
            json_data = file_handler.get_json()
            return render_template("index.html", json_data=json_data)
        elif request.method == "POST":
            return "Hello"
        return "Error"


class IndexBlueprint:
    @staticmethod
    def creator_blueprint():
        blueprint = Blueprint(
            "/", __name__, url_prefix="/", template_folder="templates"
        )
        blueprint.add_url_rule("/", view_func=XKIndex.as_view("/"))
        return blueprint
