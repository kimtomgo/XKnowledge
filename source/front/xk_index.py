from flask import render_template, Blueprint
from flask.views import View

from source.storage.xk_storage import JsonFileHandler


class XKIndex(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        file_handler = JsonFileHandler("..\\data\\test.json")
        json_data = file_handler.reader()
        return render_template("index.html", data=json_data["data"], links=json_data["links"])


class IndexBlueprint:
    @staticmethod
    def creator_blueprint():
        blueprint = Blueprint("/", __name__, url_prefix="/", template_folder="templates")
        blueprint.add_url_rule("/", view_func=XKIndex.as_view("/"))
        return blueprint
