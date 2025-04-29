import os

RUN_LOG_NAME = "run_log.txt"
ANALYSIS_RECOMMEND_LOG_NAME = "analysis_recommend_log.txt"
CHECK_VIP_TXT = "check_vip.txt"


def get_cache_path():
    path = "C:\\IJoySoft\\Kevin\\LockImageConfig\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path
