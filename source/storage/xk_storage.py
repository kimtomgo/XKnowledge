import json
import os
from typing import Union


class JsonFileHandler:
    def __init__(self, file_path: str):
        self.json_data = None
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError

    def reader(self):
        # 加载该文件对象，转换为python类型的数据
        with open(self.file_path, encoding='utf-8') as f:
            self.json_data = json.load(f)

    def writer(self, data: Union[str, dict]):
        # 将json写入文件
        with open(self.file_path, encoding='utf-8') as f:
            json.dump(data, f)

    def package_data(self, title: str):
        categories = [i["category"] for i in self.json_data["data"]]
        categories = list(set(categories))
        categories = [{"name": i} for i in categories]
        self.json_data["categories"] = categories
        self.json_data["title"] = title

    def get_json(self):
        return self.json_data
