import os
import xml.dom.minidom
import entity

TAG_SKIN = "skin"

# gift参数
TAG_ITEM = "item"
TAG_ID = "id"
TAG_DOWNLOAD_URL = "download_url"
TAG_FROM = "from"
TAG_THUMB = "thumb"
TAG_URL = "url"


def analysis_wallpaper_xml(path):
    if not os.path.exists(path):
        return None
    try:
        item_list = []
        dom = xml.dom.minidom.parse(path)
        root = dom.documentElement
        # 解析gift数据
        gift_item_list = root.getElementsByTagName(TAG_ITEM)
        for item in gift_item_list:
            wallpaper_item = entity.WallpaperItem()

            wallpaper_item.id = item.getAttribute(TAG_ID)
            wallpaper_item.download_url = item.getAttribute(TAG_DOWNLOAD_URL)
            wallpaper_item.from_type = item.getAttribute(TAG_FROM)
            wallpaper_item.thumb = item.getAttribute(TAG_THUMB)
            wallpaper_item.url = item.getAttribute(TAG_URL)

            item_list.append(wallpaper_item)
        return item_list
    except Exception as e:
        print(e)
    return None
