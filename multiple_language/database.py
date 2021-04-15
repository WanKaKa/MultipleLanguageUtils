import json
import os
from multiple_language import kevin_utils

database_name = "json_multiple_language.json"


def get_json_data():
    if os.path.exists(kevin_utils.get_log_path() + database_name):
        read_data = open(kevin_utils.get_log_path() + database_name, mode='r', encoding='utf-8')
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
    json_file = open(kevin_utils.get_log_path() + database_name, mode='w', encoding='utf-8')
    json.dump(temp_data, json_file, indent=4, ensure_ascii=False)
    json_file.close()
