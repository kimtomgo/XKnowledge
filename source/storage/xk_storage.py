import json
import os
from typing import Union


class JsonFileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError

    def reader(self):
        # 加载该文件对象，转换为python类型的数据
        with open(self.file_path, encoding='utf-8') as f:
            return json.load(f)

    def writer(self, data: Union[str, dict]):
        # 将json写入文件
        with open(self.file_path, encoding='utf-8') as f:
            json.dump(data, f)
