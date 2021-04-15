import os

RUN_LOG_NAME = "run_log.txt"


def get_cache_path():
    path = "C:\\IJoySoft\\Kevin\\LockImageConfig\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path
