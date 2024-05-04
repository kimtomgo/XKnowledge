import os

from flask import Blueprint, render_template, request, redirect, url_for
from flask.views import MethodView
from wtforms import Form, StringField, IntegerField
from wtforms.validators import length

from source.storage.xk_json import JsonFileHandler
from storage.xk_datamanager import XKDataManager

title = "test.json"
absolute_path = os.path.abspath("..\\data\\{0}".format(title))
data_manager = XKDataManager(file_path=absolute_path, title=title)


class MainForm(Form):
    id = StringField(validators=[length(min=0, max=20, message="error")])
    node_list_length = IntegerField()
    node_list = StringField(validators=[length(min=0, max=20, message="error")])


class XKMainViewAPI(MethodView):
    """ 这个类相当于一个session，每一个session在内存中保有一个数据管理器 """

    def get(self):
        data_manager.package()
        return render_template("index.html", json_data=data_manager.get_json())

    def post(self):
        form = request.form
        loads_json = JsonFileHandler.loads_json
        # form = MainForm(request.form)
        # print(form.id.data)
        # print(form.node_list_length.data)
        # print(form.node_list.data)
        # print(url_for("/.XKMainView"))
        node_list = form.get('highlightNode')
        if node_list is not None:
            data_manager.highlight_node = loads_json(node_list)
            print(data_manager.highlight_node)

        create_node = form.get('createNode')
        if create_node is not None:
            new_node = loads_json(create_node)
            new_node["symbolSize"] = 50
            data_manager.add_node(new_node)
            print(new_node)

            if len(data_manager.highlight_node) == 1:
                new_link = {
                    "source": data_manager.highlight_node[0],
                    "target": new_node["name"],
                    "name": "link04",
                    "des": "link05des"
                }
                data_manager.add_link(new_link)
                print(new_link)

            print(data_manager.get_json())
            data_manager.save_json()
        return redirect(url_for("/.XKMainView"))


class MainBlueprint:
    @staticmethod
    def creator_blueprint():
        blueprint = Blueprint("/", __name__, url_prefix="/", static_folder="static",
                              template_folder="templates")
        blueprint.add_url_rule("/", view_func=XKMainViewAPI.as_view("XKMainView"))
        return blueprint
