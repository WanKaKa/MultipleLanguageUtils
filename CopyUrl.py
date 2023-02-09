import re

re_rule = "http[s]?://[^'^\n]*"

if __name__ == '__main__':
    file = open("C:\\Users\\DELL\\Desktop\\WebUrl.py", mode='r', encoding='utf-8')
    result = open("C:\\Users\\DELL\\Desktop\\WebUrlResult.txt", mode='w', encoding='utf-8')
    line = file.readline()
    copy_enable = False
    while line:
        print(line)
        if copy_enable:
            result_list = re.findall(re_rule, line)
            if len(result_list) > 0:
                result.write(result_list[0])
                result.write("\n")
            copy_enable = False
        if "tests" in line.lower():
            copy_enable = True
        line = file.readline()
    file.close()
    result.close()
