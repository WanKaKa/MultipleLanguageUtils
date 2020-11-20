import os
import re

########################################################################################

# project_res_path: 需要删除的字符的文件夹路径
# delete_string_key_list: 删除的字符，以逗号隔开，例如["example1",""example2""]
project_res_dir = r"C:\Work\ASProjects\LockScreenGridAS\app\src\main\res"
delete_string_key_list = ["menu"]

########################################################################################


string_file_name = ["\\string.xml", "\\strings.xml"]
filter_string_key_regular = """<string name="(.+?)">"""


def delete_android_values_string():
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            for res_dir in dirs:
                if os.path.exists(project_res_dir + "\\" + res_dir):
                    if res_dir != "values" and "values" in res_dir:
                        print("*" * 50)
                        print(res_dir)
                        for path in string_file_name:
                            file_path = project_res_dir + "\\" + res_dir + path
                            if os.path.exists(file_path):
                                tmp_file_path = file_path + ".ijs"
                                file = open(file_path, mode='r', encoding='utf-8')
                                tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
                                line = file.readline()
                                temp_read_str = ""
                                while line:
                                    temp_read_str += line
                                    if "resources" in temp_read_str or "</string>" in temp_read_str:
                                        key_list = re.findall(filter_string_key_regular, temp_read_str)
                                        delete_enable = False
                                        if key_list:
                                            for key in delete_string_key_list:
                                                if key == key_list[0]:
                                                    delete_enable = True
                                                    print("已删除%s" % key)
                                                    break
                                        if not delete_enable:
                                            tmp_file.write(temp_read_str)
                                        temp_read_str = ""
                                    line = file.readline()
                                file.close()
                                tmp_file.close()
                                os.remove(file_path)
                                os.rename(tmp_file_path, file_path)
                                break
                        print("%s\n\n" % ("*" * 50))


if __name__ == '__main__':
    delete_android_values_string()
    os.system("pause")
