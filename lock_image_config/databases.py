import json
import os

from lock_image_config import path

NORMAL_JSON_DATABASE_NAME = "normal.json"


def get_normal_json_data():
    file_path = path.get_cache_path() + NORMAL_JSON_DATABASE_NAME
    if os.path.exists(file_path):
        read_data = open(file_path, mode='r', encoding='utf-8')
        try:
            return json.loads(read_data.read())
        finally:
            read_data.close()
    return None


def set_normal_json_data(data):
    temp_data = get_normal_json_data()
    if not temp_data:
        temp_data = {}
    for key in data:
        temp_data[key] = data[key]
    json_file = open(path.get_cache_path() + NORMAL_JSON_DATABASE_NAME, mode='w', encoding='utf-8')
    json.dump(temp_data, json_file, indent=4, ensure_ascii=False)
    json_file.close()
