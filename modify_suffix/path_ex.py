import os

LOG_REMOVE_SUFFIX = "log_remove_suffix.txt"
LOG_MODIFY_SUFFIX = "log_modify_suffix.txt"
LOG_BANDIZIP = "log_bandizip.txt"
DELETE_FRAME = "delete_frame.txt"


def get_cache_path():
    path = "C:\\IJoySoft\\Kevin\\ModifySuffix\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path
