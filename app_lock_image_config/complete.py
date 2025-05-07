import os
import sys
import xml_pro

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) > 0:
        file_path = arguments[0]
        print(file_path)

        style_item_list = xml_pro.analysis_wallpaper_xml(file_path)
        print("数量%d" % (len(style_item_list)))

        new_path = file_path + ".ijs"
        new_file = open(new_path, mode='w', encoding='utf-8')

        new_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
        new_file.write("\n")
        new_file.write("<" + xml_pro.TAG_RESOURCES + ">")
        new_file.write(xml_pro.xml_describe)
        new_file.write("\n")

        style_item_pre = None
        for entity in style_item_list:
            new_file.write(xml_pro.create_style_item_xml(entity, style_item_pre, simplify_enable=False))
            style_item_pre = entity
        new_file.write("</" + xml_pro.TAG_RESOURCES + ">")
        new_file.close()

        os.remove(file_path)
        os.rename(new_path, file_path)
    else:
        print("未知路径")
