import os
from typing import Union

from source.storage.xk_json import JsonFileHandler


class XKDataManager:
    """ 在内存中做数据管理，调用底层的handler """

    def __init__(self, file_path: Union[str, os.PathLike], title: str):
        self.json_handler = None  # 保留一个json处理器
        self.file_path = file_path  # json对应的文件路径
        self.json_data = None  # 储存在内存中的json数据
        self.title = title  # 储存图的标题
        self.highlight_node = []
        if not os.path.exists(self.file_path):
            raise FileNotFoundError
        else:
            self.json_handler = JsonFileHandler(self.file_path)
            self.json_data = self.json_handler.reader()

    def package(self):
        if self.json_handler is not None:
            self.json_data = self.json_handler.package_json(self.json_data, self.title)

    def get_json(self):
        return self.json_data

    def save_json(self):
        self.json_handler.writer(self.json_data)

    def add_node(self, new_node):
        self.json_data["data"].append(new_node)

    def add_link(self, new_link):
        self.json_data["links"].append(new_link)
