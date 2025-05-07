import os
import xml.dom.minidom
import entity

TAG_RESOURCES = "resources"

TAG_ITEM = "item"

TAG_NAME = "name"
TAG_INDICATOR_COLOR = "indicator_color"
TAG_LINE_COLOR = "line_color"
TAG_STATUS_COLOR = "status_color"
TAG_TEXT_COLOR = "text_color"
TAG_WALLPAPER_COLOR_DEPTH = "wallpaper_color_depth"
TAG_VIP = "vip"

TAG_TYPE = "type"
TAG_STYLE = "style"
TAG_THEME_TYPE = "theme_type"
TAG_SHAPE = "shape"
TAG_CLICK = "click"
TAG_THUMB_FORMAT = "thumb_format"
TAG_INDICATOR_FORMAT = "indicator_format"
TAG_CONTENT_FORMAT = "content_format"
TAG_WALLPAPER_FORMAT = "wallpaper_format"

xml_describe = """
    <!--
    name: 资源名称
    wallpaper_color_depth: 壁纸颜色深浅 dark light
    status_color: 状态栏文字图标颜色
    text_color: 字体颜色
    indicator_color: 指示器颜色
    line_color: 线条颜色
    vip: 是否是vip资源

    type: 资源的访问类型，net是网络，assets是本地
    style: 资源风格，number数字类型，pattern图案风格
    theme_type: 资源分类
    shape: 形状，normal普通九宫格风格
    click: 点击类型，background背景图片，image替换数字图片，alpha修改透明度

    thumb_format: 缩略图资源格式 png 图片 webp 图片
    indicator_format: 指示器资源格式
    content_format: 数字或者图案资源格式
    wallpaper_format: 壁纸资源格式
    -->
"""


def analysis_wallpaper_xml(path):
    if not os.path.exists(path):
        return None
    try:
        item_list = []
        dom = xml.dom.minidom.parse(path)
        root = dom.documentElement
        # 解析gift数据
        gift_item_list = root.getElementsByTagName(TAG_ITEM)
        style_item_pre = None
        for item in gift_item_list:
            style_item = entity.StyleItem()

            style_item.name = item.getAttribute(TAG_NAME)
            if style_item_pre and not style_item.name:
                style_item.name = style_item_pre.name

            style_item.indicator_color = item.getAttribute(TAG_INDICATOR_COLOR)
            if style_item_pre and not style_item.indicator_color:
                style_item.indicator_color = style_item_pre.indicator_color

            style_item.line_color = item.getAttribute(TAG_LINE_COLOR)
            if style_item_pre and not style_item.line_color:
                style_item.line_color = style_item_pre.line_color

            style_item.status_color = item.getAttribute(TAG_STATUS_COLOR)
            if style_item_pre and not style_item.status_color:
                style_item.status_color = style_item_pre.status_color

            style_item.text_color = item.getAttribute(TAG_TEXT_COLOR)
            if style_item_pre and not style_item.text_color:
                style_item.text_color = style_item_pre.text_color

            style_item.wallpaper_color_depth = item.getAttribute(TAG_WALLPAPER_COLOR_DEPTH)
            if style_item_pre and not style_item.wallpaper_color_depth:
                style_item.wallpaper_color_depth = style_item_pre.wallpaper_color_depth

            style_item.vip = item.getAttribute(TAG_VIP)
            if style_item_pre and not style_item.vip:
                style_item.vip = style_item_pre.vip
            if not style_item.vip:
                style_item.vip = "false"

            style_item.type = get_elements_by_tag_name(item, TAG_TYPE)
            if style_item_pre and not style_item.type:
                style_item.type = style_item_pre.type

            style_item.style = get_elements_by_tag_name(item, TAG_STYLE)
            if style_item_pre and not style_item.style:
                style_item.style = style_item_pre.style

            style_item.theme_type = get_elements_by_tag_name(item, TAG_THEME_TYPE)
            if style_item_pre and not style_item.theme_type:
                style_item.theme_type = style_item_pre.theme_type

            style_item.shape = get_elements_by_tag_name(item, TAG_SHAPE)
            if style_item_pre and not style_item.shape:
                style_item.shape = style_item_pre.shape

            style_item.click = get_elements_by_tag_name(item, TAG_CLICK)
            if style_item_pre and not style_item.click:
                style_item.click = style_item_pre.click

            style_item.thumb_format = get_elements_by_tag_name(item, TAG_THUMB_FORMAT)
            if style_item_pre and not style_item.thumb_format:
                style_item.thumb_format = style_item_pre.thumb_format

            style_item.indicator_format = get_elements_by_tag_name(item, TAG_INDICATOR_FORMAT)
            if style_item_pre and not style_item.indicator_format:
                style_item.indicator_format = style_item_pre.indicator_format

            style_item.content_format = get_elements_by_tag_name(item, TAG_CONTENT_FORMAT)
            if style_item_pre and not style_item.content_format:
                style_item.content_format = style_item_pre.content_format

            style_item.wallpaper_format = get_elements_by_tag_name(item, TAG_WALLPAPER_FORMAT)
            if style_item_pre and not style_item.wallpaper_format:
                style_item.wallpaper_format = style_item_pre.wallpaper_format

            # print(style_item)
            style_item_pre = style_item
            item_list.append(style_item)
        return item_list
    except Exception as e:
        print(e)
    return None


def get_elements_by_tag_name(content, name):
    items = content.getElementsByTagName(name)
    if not items or len(items) == 0:
        return None
    # print(items[0].nodeName, ":", items[0].childNodes[0].data)
    return items[0].childNodes[0].data


def create_style_item_xml(style_item: entity.StyleItem, style_item_pre: entity.StyleItem, simplify_enable=True):
    item_str = " " * 4 + "<" + TAG_ITEM + " "
    item_str += TAG_NAME + "=" + "\"" + style_item.name + "\""

    if not simplify_enable or not style_item_pre or style_item.indicator_color != style_item_pre.indicator_color:
        item_str += " " + TAG_INDICATOR_COLOR + "=" + "\"" + style_item.indicator_color + "\""

    if not simplify_enable or not style_item_pre or style_item.line_color != style_item_pre.line_color:
        item_str += " " + TAG_LINE_COLOR + "=" + "\"" + style_item.line_color + "\""

    if not simplify_enable or not style_item_pre or style_item.status_color != style_item_pre.status_color:
        item_str += " " + TAG_STATUS_COLOR + "=" + "\"" + style_item.status_color + "\""

    if not simplify_enable or not style_item_pre or style_item.text_color != style_item_pre.text_color:
        item_str += " " + TAG_TEXT_COLOR + "=" + "\"" + style_item.text_color + "\""

    if not simplify_enable or not style_item_pre or style_item.wallpaper_color_depth != style_item_pre.wallpaper_color_depth:
        item_str += " " + TAG_WALLPAPER_COLOR_DEPTH + "=" + "\"" + style_item.wallpaper_color_depth + "\""

    if not simplify_enable or not style_item_pre or style_item.vip != style_item_pre.vip:
        item_str += " " + TAG_VIP + "=" + "\"" + style_item.vip + "\""

    content_str = ""
    if not simplify_enable or not style_item_pre or style_item.type != style_item_pre.type:
        content_str += "\n" + " " * 8 + "<" + TAG_TYPE + ">" + style_item.type + "</" + TAG_TYPE + ">"
    if not simplify_enable or not style_item_pre or style_item.style != style_item_pre.style:
        content_str += "\n" + " " * 8 + "<" + TAG_STYLE + ">" + style_item.style + "</" + TAG_STYLE + ">"
    if not simplify_enable or not style_item_pre or style_item.theme_type != style_item_pre.theme_type:
        content_str += "\n" + " " * 8 + "<" + TAG_THEME_TYPE + ">" + style_item.theme_type + "</" + TAG_THEME_TYPE + ">"
    if not simplify_enable or not style_item_pre or style_item.shape != style_item_pre.shape:
        content_str += "\n" + " " * 8 + "<" + TAG_SHAPE + ">" + style_item.shape + "</" + TAG_SHAPE + ">"
    if not simplify_enable or not style_item_pre or style_item.click != style_item_pre.click:
        content_str += "\n" + " " * 8 + "<" + TAG_CLICK + ">" + style_item.click + "</" + TAG_CLICK + ">"
    if not simplify_enable or not style_item_pre or style_item.thumb_format != style_item_pre.thumb_format:
        content_str += "\n" + " " * 8 + "<" + TAG_THUMB_FORMAT + ">"
        content_str += style_item.thumb_format
        content_str += "</" + TAG_THUMB_FORMAT + ">"

    if not simplify_enable or not style_item_pre or style_item.indicator_format != style_item_pre.indicator_format:
        content_str += "\n" + " " * 8 + "<" + TAG_INDICATOR_FORMAT + ">"
        content_str += style_item.indicator_format
        content_str += "</" + TAG_INDICATOR_FORMAT + ">"

    if not simplify_enable or not style_item_pre or style_item.content_format != style_item_pre.content_format:
        content_str += "\n" + " " * 8 + "<" + TAG_CONTENT_FORMAT + ">"
        content_str += style_item.content_format
        content_str += "</" + TAG_CONTENT_FORMAT + ">"

    if not simplify_enable or not style_item_pre or style_item.wallpaper_format != style_item_pre.wallpaper_format:
        content_str += "\n" + " " * 8 + "<" + TAG_WALLPAPER_FORMAT + ">"
        content_str += style_item.wallpaper_format
        content_str += "</" + TAG_WALLPAPER_FORMAT + ">"

    if content_str:
        item_str += ">"
        item_str += content_str
        item_str += "\n" + " " * 4 + "</" + TAG_ITEM + ">\n"
    else:
        item_str += " />\n"

    return item_str
