import json
import os

from modify_suffix import path_ex

database_name = "modify_suffix.json"


def get_json_data():
    if os.path.exists(path_ex.get_cache_path() + database_name):
        read_data = open(path_ex.get_cache_path() + database_name, mode='r', encoding='utf-8')
        try:
            return json.loads(read_data.read())
        finally:
            read_data.close()
    return None


def set_json_data(data):
    temp_data = get_json_data()
    if not temp_data:
        temp_data = {}
    for key in data:
        temp_data[key] = data[key]
    json_file = open(path_ex.get_cache_path() + database_name, mode='w', encoding='utf-8')
    json.dump(temp_data, json_file, indent=4, ensure_ascii=False)
    json_file.close()
