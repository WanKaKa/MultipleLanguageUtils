import xml_pro


class WallpaperItem:
    def __init__(self, **kwargs):
        self.id = kwargs[xml_pro.TAG_ID] if xml_pro.TAG_ID in kwargs else 0
        self.download_url = kwargs[xml_pro.TAG_DOWNLOAD_URL] if xml_pro.TAG_DOWNLOAD_URL in kwargs else None
        self.from_type = kwargs[xml_pro.TAG_FROM] if xml_pro.TAG_FROM in kwargs else None
        self.thumb = kwargs[xml_pro.TAG_THUMB] if xml_pro.TAG_THUMB in kwargs else None
        self.url = kwargs[xml_pro.TAG_URL] if xml_pro.TAG_URL in kwargs else None
        self.vip = kwargs[xml_pro.TAG_VIP] if xml_pro.TAG_VIP in kwargs else "false"

    def __str__(self):
        return "WallpaperItem = {\n" \
               "    id = %d;\n" \
               "    download_url = %s;\n" \
               "    from_type = %s;\n" \
               "    thumb = %s;\n" \
               "    url = %s;\n" \
               "    vip = %s;\n" \
               "} " % (self.id, self.download_url, self.from_type, self.thumb, self.url, self.vip)
