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
        print(data_manager.get_json())
        return render_template("xk_mainview.html", json_data=data_manager.get_json())

    def post(self):
        form = request.form
        loads_json = JsonFileHandler.loads_json

        need_save_data = form.get('saveData')
        if need_save_data is not None:
            data_manager.save_json()

        need_reload_data = form.get('reloadData')
        if need_reload_data is not None:
            data_manager.reload()

        node_list = form.get('highlightNode')
        if node_list is not None:
            data_manager.highlight_node = loads_json(node_list)
            print(data_manager.highlight_node)

        create_node = form.get('createNode')
        if create_node is not None:
            new_node = loads_json(create_node)
            new_node["symbolSize"] = 50
            data_manager.add_node(new_node)
            if len(data_manager.highlight_node) == 1:
                new_link = {
                    "source": data_manager.highlight_node[0],
                    "target": new_node["name"],
                    "name": ""
                }
                data_manager.add_link(new_link)

        create_link = form.get('createEdge')
        if create_link is not None:
            new_link = loads_json(create_link)
            new_link["source"] = data_manager.highlight_node[0]
            new_link["target"] = data_manager.highlight_node[1]
            data_manager.add_link(new_link)

        delete_node_list = form.get('deleteNode')
        if delete_node_list is not None:
            for node_name in data_manager.highlight_node:
                data_manager.del_node(node_name)

        return redirect(url_for("/.XKMainView"))


class MainBlueprint:
    @staticmethod
    def creator_blueprint():
        blueprint = Blueprint("/", __name__, url_prefix="/", static_folder="static",
                              template_folder="templates")
        blueprint.add_url_rule("/", view_func=XKMainViewAPI.as_view("XKMainView"))
        return blueprint
