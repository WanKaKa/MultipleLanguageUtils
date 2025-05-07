import xml_pro


class StyleItem:
    def __init__(self, **kwargs):
        self.name = kwargs[xml_pro.TAG_NAME] if xml_pro.TAG_NAME in kwargs else None
        self.indicator_color = kwargs[xml_pro.TAG_INDICATOR_COLOR] if xml_pro.TAG_INDICATOR_COLOR in kwargs else None
        self.line_color = kwargs[xml_pro.TAG_LINE_COLOR] if xml_pro.TAG_LINE_COLOR in kwargs else None
        self.status_color = kwargs[xml_pro.TAG_STATUS_COLOR] if xml_pro.TAG_STATUS_COLOR in kwargs else None
        self.text_color = kwargs[xml_pro.TAG_TEXT_COLOR] if xml_pro.TAG_TEXT_COLOR in kwargs else None
        self.wallpaper_color_depth = kwargs[
            xml_pro.TAG_WALLPAPER_COLOR_DEPTH] if xml_pro.TAG_WALLPAPER_COLOR_DEPTH in kwargs else None
        self.vip = kwargs[xml_pro.TAG_VIP] if xml_pro.TAG_VIP in kwargs else "false"

        self.type = kwargs[xml_pro.TAG_TYPE] if xml_pro.TAG_TYPE in kwargs else None
        self.style = kwargs[xml_pro.TAG_STYLE] if xml_pro.TAG_STYLE in kwargs else None
        self.theme_type = kwargs[xml_pro.TAG_THEME_TYPE] if xml_pro.TAG_THEME_TYPE in kwargs else None
        self.shape = kwargs[xml_pro.TAG_SHAPE] if xml_pro.TAG_SHAPE in kwargs else None
        self.click = kwargs[xml_pro.TAG_CLICK] if xml_pro.TAG_CLICK in kwargs else None
        self.thumb_format = kwargs[xml_pro.TAG_THUMB_FORMAT] if xml_pro.TAG_THUMB_FORMAT in kwargs else None
        self.indicator_format = kwargs[xml_pro.TAG_INDICATOR_FORMAT] if xml_pro.TAG_INDICATOR_FORMAT in kwargs else None
        self.content_format = kwargs[xml_pro.TAG_CONTENT_FORMAT] if xml_pro.TAG_CONTENT_FORMAT in kwargs else None
        self.wallpaper_format = kwargs[xml_pro.TAG_WALLPAPER_FORMAT] if xml_pro.TAG_WALLPAPER_FORMAT in kwargs else None

    def __str__(self):
        return "StyleItem = {\n" \
               "    name = %s;\n" \
               "    indicator_color = %s;\n" \
               "    line_color = %s;\n" \
               "    status_color = %s;\n" \
               "    text_color = %s;\n" \
               "    wallpaper_color_depth = %s;\n" \
               "    vip = %s;\n" \
               "    type = %s;\n" \
               "    style = %s;\n" \
               "    theme_type = %s;\n" \
               "    shape = %s;\n" \
               "    click = %s;\n" \
               "    thumb_format = %s;\n" \
               "    indicator_format = %s;\n" \
               "    content_format = %s;\n" \
               "    wallpaper_format = %s;\n" \
               "} " % (
                   self.name,
                   self.indicator_color,
                   self.line_color,
                   self.status_color,
                   self.text_color,
                   self.wallpaper_color_depth,
                   self.vip,
                   self.type,
                   self.style,
                   self.theme_type,
                   self.shape,
                   self.click,
                   self.thumb_format,
                   self.indicator_format,
                   self.content_format,
                   self.wallpaper_format
               )
