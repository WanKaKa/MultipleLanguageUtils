import os
import re

string_file_name = ["\\string.xml", "\\strings.xml"]
filter_string_key_regular = """<string name="(.+?)">"""
filter_folder = ["large", "small", "dpi", "land", "port"]


def copy_string():
    for root, dirs, file_paths in os.walk(translate_res_path):
        if dirs:
            print("root = %s;\ndirs = %s;\nfiles = %s\n" % (root, dirs, file_paths))
            add_string_key_list = []
            for res_dir in dirs:
                isPassPath = False
                if "values" not in res_dir:
                    isPassPath = True
                else:
                    for i in range(9):
                        if str(i) in res_dir:
                            isPassPath = True
                    for str_folder in filter_folder:
                        if str_folder in res_dir:
                            isPassPath = True
                if isPassPath:
                    continue
                # 判断项目是否存在对应的语音文件夹，不存在则创建文件夹和文件
                if not os.path.exists(project_res_path + "\\" + res_dir):
                    os.makedirs(project_res_path + "\\" + res_dir)
                    file = open(project_res_path + "\\" + res_dir + "\\strings.xml", mode='w', encoding='utf-8')
                    file.write("""<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>""")
                    file.close()
                print("语言文件夹 = \033[0;32;40m%s\033[0m" % res_dir)
                if res_dir == "values":
                    add_string_key_list = analysis_equal_sting(res_dir)
                else:
                    analysis_add_string(res_dir, add_string_key_list)


def analysis_equal_sting(res_dir):
    """
        提取相同字符的key值
        res_dir : 资源文件夹名称
    """
    for path in string_file_name:
        file_path = translate_res_path + "\\" + res_dir + path
        add_string_key_list = []
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        if judge_string_exist_project(res_dir, key_list[0]):
                            add_string_key_list.append(key_list[0])
                    temp_read_str = ""
                line = file.readline()
            file.close()
            print("新增字符的KEY:\n%s\n%s" % (add_string_key_list, "*" * 50))
            return add_string_key_list


def analysis_add_string(res_dir, add_string_key_list):
    """
        判断项目资源文件夹中是否存在翻译字符，存在则不添加
        res_dir : 资源文件夹名称
    """
    for path in string_file_name:
        file_path = translate_res_path + "\\" + res_dir + path
        add_string = ""
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        # print(string_keys[0])
                        for key in add_string_key_list:
                            if key == key_list[0]:
                                if not judge_string_exist_project(res_dir, key_list[0]):
                                    add_string = add_string + "\n" + temp_read_str.strip("\n")
                                    break
                    temp_read_str = ""
                line = file.readline()
            file.close()
            if add_string:
                write_string_to_project(res_dir, add_string)
            print("新增字符:\n\033[0;32;40m%s\033[0m\n%s" % (add_string, "*" * 50))
            return
    print("\n此文件夹下没有string.xml或者strings.xml\n%s" % ("*" * 50))


def judge_string_exist_project(res_dir, string_key):
    """
        判断字符在项目文件中是否不存在
        res_dir : 资源文件夹名称
        string_key : 字符名称
    """
    for path in string_file_name:
        file_path = project_res_path + "\\" + res_dir + path
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        if key_list[0] == string_key:
                            return True
                    temp_read_str = ""
                line = file.readline()
            file.close()
    return False


def write_string_to_project(res_dir, add_string):
    """
        写入新增字符到项目字符文件中
        res_dir : 资源文件夹名称
        add_string : 需要插入的字符
    """
    for path in string_file_name:
        file_path = project_res_path + "\\" + res_dir + path
        if os.path.exists(file_path):
            tmp_file_path = file_path + ".ijs"
            file = open(file_path, mode='r', encoding='utf-8')
            tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
            line = file.readline()
            while line:
                if "</resources>" in line:
                    break
                tmp_file.write(line)
                line = file.readline()
            tmp_file.write(add_string)
            tmp_file.write("\n</resources>")
            file.close()
            tmp_file.close()
            os.remove(file_path)
            os.rename(tmp_file_path, file_path)
            break


if __name__ == '__main__':
    print("""
        \033[0;31;40m
        先把需要翻译的字符手动拷贝到项目的values下
        
        此脚本的逻辑是
        1. 找到项目中values和翻译文件夹中values相同的字符
        2. 拷贝1步骤中筛选出来的字符到对应的语言目录下，如果项目中对应的语言存在此字符，则跳过拷贝
        \033[0m
    """)
    example1 = r"C:\Work\ASProjects\WeatherForecastBM\WeatherForecast\src\main\res"
    example2 = r"C:\Work\ASProjects\WeatherForecastAS\WeatherForecast\src\main\res"
    translate_res_path = input("翻译资源路径(例如: \033[0;31;40m%s\033[0m)\n" % example1)
    # if not translate_res_path:
    #     translate_res_path = example1
    project_res_path = input("项目资源路径(例如: \033[0;31;40m%s\033[0m)\n" % example2)
    # if not project_res_path:
    #     project_res_path = example2
    print("\n%s解析复制开始%s\n" % ("▼ " * 18, " ▼" * 18))
    copy_string()
    print("\n%s解析复制结束%s\n" % ("▲ " * 18, " ▲" * 18))
    # os.system("pause")
