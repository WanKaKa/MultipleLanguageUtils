import os

image_dir_1 = r"H:\照      片\IPhone7Plus"
image_dir_2 = r"H:\Photo\IPhone7Plus\2020-04-09"


class ImageInfo:

    def __init__(self, name, size, c_time, path):
        self.name = name
        self.size = size
        self.c_time = c_time
        self.path = path


def load_image_info(image_dir):
    image_info_list = []
    for root, dirs, files in os.walk(image_dir):
        print(root)
        print("数量 = %s" % len(files))

        count = 0
        string_builder = ""
        for file in files:
            count += 1
            string_builder += str(file).ljust(15, " ")
            if count % 10 == 0:
                print(string_builder)
                count = 0
                string_builder = ""
            path = os.path.join(root, file)
            image_info_list.append(ImageInfo(file, os.path.getsize(path), os.path.getctime(path), path))
        print("\n" * 2)
    return image_info_list


if __name__ == '__main__':
    image_info_list_1 = load_image_info(image_dir_1)
    # image_info_list_2 = load_image_info(image_dir_2)
    same_count = 0
    for index_1 in range(len(image_info_list_1)):
        for index_2 in range(len(image_info_list_1)):
            if index_1 == index_2:
                continue
            info_1 = image_info_list_1[index_1]
            info_2 = image_info_list_1[index_2]
            if info_1.size == info_2.size and info_1.c_time == info_2.c_time:
                same_count += 1
                print("图片相同".center(50, "*"))
                print(info_1.path)
                print(info_2.path)
                print("*" * 50)
    print("相同的数量为 = %d" % same_count)
