import os

LOG_REMOVE_SUFFIX = "log_remove_suffix.txt"
LOG_ADD_SUFFIX = "log_add_suffix.txt"
LOG_MODIFY_SUFFIX = "log_modify_suffix.txt"
LOG_BANDIZIP = "log_bandizip.txt"
LOG_DELETE_FRAME = "log_delete_frame.txt"
LOG_MODIFY_NAME = "log_modify_name.txt"


def get_cache_path():
    path = "C:\\IJoySoft\\Kevin\\ModifySuffix\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path
