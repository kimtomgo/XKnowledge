import os

from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from wtforms import Form, StringField, IntegerField
from wtforms.validators import length

from storage.xk_datamanager import global_data_manager
from storage.xk_json import JsonFileHandler


class XKFileForm(Form):
    file_path = StringField(validators=[length(min=0, max=20, message="error")])
    node_list_length = IntegerField()
    node_list = StringField(validators=[length(min=0, max=20, message="error")])


class XKHomePageViewAPI(MethodView):
    """ 这个类相当于一个session，每一个session在内存中保有一个数据管理器 """

    def get(self):
        folder_path = "../data"
        files_and_folders = os.listdir(folder_path)
        # todo 未来支持创建文件夹
        files = [file for file in files_and_folders if os.path.isfile(os.path.join(folder_path, file))]

        return render_template("xk_homepage.html", files=files)

    def post(self):
        form = request.form
        loads_json = JsonFileHandler.loads_json

        file_name = form.get('file_name')
        if file_name is not None:
            global_data_manager.set_title(loads_json(file_name))
            global_data_manager.open_file()

        return redirect(url_for("XKnowledge.XKMainView"))
