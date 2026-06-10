import mimetypes
import os
import re
import zipfile

MIME_TO_EXTENSION = {
    # 文本
    'text/plain': '.txt',
    'text/html': '.html',
    'text/css': '.css',
    'text/xml': '.xml',
    'text/csv': '.csv',
    'text/tab-separated-values': '.tsv',
    'text/javascript': '.js',
    'text/markdown': '.md',
    'text/rtf': '.rtf',
    'text/calendar': '.ics',
    'text/vcard': '.vcf',
    'text/x-python': '.py',
    'text/x-c': '.c',
    'text/x-c++': '.cpp',
    'text/x-java': '.java',
    'text/x-shellscript': '.sh',
    'text/x-yaml': '.yaml',
    'text/yaml': '.yaml',
    'text/x-log': '.log',
    'text/x-diff': '.diff',
    'text/x-patch': '.patch',

    # 图片
    'image/jpeg': '.jpg',
    'image/jpg': '.jpg',
    'image/pjpeg': '.jpg',
    'image/png': '.png',
    'image/x-png': '.png',
    'image/gif': '.gif',
    'image/bmp': '.bmp',
    'image/x-bmp': '.bmp',
    'image/tiff': '.tiff',
    'image/x-tiff': '.tiff',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
    'image/x-icon': '.ico',
    'image/vnd.microsoft.icon': '.ico',
    'image/heic': '.heic',
    'image/heif': '.heif',
    'image/avif': '.avif',
    'image/x-portable-pixmap': '.ppm',
    'image/x-portable-graymap': '.pgm',
    'image/x-portable-bitmap': '.pbm',
    'image/vnd.adobe.photoshop': '.psd',
    'image/x-photoshop': '.psd',
    'image/x-xcf': '.xcf',
    'image/vnd.dwg': '.dwg',
    'image/vnd.dxf': '.dxf',

    # 音频
    'audio/mpeg': '.mp3',
    'audio/mp3': '.mp3',
    'audio/wav': '.wav',
    'audio/x-wav': '.wav',
    'audio/flac': '.flac',
    'audio/ogg': '.ogg',
    'audio/aac': '.aac',
    'audio/x-aac': '.aac',
    'audio/x-ms-wma': '.wma',
    'audio/x-m4a': '.m4a',
    'audio/mp4': '.m4a',
    'audio/midi': '.mid',
    'audio/x-midi': '.mid',
    'audio/opus': '.opus',
    'audio/amr': '.amr',

    # 视频
    'video/mp4': '.mp4',
    'video/x-msvideo': '.avi',
    'video/x-ms-asf': '.asf',
    'video/x-ms-wmv': '.wmv',
    'video/3gpp': '.3gp',
    'video/quicktime': '.mov',
    'video/webm': '.webm',
    'video/mpeg': '.mpeg',
    'video/x-matroska': '.mkv',
    'video/x-flv': '.flv',
    'video/x-m4v': '.m4v',
    'video/ogg': '.ogv',
    'video/vnd.avi': '.avi',

    # Office
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.ms-visio': '.vsd',
    'application/vnd.visio': '.vsd',
    'application/onenote': '.one',
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.oasis.opendocument.spreadsheet': '.ods',
    'application/vnd.oasis.opendocument.presentation': '.odp',
    'application/vnd.oasis.opendocument.graphics': '.odg',
    'application/rtf': '.rtf',
    'application/vnd.ms-office': '.doc',

    # PDF / 电子书
    'application/pdf': '.pdf',
    'application/epub+zip': '.epub',
    'application/x-mobipocket-ebook': '.mobi',
    'application/x-fictionbook+xml': '.fb2',

    # 压缩包
    'application/zip': '.zip',
    'application/zip-compressed': '.zip',
    'application/x-zip-compressed': '.zip',
    'application/x-rar-compressed': '.rar',
    'application/vnd.rar': '.rar',
    'application/x-7z-compressed': '.7z',
    'application/x-gzip': '.gz',
    'application/gzip': '.gz',
    'application/x-tar': '.tar',
    'application/x-bzip2': '.bz2',
    'application/x-xz': '.xz',
    'application/x-lzma': '.lzma',
    'application/x-compress': '.z',
    'application/x-iso9660-image': '.iso',
    'application/x-apple-diskimage': '.dmg',

    # 可执行 / 安装包
    'application/x-msdownload': '.exe',
    'application/x-dosexec': '.exe',
    'application/x-ms-installer': '.msi',
    'application/vnd.android.package-archive': '.apk',
    'application/java-archive': '.jar',
    'application/x-shockwave-flash': '.swf',
    'application/x-debian-package': '.deb',
    'application/x-rpm': '.rpm',
    'application/vnd.microsoft.portable-executable': '.exe',

    # 字体
    'font/ttf': '.ttf',
    'font/otf': '.otf',
    'font/woff': '.woff',
    'font/woff2': '.woff2',
    'application/font-sfnt': '.ttf',
    'application/vnd.ms-fontobject': '.eot',
    'application/x-font-ttf': '.ttf',
    'application/x-font-otf': '.otf',
    'application/x-font-woff': '.woff',
    'application/x-font-woff2': '.woff2',

    # 数据 / 配置 / 脚本
    'application/json': '.json',
    'application/xml': '.xml',
    'application/javascript': '.js',
    'application/x-javascript': '.js',
    'application/sql': '.sql',
    'application/x-sqlite3': '.sqlite',
    'application/x-sqlite': '.sqlite',
    'application/x-lua': '.lua',
    'application/x-python': '.py',
    'application/x-python-code': '.py',
    'application/x-java': '.java',
    'application/x-php': '.php',
    'application/x-httpd-php': '.php',
    'application/x-sh': '.sh',
    'application/x-bat': '.bat',
    'application/x-msdos-program': '.com',
    'application/x-perl': '.pl',
    'application/x-ruby': '.rb',
    'application/x-yaml': '.yaml',
    'application/yaml': '.yaml',
    'application/toml': '.toml',
    'application/x-toml': '.toml',
    'application/x-ini': '.ini',
    'application/x-config': '.cfg',
    'application/x-subrip': '.srt',
    'application/x-ass': '.ass',
    'application/x-ssa': '.ssa',
    'application/x-mpegurl': '.m3u8',
    'application/vnd.apple.mpegurl': '.m3u8',
    'application/x-plist': '.plist',
    'application/x-wine-extension-ini': '.ini',

    # 证书 / 密钥
    'application/pkcs7-mime': '.p7m',
    'application/pkcs7-signature': '.p7s',
    'application/x-pkcs12': '.p12',
    'application/pkcs8': '.key',
    'application/x-x509-ca-cert': '.crt',
    'application/x-pem-file': '.pem',
    'application/pgp-keys': '.gpg',
    'application/pgp-signature': '.asc',

    # 设计 / 工程 / 三维
    'application/postscript': '.ps',
    'application/illustrator': '.ai',
    'application/vnd.sketchup.skp': '.skp',
    'model/stl': '.stl',
    'model/obj': '.obj',
    'model/gltf+json': '.gltf',
    'model/gltf-binary': '.glb',
    'application/acad': '.dwg',
    'image/vnd.dwg': '.dwg',
    'application/dxf': '.dxf',
    'application/step': '.step',
    'application/x-step': '.step',
    'application/vnd.ms-pki.stl': '.stl',

    # 数据库 / 虚拟机
    'application/x-msaccess': '.mdb',
    'application/vnd.ms-access': '.mdb',
    'application/x-virtualbox-vdi': '.vdi',
    'application/x-vmdk': '.vmdk',
    'application/x-qcow2': '.qcow2',
}

SUBTYPE_ALIASES = {
    'jpeg': 'jpg',
    'pjpeg': 'jpg',
    'svg+xml': 'svg',
    'x-png': 'png',
    'plain': 'txt',
    'mpeg': 'mpg',
    'quicktime': 'mov',
    'x-ms-wmv': 'wmv',
    'x-msvideo': 'avi',
    'x-matroska': 'mkv',
    'x-flv': 'flv',
    'x-wav': 'wav',
    'x-aac': 'aac',
    'x-midi': 'mid',
    'x-python': 'py',
    'x-java': 'java',
    'x-c': 'c',
    'x-c++': 'cpp',
    'x-shellscript': 'sh',
    'x-yaml': 'yaml',
    'x-tiff': 'tiff',
    'x-bmp': 'bmp',
}

OASIS_MIME_TO_EXTENSION = {
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.oasis.opendocument.spreadsheet': '.ods',
    'application/vnd.oasis.opendocument.presentation': '.odp',
    'application/vnd.oasis.opendocument.graphics': '.odg',
}

SIGNATURE_CHECKS = (
    (0, b'\x89PNG\r\n\x1a\n', '.png'),
    (0, b'GIF87a', '.gif'),
    (0, b'GIF89a', '.gif'),
    (0, b'\xff\xd8\xff', '.jpg'),
    (0, b'BM', '.bmp'),
    (0, b'II*\x00', '.tiff'),
    (0, b'MM\x00*', '.tiff'),
    (0, b'%PDF-', '.pdf'),
    (0, b'PK\x03\x04', None),
    (0, b'\x1f\x8b', '.gz'),
    (0, b'BZh', '.bz2'),
    (0, b'\xfd7zXZ\x00', '.xz'),
    (0, b'Rar!\x1a\x07\x00', '.rar'),
    (0, b'Rar!\x1a\x07\x01\x00', '.rar'),
    (0, b'7z\xbc\xaf\x27\x1c', '.7z'),
    (0, b'\x1a\x45\xdf\xa3', '.mkv'),
    (0, b'FLV\x01', '.flv'),
    (0, b'fLaC', '.flac'),
    (0, b'OggS\x00', '.ogg'),
    (0, b'ID3', '.mp3'),
    (0, b'\xff\xfb', '.mp3'),
    (0, b'\xff\xf3', '.mp3'),
    (0, b'\xff\xf2', '.mp3'),
    (0, b'SQLite format 3\x00', '.sqlite'),
    (0, b'\x00\x00\x01\x00', '.ico'),
    (0, b'8BPS', '.psd'),
    (0, b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', '.doc'),
    (0, b'MZ', '.exe'),
    (0, b'\x7fELF', '.elf'),
    (0, b'<?xml', '.xml'),
    (4, b'ftyp', None),
)

RIFF_FORMATS = {
    b'WAVE': '.wav',
    b'WEBP': '.webp',
    b'AVI ': '.avi',
}

FTYP_BRANDS = {
    b'heic': '.heic',
    b'heix': '.heic',
    b'hevc': '.heic',
    b'heif': '.heif',
    b'mif1': '.heif',
    b'avis': '.avif',
    b'iso2': '.mp4',
    b'isom': '.mp4',
    b'mp41': '.mp4',
    b'mp42': '.mp4',
    b'qt  ': '.mov',
    b'M4V ': '.m4v',
    b'3gp4': '.3gp',
    b'3g2a': '.3g2',
}


def _normalize_extension(extension):
    if not extension:
        return None
    extension = extension.strip().lower()
    if not extension.startswith('.'):
        extension = '.' + extension
    if extension in ('.jpe',):
        return '.jpg'
    return extension


EXTENSION_EQUIVALENTS = (
    {'.jpg', '.jpeg', '.jpe'},
    {'.tif', '.tiff'},
    {'.htm', '.html'},
    {'.mpeg', '.mpg'},
)


def extensions_are_equivalent(current_ext, detected_ext):
    current = _normalize_extension(current_ext)
    detected = _normalize_extension(detected_ext)
    if not current or not detected:
        return False
    if current == detected:
        return True
    for group in EXTENSION_EQUIVALENTS:
        if current in group and detected in group:
            return True
    return False


def _read_header(file_path, size=8192):
    with open(file_path, 'rb') as file:
        return file.read(size)


def _is_apk_archive(names):
    if any(
        name == 'AndroidManifest.xml' or name.endswith('/AndroidManifest.xml')
        for name in names
    ):
        return True
    if 'classes.dex' in names:
        return True
    if any(name.endswith('.dex') for name in names):
        return True
    return False


def _guess_zip_extension(file_path):
    try:
        with zipfile.ZipFile(file_path) as archive:
            names = set(archive.namelist())
            if 'word/document.xml' in names:
                return '.docx'
            if 'xl/workbook.xml' in names:
                return '.xlsx'
            if 'ppt/presentation.xml' in names:
                return '.pptx'
            if _is_apk_archive(names):
                return '.apk'
            if 'META-INF/MANIFEST.MF' in names:
                return '.jar'
            if 'mimetype' in names:
                try:
                    mime = archive.read('mimetype').decode('utf-8', errors='ignore').strip()
                    if mime in OASIS_MIME_TO_EXTENSION:
                        return OASIS_MIME_TO_EXTENSION[mime]
                    if mime == 'application/epub+zip':
                        return '.epub'
                except Exception:
                    pass
    except Exception:
        return None
    return '.zip'


def _guess_riff_extension(header):
    if len(header) < 12 or header[:4] != b'RIFF':
        return None
    return RIFF_FORMATS.get(header[8:12])


def _guess_ftyp_extension(header):
    if len(header) < 12 or header[4:8] != b'ftyp':
        return None
    brand = header[8:12]
    return FTYP_BRANDS.get(brand, '.mp4')


def _guess_by_signature(header):
    if header.startswith(b'RIFF'):
        riff_ext = _guess_riff_extension(header)
        if riff_ext:
            return riff_ext

    if len(header) >= 12 and header[4:8] == b'ftyp':
        return _guess_ftyp_extension(header)

    for offset, marker, extension in SIGNATURE_CHECKS:
        chunk = header[offset:offset + len(marker)]
        if len(chunk) < len(marker):
            continue
        if chunk == marker:
            if marker == b'PK\x03\x04':
                return None
            return extension
    return None


def _guess_by_filetype(file_path):
    try:
        from filetype import filetype
        kind = filetype.guess(file_path)
        if kind:
            return _normalize_extension(kind.extension)
    except Exception:
        pass
    return None


def _guess_by_magic(file_path):
    try:
        import magic
        mime = magic.from_file(file_path, mime=True)
        if mime:
            return extension_from_mime(mime)
    except Exception:
        pass
    return None


def extension_from_mime(mime):
    mime = mime.split(';')[0].strip().lower()
    if mime in MIME_TO_EXTENSION:
        return MIME_TO_EXTENSION[mime]

    guessed = mimetypes.guess_extension(mime, strict=False)
    if guessed:
        return _normalize_extension(guessed)

    if '/' not in mime:
        return None

    major, subtype = mime.split('/', 1)
    subtype = SUBTYPE_ALIASES.get(subtype, subtype)
    if '+' in subtype:
        subtype = subtype.split('+')[-1]

    if major in ('image', 'audio', 'video', 'text', 'font', 'model'):
        if subtype and re.fullmatch(r'[a-z0-9][a-z0-9.-]*', subtype):
            return _normalize_extension(subtype)

    if major == 'application' and subtype.startswith('x-'):
        alias = subtype[2:]
        if alias and re.fullmatch(r'[a-z0-9][a-z0-9.-]*', alias):
            return _normalize_extension(alias)

    return None


def _refine_zip_extension(file_path, extension):
    if extension and extension != '.zip':
        return extension
    zip_ext = _guess_zip_extension(file_path)
    return zip_ext or extension


def guess_file_extension(file_path):
    if not file_path or not os.path.isfile(file_path):
        return None

    try:
        header = _read_header(file_path)
    except Exception:
        header = b''

    is_zip = header.startswith(b'PK\x03\x04') or header.startswith(b'PK\x05\x06')
    if is_zip:
        zip_ext = _guess_zip_extension(file_path)
        if zip_ext and zip_ext != '.zip':
            return zip_ext

    extension = _guess_by_filetype(file_path)
    if extension:
        if is_zip:
            return _refine_zip_extension(file_path, extension)
        return extension

    extension = _guess_by_signature(header)
    if extension:
        return extension

    extension = _guess_by_magic(file_path)
    if extension:
        if is_zip or extension == '.zip':
            return _refine_zip_extension(file_path, extension)
        return extension

    if is_zip:
        return '.zip'

    return None
